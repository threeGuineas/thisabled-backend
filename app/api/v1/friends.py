"""FRIEND-01 친구 요청 · FRIEND-02 친구 관리."""

import uuid
from datetime import datetime, timezone
from typing import Literal

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.enums import RequestStatus
from app.core.pairs import normalize_pair
from app.db.redis import get_redis
from app.db.session import get_db
from app.services import notify as noti
from app.models import FriendRequest, Friendship, User
from app.schemas.post import AuthorOut
from app.schemas.social import (
    FriendListOut,
    FriendRequestIn,
    FriendRequestListOut,
    FriendRequestOut,
)
from app.services.relations import are_friends, is_blocked_either

router = APIRouter(prefix="/friends", tags=["friends"])

UNAVAILABLE = "요청을 보낼 수 없는 상대입니다"  # 차단·정책 사유 비노출 (CHAT-02 원칙 공유)


def _author(u: User | None) -> AuthorOut:
    if u is None:
        return AuthorOut(id=None, nickname="탈퇴한 사용자")
    return AuthorOut(id=u.id, nickname=u.nickname, profile_image_url=u.profile_image_url)


async def _request_out(db: AsyncSession, req: FriendRequest) -> FriendRequestOut:
    sender = await db.get(User, req.sender_id)
    receiver = await db.get(User, req.receiver_id)
    return FriendRequestOut(
        id=req.id, sender=_author(sender), receiver=_author(receiver),
        status=req.status, created_at=req.created_at, responded_at=req.responded_at,
    )


@router.post("/requests", response_model=FriendRequestOut, status_code=201)
async def send_request(
    body: FriendRequestIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    if body.receiver_id == user.id:
        raise HTTPException(status_code=400, detail="자기 자신에게는 요청할 수 없습니다")
    receiver = await db.get(User, body.receiver_id)
    if receiver is None or await is_blocked_either(db, user.id, body.receiver_id):
        raise HTTPException(status_code=404, detail=UNAVAILABLE)
    if await are_friends(db, user.id, body.receiver_id):
        raise HTTPException(status_code=400, detail="이미 친구입니다")
    pending = (
        await db.execute(
            select(FriendRequest.id).where(
                FriendRequest.status == RequestStatus.pending.value,
                or_(
                    (FriendRequest.sender_id == user.id)
                    & (FriendRequest.receiver_id == body.receiver_id),
                    (FriendRequest.sender_id == body.receiver_id)
                    & (FriendRequest.receiver_id == user.id),
                ),
            )
        )
    ).first()
    if pending is not None:
        raise HTTPException(status_code=400, detail="처리 중인 친구 요청이 있습니다")

    req = FriendRequest(id=uuid.uuid4(), sender_id=user.id, receiver_id=body.receiver_id)
    db.add(req)
    await db.commit()
    await noti.notify(
        db, redis, body.receiver_id, noti.FRIEND_REQUEST,
        {"request_id": str(req.id), "sender_nickname": user.nickname},
    )
    return await _request_out(db, req)


@router.get("/requests", response_model=FriendRequestListOut)
async def list_requests(
    box: Literal["received", "sent"] = Query(default="received"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cond = (
        FriendRequest.receiver_id == user.id
        if box == "received"
        else FriendRequest.sender_id == user.id
    )
    rows = (
        await db.execute(
            select(FriendRequest)
            .where(cond, FriendRequest.status == RequestStatus.pending.value)
            .order_by(FriendRequest.created_at.desc())
        )
    ).scalars().all()
    return FriendRequestListOut(items=[await _request_out(db, r) for r in rows])


async def _get_pending(db: AsyncSession, req_id: uuid.UUID) -> FriendRequest:
    req = await db.get(FriendRequest, req_id)
    if req is None or req.status != RequestStatus.pending.value:
        raise HTTPException(status_code=404, detail="처리할 수 없는 요청입니다")
    return req


@router.post("/requests/{request_id}/accept", response_model=FriendRequestOut)
async def accept_request(
    request_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    req = await _get_pending(db, request_id)
    if req.receiver_id != user.id:
        raise HTTPException(status_code=403, detail="수신자만 수락할 수 있습니다")
    req.status = RequestStatus.accepted.value
    req.responded_at = datetime.now(timezone.utc)
    ua, ub = normalize_pair(req.sender_id, req.receiver_id)
    if not await are_friends(db, ua, ub):
        db.add(Friendship(user_a=ua, user_b=ub))
    await db.commit()
    await noti.notify(
        db, redis, req.sender_id, noti.FRIEND_ACCEPTED,
        {"request_id": str(req.id), "receiver_nickname": user.nickname},
    )
    return await _request_out(db, req)


@router.post("/requests/{request_id}/decline", response_model=FriendRequestOut)
async def decline_request(
    request_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    req = await _get_pending(db, request_id)
    if req.receiver_id != user.id:
        raise HTTPException(status_code=403, detail="수신자만 거절할 수 있습니다")
    req.status = RequestStatus.declined.value
    req.responded_at = datetime.now(timezone.utc)  # 거절 후 30일 추천 제외 (MATCH-03)
    await db.commit()
    return await _request_out(db, req)


@router.post("/requests/{request_id}/cancel", response_model=FriendRequestOut)
async def cancel_request(
    request_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    req = await _get_pending(db, request_id)
    if req.sender_id != user.id:
        raise HTTPException(status_code=403, detail="요청자만 취소할 수 있습니다")
    req.status = RequestStatus.cancelled.value
    req.responded_at = datetime.now(timezone.utc)
    await db.commit()
    return await _request_out(db, req)


@router.get("", response_model=FriendListOut)
async def list_friends(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            select(Friendship).where(
                or_(Friendship.user_a == user.id, Friendship.user_b == user.id)
            )
        )
    ).scalars().all()
    friend_ids = [f.user_b if f.user_a == user.id else f.user_a for f in rows]
    friends = (
        (await db.execute(select(User).where(User.id.in_(friend_ids)))).scalars().all()
        if friend_ids
        else []
    )
    return FriendListOut(items=[_author(u) for u in friends])


@router.delete("/{user_id}", status_code=204)
async def unfriend(
    user_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ua, ub = normalize_pair(user.id, user_id)
    await db.execute(delete(Friendship).where(Friendship.user_a == ua, Friendship.user_b == ub))
    await db.commit()
