"""1:1 채팅 도메인 로직 — 방 생성 정책, SAFE 동기 전송 파이프라인, SAFE-05 제한."""

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.age import is_minor
from app.core.config import settings
from app.core.enums import MessageType, RoomState, SafetyStatus
from app.core.pairs import normalize_pair
from app.models import ChatMessage, ChatRoom, SendRestriction, User
from app.services.relations import are_friends, is_blocked_either
from app.services.safety import SafetyClient, SafetyUnavailable


class ChatPolicyError(Exception):
    """차단·연령 보호 등 — 라우터에서 404 + 사유 비노출 메시지로 변환."""


class SendRestricted(Exception):
    """SAFE-05 활성 제한 — 발신자에게는 '메시지를 보낼 수 없습니다'만 (403)."""


def counterpart_id(room: ChatRoom, me_id: uuid.UUID) -> uuid.UUID | None:
    return room.user_b if room.user_a == me_id else room.user_a


async def get_or_create_room(db: AsyncSession, me: User, other: User) -> ChatRoom:
    """친구=active, 비친구=request. 차단·수신 거부·미성년 보호는 사유 비노출로 거부."""
    if await is_blocked_either(db, me.id, other.id):
        raise ChatPolicyError()

    ua, ub = normalize_pair(me.id, other.id)
    room = (
        await db.execute(select(ChatRoom).where(ChatRoom.user_a == ua, ChatRoom.user_b == ub))
    ).scalar_one_or_none()
    friends = await are_friends(db, me.id, other.id)

    if room is not None:
        # 요청 방 상태에서 친구가 되면 일반 채팅으로 승격
        if room.state == RoomState.request.value and friends:
            room.state = RoomState.active.value
            room.accepted_at = datetime.now(timezone.utc)
            await db.commit()
        return room

    if not friends:
        # CHAT-02: 수신자 허용 설정 (§4.5 — 미성년은 가입 시 기본 false)
        if not other.stranger_requests_allowed:
            raise ChatPolicyError()

    room = ChatRoom(
        id=uuid.uuid4(),
        user_a=ua,
        user_b=ub,
        state=RoomState.active.value if friends else RoomState.request.value,
        requested_by=None if friends else me.id,
        accepted_at=datetime.now(timezone.utc) if friends else None,
    )
    db.add(room)
    await db.commit()
    return room


async def has_active_restriction(
    db: AsyncSession, sender_id: uuid.UUID, receiver_id: uuid.UUID
) -> bool:
    row = (
        await db.execute(
            select(SendRestriction.id).where(
                SendRestriction.sender_id == sender_id,
                SendRestriction.receiver_id == receiver_id,
                SendRestriction.active.is_(True),
            )
        )
    ).first()
    return row is not None


async def flagged_count_since_reset(
    db: AsyncSession, room_id: uuid.UUID, sender_id: uuid.UUID, receiver_id: uuid.UUID
) -> int:
    """SAFE-05 누적: flagged AND created_at > max(now-기간, 마지막 released_at)."""
    boundary = datetime.now(timezone.utc) - timedelta(days=settings.SAFE_FLAG_WINDOW_DAYS)
    last_release = (
        await db.execute(
            select(func.max(SendRestriction.released_at)).where(
                SendRestriction.sender_id == sender_id,
                SendRestriction.receiver_id == receiver_id,
            )
        )
    ).scalar_one_or_none()
    if last_release is not None and last_release > boundary:
        boundary = last_release
    return (
        await db.execute(
            select(func.count()).select_from(ChatMessage).where(
                ChatMessage.room_id == room_id,
                ChatMessage.sender_id == sender_id,
                ChatMessage.safety_status == SafetyStatus.flagged.value,
                ChatMessage.created_at > boundary,
            )
        )
    ).scalar_one()


async def send_text(
    db: AsyncSession,
    safety: SafetyClient,
    me: User,
    room: ChatRoom,
    content: str,
) -> tuple[ChatMessage, bool]:
    """SAFE-01 동기 파이프라인. → (메시지, 이번 전송으로 제한이 새로 발동했는지)."""
    other_id = counterpart_id(room, me.id)
    if other_id is None:
        raise ChatPolicyError()  # 상대가 탈퇴한 방
    if await is_blocked_either(db, me.id, other_id):
        raise ChatPolicyError()  # BLOCK-01이 최우선
    if await has_active_restriction(db, me.id, other_id):
        raise SendRestricted()

    is_request_room = room.state == RoomState.request.value
    if is_request_room:
        if room.requested_by != me.id:
            raise ChatPolicyError()  # 수신자는 수락으로만 응답
        sent_before = (
            await db.execute(
                select(func.count()).select_from(ChatMessage).where(
                    ChatMessage.room_id == room.id, ChatMessage.sender_id == me.id
                )
            )
        ).scalar_one()
        if sent_before >= 1:
            raise ValueError("요청이 수락되기 전에는 메시지를 1건만 보낼 수 있습니다")

    other = await db.get(User, other_id)
    try:
        verdict = await safety.analyze(content, receiver_is_minor=is_minor(other.birth_date))
        status = SafetyStatus.safe.value if verdict == "safe" else SafetyStatus.flagged.value
    except SafetyUnavailable:
        # §18.3: 친구=성능저하 모드로 전달, 비친구 요청=보류 (동기 원칙 유지)
        status = SafetyStatus.pending.value if is_request_room else SafetyStatus.unanalyzed.value

    message = ChatMessage(
        id=uuid.uuid4(),
        room_id=room.id,
        sender_id=me.id,
        type=MessageType.text.value,
        content=content,
        safety_status=status,
    )
    db.add(message)
    await db.flush()

    newly_restricted = False
    if status == SafetyStatus.flagged.value:
        count = await flagged_count_since_reset(db, room.id, me.id, other_id)
        if count >= settings.SAFE_FLAG_LIMIT and not await has_active_restriction(
            db, me.id, other_id
        ):
            db.add(SendRestriction(id=uuid.uuid4(), sender_id=me.id, receiver_id=other_id))
            newly_restricted = True

    await db.commit()
    return message, newly_restricted


async def reanalyze_unanalyzed(session_factory, redis, safety: SafetyClient) -> int:
    """§18.3: 모델 복구 후 미분석(unanalyzed)·보류(pending) 텍스트 재분석.

    재분석에서 주의 판정 시 소급 블러(=flagged 저장) + 수신자 알림.
    미디어 메시지는 대상이 아니다 (type=text만, SAFE-02).
    """
    from app.services import notify as noti

    processed = 0
    async with session_factory() as db:
        rows = (
            await db.execute(
                select(ChatMessage).where(
                    ChatMessage.type == MessageType.text.value,
                    ChatMessage.safety_status.in_(
                        [SafetyStatus.unanalyzed.value, SafetyStatus.pending.value]
                    ),
                )
            )
        ).scalars().all()
        for msg in rows:
            if msg.sender_id is None or msg.content is None:
                continue
            room = await db.get(ChatRoom, msg.room_id)
            other_id = counterpart_id(room, msg.sender_id)
            if other_id is None:
                continue
            other = await db.get(User, other_id)
            try:
                verdict = await safety.analyze(
                    msg.content, receiver_is_minor=is_minor(other.birth_date)
                )
            except SafetyUnavailable:
                continue  # 아직 복구 전 — 다음 주기에 재시도
            msg.safety_status = (
                SafetyStatus.safe.value if verdict == "safe" else SafetyStatus.flagged.value
            )
            await db.commit()
            processed += 1
            if msg.safety_status == SafetyStatus.flagged.value:
                # 소급 블러 + 추가 알림 (§18.3)
                await noti.notify(
                    db, redis, other_id, noti.CHAT_FLAGGED,
                    {"room_id": str(msg.room_id), "message_id": str(msg.id), "retroactive": True},
                )
    return processed


async def release_restriction(
    db: AsyncSession, sender_id: uuid.UUID, receiver: User
) -> bool:
    """수신자의 제한 해제 — released_at 기록이 곧 누적 카운터 리셋 (SAFE-05-7)."""
    rows = (
        await db.execute(
            select(SendRestriction).where(
                SendRestriction.sender_id == sender_id,
                SendRestriction.receiver_id == receiver.id,
                SendRestriction.active.is_(True),
            )
        )
    ).scalars().all()
    if not rows:
        return False
    now = datetime.now(timezone.utc)
    for r in rows:
        r.active = False
        r.released_at = now
    await db.commit()
    return True
