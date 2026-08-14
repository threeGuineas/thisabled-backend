"""CHAT-01~05 — 1:1 채팅 · 요청함 · 읽음 · WebRTC 시그널링."""

import json
import uuid
from urllib.parse import quote, unquote
from datetime import datetime, timezone

import redis.asyncio as aioredis
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.age import is_minor
from app.core.config import settings
from app.core.deps import get_current_user
from app.core.enums import AiStatus, MediaType, MessageType, RoomState, SafetyStatus
from app.core.storage import (
    ALLOWED_CONTENT_TYPES,
    UploadTooLarge,
    delete_upload,
    save_upload,
    save_upload_stream,
)
from app.db.redis import get_redis
from app.db.session import get_db, get_session_factory
from app.models import ChatMessage, ChatRoom, User
from app.schemas.chat import (
    MessageIn,
    MessageListOut,
    MessageOut,
    CallCreateIn,
    CallOut,
    CallSignalIn,
    CallSignalOut,
    RevealOut,
    RoomCreateIn,
    RoomListOut,
    RoomMessagePreviewOut,
    RoomOut,
)
from app.schemas.post import AuthorOut
from app.services import ai_media, media_probe
from app.services import notify as noti
from app.services.events import publish_to_user
from app.services.presence import online_statuses
from app.services import call_signaling
from app.services.chat import (
    ChatPolicyError,
    SendRestricted,
    advance_read_cursor,
    counterpart_read_message_id,
    counterpart_id,
    get_or_create_room,
    has_active_restriction,
    release_restriction,
    send_text,
    unread_count,
)
from app.services.quota import (
    CAPTION_GLOBAL_LIMIT,
    CAPTION_USER_LIMIT,
    caption_key,
    consume_caption,
)
from app.services.relations import are_friends, is_blocked_either
from app.services.safety import SafetyClient, get_safety_client

router = APIRouter(prefix="/chat", tags=["chat"])

UNAVAILABLE = "요청을 보낼 수 없는 상대입니다"  # CHAT-02 사유 비노출
RESTRICTED = "메시지를 보낼 수 없습니다"  # SAFE-05-4 사유 비노출

ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}


class RestrictionReleaseOut(BaseModel):
    released: bool


def _author(u: User | None) -> AuthorOut:
    if u is None:
        return AuthorOut(id=None, nickname="탈퇴한 사용자")
    return AuthorOut(id=u.id, nickname=u.nickname, profile_image_url=u.profile_image_url)


async def _get_my_room(db: AsyncSession, me: User, room_id: uuid.UUID) -> ChatRoom:
    room = await db.get(ChatRoom, room_id)
    if room is None or me.id not in (room.user_a, room.user_b):
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")
    return room


async def _validate_call_room(
    db: AsyncSession, me: User, room: ChatRoom
) -> tuple[uuid.UUID, User]:
    other_id = counterpart_id(room, me.id)
    if other_id is None or room.state != RoomState.active.value:
        raise HTTPException(status_code=403, detail="통화할 수 없는 채팅방입니다")
    if not await are_friends(db, me.id, other_id):
        raise HTTPException(status_code=403, detail="통화는 친구와의 채팅에서만 가능합니다")
    if await is_blocked_either(db, me.id, other_id):
        raise HTTPException(status_code=403, detail=RESTRICTED)
    if await has_active_restriction(db, me.id, other_id) or await has_active_restriction(
        db, other_id, me.id
    ):
        raise HTTPException(status_code=403, detail=RESTRICTED)
    other = await db.get(User, other_id)
    if other is None:
        raise HTTPException(status_code=403, detail="통화할 수 없는 채팅방입니다")
    if is_minor(me.birth_date) != is_minor(other.birth_date):
        raise HTTPException(status_code=403, detail="이 채팅에서는 통화할 수 없습니다")
    return other_id, other


def _message_out(
    m: ChatMessage,
    me_id: uuid.UUID,
    sender: User | None,
    counterpart_read_message_id: uuid.UUID | None = None,
) -> MessageOut:
    mine = m.sender_id == me_id
    blurred = False
    content = m.content
    safety: str | None = None
    if not mine:
        # SAFE-03: 수신자 화면 — flagged & 미열람은 블러, unanalyzed는 '미분석' 표시
        safety = m.safety_status
        if m.safety_status == SafetyStatus.flagged.value and m.revealed_at is None:
            blurred = True
            content = None
    return MessageOut(
        id=m.id, room_id=m.room_id, sender=_author(sender), mine=mine,
        type=m.type, content=content, blurred=blurred, safety_status=safety,
        media_url=m.media_url, description=m.description,
        description_status=m.description_status, caption=m.caption,
        caption_status=m.caption_status, created_at=m.created_at,
        is_read=mine and m.id == counterpart_read_message_id,
    )


def _message_preview(message: ChatMessage, me_id: uuid.UUID) -> RoomMessagePreviewOut:
    mine = message.sender_id == me_id
    blurred = (
        not mine
        and message.safety_status == SafetyStatus.flagged.value
        and message.revealed_at is None
    )
    return RoomMessagePreviewOut(
        id=message.id,
        type=message.type,
        content=None if blurred else message.content,
        mine=mine,
        blurred=blurred,
        created_at=message.created_at,
    )


async def _latest_messages(
    db: AsyncSession, room_ids: list[uuid.UUID]
) -> dict[uuid.UUID, ChatMessage]:
    if not room_ids:
        return {}
    ranked = (
        select(
            ChatMessage.id.label("message_id"),
            func.row_number()
            .over(
                partition_by=ChatMessage.room_id,
                order_by=(ChatMessage.available_at.desc(), ChatMessage.id.desc()),
            )
            .label("position"),
        )
        .where(
            ChatMessage.room_id.in_(room_ids),
            ChatMessage.safety_status != SafetyStatus.pending.value,
            ChatMessage.available_at.is_not(None),
        )
        .subquery()
    )
    rows = (
        await db.execute(
            select(ChatMessage)
            .join(ranked, ranked.c.message_id == ChatMessage.id)
            .where(ranked.c.position == 1)
        )
    ).scalars().all()
    return {message.room_id: message for message in rows}


async def _room_out(
    db: AsyncSession,
    me: User,
    room: ChatRoom,
    *,
    other: User | None,
    latest: ChatMessage | None,
    online: bool,
) -> RoomOut:
    other_id = counterpart_id(room, me.id)
    restricted = (
        await has_active_restriction(db, other_id, me.id) if other_id is not None else False
    )
    return RoomOut(
        id=room.id, state=room.state, counterpart=_author(other),
        requested_by=room.requested_by, restricted_sender=restricted,
        accepted_at=room.accepted_at, created_at=room.created_at,
        unread_count=await unread_count(db, room.id, me.id),
        last_message=_message_preview(latest, me.id) if latest is not None else None,
        last_activity_at=(latest.available_at or latest.created_at) if latest else room.created_at,
        counterpart_online=online,
    )


async def _rooms_out(
    db: AsyncSession,
    redis: aioredis.Redis,
    me: User,
    rooms: list[ChatRoom],
) -> list[RoomOut]:
    other_ids = [other_id for room in rooms if (other_id := counterpart_id(room, me.id))]
    users = {
        user.id: user
        for user in (
            (await db.execute(select(User).where(User.id.in_(other_ids)))).scalars().all()
            if other_ids
            else []
        )
    }
    latest_by_room = await _latest_messages(db, [room.id for room in rooms])
    online_by_user = await online_statuses(redis, list(users))
    items = [
        await _room_out(
            db,
            me,
            room,
            other=users.get(counterpart_id(room, me.id)),
            latest=latest_by_room.get(room.id),
            online=online_by_user.get(counterpart_id(room, me.id), False),
        )
        for room in rooms
    ]
    return sorted(items, key=lambda item: (item.last_activity_at, str(item.id)), reverse=True)


@router.post("/rooms", response_model=RoomOut)
async def create_room(
    body: RoomCreateIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    if body.user_id == user.id:
        raise HTTPException(status_code=400, detail="자기 자신과는 채팅할 수 없습니다")
    other = await db.get(User, body.user_id)
    if other is None:
        raise HTTPException(status_code=404, detail=UNAVAILABLE)
    try:
        room = await get_or_create_room(db, user, other)
    except ChatPolicyError:
        raise HTTPException(status_code=404, detail=UNAVAILABLE)
    return (await _rooms_out(db, redis, user, [room]))[0]


@router.get("/rooms", response_model=RoomListOut)
async def list_rooms(
    search_text: str | None = Query(default=None, alias="q", max_length=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    rooms = (
        await db.execute(
            select(ChatRoom)
            .where(
                or_(ChatRoom.user_a == user.id, ChatRoom.user_b == user.id),
                ChatRoom.state == RoomState.active.value,
            )
        )
    ).scalars().all()
    items = await _rooms_out(db, redis, user, rooms)
    unread_total = sum(item.unread_count for item in items)
    search = search_text.strip().casefold() if search_text else None
    if search:
        items = [item for item in items if search in item.counterpart.nickname.casefold()]
    return RoomListOut(items=items, unread_total=unread_total)


@router.get("/requests", response_model=RoomListOut)
async def list_requests(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """요청함 (CHAT-02) — 분석 완료된 메시지가 있는 요청만 표시 (SAFE-01 동기 원칙)."""
    rooms = (
        await db.execute(
            select(ChatRoom)
            .where(
                or_(ChatRoom.user_a == user.id, ChatRoom.user_b == user.id),
                ChatRoom.state == RoomState.request.value,
                ChatRoom.requested_by != user.id,
            )
            .order_by(ChatRoom.created_at.desc())
        )
    ).scalars().all()
    visible_rooms: list[ChatRoom] = []
    for room in rooms:
        analyzed = (
            await db.execute(
                select(func.count()).select_from(ChatMessage).where(
                    ChatMessage.room_id == room.id,
                    ChatMessage.safety_status != SafetyStatus.pending.value,
                )
            )
        ).scalar_one()
        if analyzed > 0:
            visible_rooms.append(room)
    visible = await _rooms_out(db, redis, user, visible_rooms)
    return RoomListOut(
        items=visible,
        unread_total=sum(item.unread_count for item in visible),
    )


@router.post("/rooms/{room_id}/messages", response_model=MessageOut, status_code=201)
async def send_message(
    room_id: uuid.UUID,
    body: MessageIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    safety: SafetyClient = Depends(get_safety_client),
):
    room = await _get_my_room(db, user, room_id)
    try:
        message, newly_restricted = await send_text(db, safety, user, room, body.content)
    except SendRestricted:
        raise HTTPException(status_code=403, detail=RESTRICTED)
    except ChatPolicyError:
        raise HTTPException(status_code=403, detail=RESTRICTED)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    other_id = counterpart_id(room, user.id)
    if other_id is not None and message.safety_status != SafetyStatus.pending.value:
        # 원문은 싣지 않는다 — 수신 측이 REST로 조회하며 블러 규칙 적용
        await publish_to_user(
            redis, other_id,
            {"type": "chat.message", "payload": {"room_id": str(room.id), "message_id": str(message.id)}},
        )
        if room.state == RoomState.request.value:
            await noti.notify(
                db, redis, other_id, noti.CHAT_REQUEST,
                {"room_id": str(room.id), "sender_nickname": user.nickname},
            )
        if message.safety_status == SafetyStatus.flagged.value:
            # 주의 메시지 도착 — 수신자에게만 (§16, SAFE-03)
            await noti.notify(
                db, redis, other_id, noti.CHAT_FLAGGED,
                {"room_id": str(room.id), "message_id": str(message.id)},
            )
    if other_id is not None and newly_restricted:
        # SAFE-05-5: 수신자 안내 (발신자에게는 어떤 알림도 없음)
        await noti.notify(
            db, redis, other_id, noti.CHAT_RESTRICTED,
            {
                "room_id": str(room.id),
                "sender_id": str(user.id),
                "message": "위험 가능성이 있는 메시지가 반복되어 전송을 제한했어요",
            },
        )
    return _message_out(message, user.id, user)


@router.get("/rooms/{room_id}/messages", response_model=MessageListOut)
async def list_messages(
    room_id: uuid.UUID,
    cursor: str | None = None,
    limit: int = Query(default=30, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    room = await _get_my_room(db, user, room_id)
    other_id = counterpart_id(room, user.id)
    relationship_hidden = other_id is None or await is_blocked_either(db, user.id, other_id)
    if other_id is not None:
        relationship_hidden = relationship_hidden or await has_active_restriction(db, user.id, other_id)
        relationship_hidden = relationship_hidden or await has_active_restriction(db, other_id, user.id)
    receipt_hidden = relationship_hidden or room.state == RoomState.request.value
    if cursor is None and not receipt_hidden:
        read_message_id = await advance_read_cursor(db, room, user.id)
        if read_message_id is not None and other_id is not None:
            await publish_to_user(
                redis,
                other_id,
                {
                    "type": "chat.read",
                    "payload": {
                        "room_id": str(room.id),
                        "message_id": str(read_message_id),
                    },
                },
            )
    counterpart_read_id = None if receipt_hidden else await counterpart_read_message_id(db, room, user.id)
    q = (
        select(ChatMessage, User)
        .outerjoin(User, User.id == ChatMessage.sender_id)
        .where(ChatMessage.room_id == room.id)
        .order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
        .limit(limit + 1)
    )
    # 수신자에게 pending(안전 확인 중) 메시지는 보이지 않는다 (SAFE-01)
    q = q.where(
        or_(
            ChatMessage.sender_id == user.id,
            ChatMessage.safety_status != SafetyStatus.pending.value,
        )
    )
    if cursor:
        try:
            ts_raw, id_raw = unquote(cursor).split("|", 1)
            cur_ts, cur_id = datetime.fromisoformat(ts_raw), uuid.UUID(id_raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="잘못된 커서입니다")
        q = q.where(
            or_(
                ChatMessage.created_at < cur_ts,
                (ChatMessage.created_at == cur_ts) & (ChatMessage.id < cur_id),
            )
        )
    rows = (await db.execute(q)).all()
    next_cursor = None
    if len(rows) > limit:
        rows = rows[:limit]
        last_msg = rows[-1][0]
        next_cursor = quote(f"{last_msg.created_at.isoformat()}|{last_msg.id}")
    return MessageListOut(
        items=[
            _message_out(m, user.id, sender, counterpart_read_id)
            for m, sender in rows
        ],
        next_cursor=next_cursor,
    )


@router.post("/messages/{message_id}/reveal", response_model=RevealOut)
async def reveal_message(
    message_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """SAFE-03 '내용 보기' — 열람해도 SAFE-05 집계에는 계속 포함 (SAFE-05-6)."""
    msg = await db.get(ChatMessage, message_id)
    if msg is None:
        raise HTTPException(status_code=404, detail="메시지를 찾을 수 없습니다")
    room = await db.get(ChatRoom, msg.room_id)
    if user.id not in (room.user_a, room.user_b) or msg.sender_id == user.id:
        raise HTTPException(status_code=403, detail="수신자만 내용을 볼 수 있습니다")
    if msg.safety_status != SafetyStatus.flagged.value:
        raise HTTPException(status_code=400, detail="블러 처리된 메시지가 아닙니다")
    if msg.revealed_at is None:
        msg.revealed_at = datetime.now(timezone.utc)
        await db.commit()
    return RevealOut(id=msg.id, content=msg.content or "")


@router.post("/requests/{room_id}/accept", response_model=RoomOut)
async def accept_request(
    room_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    room = await _get_my_room(db, user, room_id)
    if room.state != RoomState.request.value or room.requested_by == user.id:
        raise HTTPException(status_code=400, detail="수락할 수 없는 요청입니다")
    room.state = RoomState.active.value
    room.accepted_at = datetime.now(timezone.utc)
    await db.commit()
    return (await _rooms_out(db, redis, user, [room]))[0]


@router.post("/restrictions/{sender_id}/release", response_model=RestrictionReleaseOut)
async def release_send_restriction(
    sender_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """수신자가 대화 계속을 원할 때 직접 해제 → 누적 카운터 리셋 (SAFE-05-3/7)."""
    released = await release_restriction(db, sender_id, user)
    if not released:
        raise HTTPException(status_code=404, detail="해제할 전송 제한이 없습니다")
    return RestrictionReleaseOut(released=True)


@router.post("/rooms/{room_id}/calls", response_model=CallOut, status_code=201)
async def start_call(
    room_id: uuid.UUID,
    body: CallCreateIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """CHAT-05: 온라인 친구에게 음성·영상 WebRTC 통화 초대를 보낸다."""
    room = await _get_my_room(db, user, room_id)
    other_id, _ = await _validate_call_room(db, user, room)
    online = await online_statuses(redis, [other_id])
    if not online.get(other_id, False):
        raise HTTPException(status_code=409, detail="상대가 현재 온라인이 아닙니다")
    try:
        call = await call_signaling.create_call(
            redis,
            room_id=room.id,
            caller_id=user.id,
            callee_id=other_id,
            kind=body.kind,
        )
    except call_signaling.CallBusy:
        raise HTTPException(status_code=409, detail="이미 진행 중인 통화가 있습니다")
    try:
        await publish_to_user(
            redis,
            other_id,
            {"type": "call.invited", "payload": call_signaling.public_call(call)},
        )
    except Exception:
        await call_signaling.close_call(redis, call)
        raise
    return call_signaling.public_call(call)


@router.get("/calls/{call_id}", response_model=CallOut)
async def get_call(
    call_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    try:
        call = await call_signaling.get_call(redis, call_id, user.id)
    except call_signaling.CallNotFound:
        raise HTTPException(status_code=404, detail="통화를 찾을 수 없습니다")
    room = await _get_my_room(db, user, uuid.UUID(call["room_id"]))
    await _validate_call_room(db, user, room)
    return call_signaling.public_call(call)


@router.post("/calls/{call_id}/signals", response_model=CallSignalOut, status_code=202)
async def send_call_signal(
    call_id: uuid.UUID,
    body: CallSignalIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    encoded = json.dumps(body.data, ensure_ascii=False, separators=(",", ":")).encode()
    if len(encoded) > settings.CALL_SIGNAL_MAX_BYTES:
        raise HTTPException(status_code=413, detail="통화 시그널이 너무 큽니다")
    try:
        call = await call_signaling.get_call(redis, call_id, user.id)
    except call_signaling.CallNotFound:
        raise HTTPException(status_code=404, detail="통화를 찾을 수 없습니다")
    room = await _get_my_room(db, user, uuid.UUID(call["room_id"]))
    await _validate_call_room(db, user, room)
    try:
        call_signaling.validate_signal(call, user.id, body.type)
    except call_signaling.InvalidCallSignal:
        raise HTTPException(status_code=409, detail="현재 상태에서 보낼 수 없는 통화 시그널입니다")
    try:
        call, _terminal = await call_signaling.update_call_for_signal(redis, call, body.type)
    except call_signaling.CallNotFound:
        raise HTTPException(status_code=404, detail="통화를 찾을 수 없습니다")
    other_id = call_signaling.counterpart(call, user.id)
    await publish_to_user(
        redis,
        other_id,
        {
            "type": "call.signal",
            "payload": {
                "call_id": call["id"],
                "room_id": call["room_id"],
                "from_user_id": str(user.id),
                "signal": body.type.value,
                "data": body.data,
            },
        },
    )
    return CallSignalOut(status=call["status"])


@router.post("/rooms/{room_id}/media", response_model=MessageOut, status_code=201)
async def send_media(
    room_id: uuid.UUID,
    background: BackgroundTasks,
    file: UploadFile = File(...),
    duration_seconds: int = Form(default=0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    session_factory: async_sessionmaker = Depends(get_session_factory),
    describe_caller=Depends(ai_media.get_describe_caller),
    caption_caller=Depends(ai_media.get_caption_caller),
    video_probe=Depends(media_probe.get_video_probe),
):
    """CHAT-01: 사진·동영상은 친구 방에서만, 미성년-성인 쌍은 제한 (§4.5).

    안전 분석 없이 즉시 전달(SAFE-02)하고 설명(VISION-01)·자막(CAPTION-01)을 비동기 부착.
    """
    room = await _get_my_room(db, user, room_id)
    other_id = counterpart_id(room, user.id)
    if other_id is None:
        raise HTTPException(status_code=403, detail=RESTRICTED)
    if room.state != RoomState.active.value or not await are_friends(db, user.id, other_id):
        raise HTTPException(status_code=403, detail="사진·동영상은 친구와의 채팅에서만 보낼 수 있습니다")
    if await is_blocked_either(db, user.id, other_id):
        raise HTTPException(status_code=403, detail=RESTRICTED)
    if await has_active_restriction(db, user.id, other_id):
        raise HTTPException(status_code=403, detail=RESTRICTED)

    other = await db.get(User, other_id)
    if is_minor(user.birth_date) != is_minor(other.birth_date):
        # 미성년-성인 채팅은 텍스트만 (§4.5 미디어 전송 제한)
        raise HTTPException(status_code=403, detail="이 채팅에서는 사진·동영상을 보낼 수 없습니다")

    if file.content_type in ALLOWED_CONTENT_TYPES:
        data = await file.read()
        media_type = MediaType.image.value
        if len(data) > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"이미지는 {settings.MAX_UPLOAD_MB}MB 이하만 가능합니다")
        url = await save_upload(data, file.content_type)
        media_hash = ai_media.media_hash_of(data)
    elif file.content_type in ALLOWED_VIDEO_TYPES:
        media_type = MediaType.video.value
        if duration_seconds <= 0 or duration_seconds > settings.MAX_VIDEO_SECONDS:
            raise HTTPException(
                status_code=400,
                detail=f"영상 길이는 1초 이상 {settings.MAX_VIDEO_SECONDS // 60}분 이하여야 합니다",
            )
        try:
            saved = await save_upload_stream(
                file,
                file.content_type,
                max_bytes=settings.MAX_VIDEO_MB * 1024 * 1024,
            )
        except UploadTooLarge:
            raise HTTPException(status_code=413, detail=f"영상은 {settings.MAX_VIDEO_MB}MB 이하만 가능합니다")
        try:
            actual_duration = await video_probe(saved.path, file.content_type)
        except media_probe.InvalidVideo as exc:
            delete_upload(saved.url)
            raise HTTPException(status_code=400, detail=str(exc))
        if actual_duration > settings.MAX_VIDEO_SECONDS:
            delete_upload(saved.url)
            raise HTTPException(
                status_code=400,
                detail=f"영상은 최대 {settings.MAX_VIDEO_SECONDS // 60}분까지 보낼 수 있습니다",
            )
        quota_result = await consume_caption(redis, user.id)
        if quota_result == CAPTION_USER_LIMIT:
            delete_upload(saved.url)
            limit = caption_key(user.id)[1]
            raise HTTPException(
                status_code=429, detail=f"영상 업로드는 하루 {limit}회까지 가능합니다 (게시물·채팅 합산)"
            )
        if quota_result == CAPTION_GLOBAL_LIMIT:
            delete_upload(saved.url)
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "STT_DAILY_BUDGET_EXCEEDED",
                    "message": "오늘의 자막 생성 한도가 소진되었습니다. 내일 다시 시도해 주세요.",
                },
            )
        url = saved.url
        media_hash = saved.media_hash
    else:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다")

    message = ChatMessage(
        id=uuid.uuid4(),
        room_id=room.id,
        sender_id=user.id,
        type=media_type,
        media_url=url,
        # 사진·동영상은 안전 분석 대상이 아님(SAFE-02) — 재분석 잡은 type=text만 다룬다
        safety_status=SafetyStatus.unanalyzed.value,
        available_at=datetime.now(timezone.utc),
        description_status=(
            AiStatus.processing.value if media_type == MediaType.image.value else AiStatus.none.value
        ),
        caption_status=(
            AiStatus.processing.value if media_type == MediaType.video.value else AiStatus.none.value
        ),
    )
    db.add(message)
    await db.commit()

    if media_type == MediaType.image.value:
        background.add_task(
            ai_media.describe_chat_message_job, session_factory, redis, message.id, media_hash,
            user.id, describe_caller,
        )
    else:
        background.add_task(
            ai_media.caption_chat_message_job, session_factory, redis, message.id, media_hash,
            user.id, caption_caller,
        )
    await publish_to_user(
        redis, other_id,
        {"type": "chat.message", "payload": {"room_id": str(room.id), "message_id": str(message.id)}},
    )
    return _message_out(message, user.id, user)
