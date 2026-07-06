"""COMM-01~05 — AI 소통 코치. 전 모드 제공, 발달 모드 기본 노출(§14)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.enums import MessageType, SafetyStatus
from app.db.session import get_db
from app.models import ChatMessage, ChatRoom, User
from app.services.comm import get_comm_client

router = APIRouter(prefix="/comm", tags=["comm"])


class TextIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class SimplifyOut(BaseModel):
    result: str
    original: str  # COMM-01: 변환 결과와 원문 전환 제공


class SuggestionsOut(BaseModel):
    suggestions: list[str]


class RoomIn(BaseModel):
    room_id: uuid.UUID


class HintsOut(BaseModel):
    hints: list[str]


async def _recent_context(db: AsyncSession, user: User, room_id: uuid.UUID) -> list[str]:
    """COMM-05: 참여자 검증 후 최근 N개 텍스트. flagged 미열람·pending은 제외."""
    room = await db.get(ChatRoom, room_id)
    if room is None or user.id not in (room.user_a, room.user_b):
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")
    rows = (
        await db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.room_id == room_id,
                ChatMessage.type == MessageType.text.value,
                ChatMessage.safety_status != SafetyStatus.pending.value,
                or_(
                    ChatMessage.safety_status != SafetyStatus.flagged.value,
                    ChatMessage.revealed_at.is_not(None),
                ),
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(settings.COMM_CONTEXT_MESSAGES)
        )
    ).scalars().all()
    return [m.content for m in reversed(rows) if m.content]


@router.post("/simplify", response_model=SimplifyOut)
async def simplify(
    body: TextIn,
    user: User = Depends(get_current_user),
    comm=Depends(get_comm_client),
):
    return SimplifyOut(result=await comm.simplify(body.text), original=body.text)


@router.post("/complete", response_model=SuggestionsOut)
async def complete(
    body: TextIn,
    user: User = Depends(get_current_user),
    comm=Depends(get_comm_client),
):
    """COMM-02: 제안일 뿐, 자동 입력·게시하지 않는다 (§20-8)."""
    return SuggestionsOut(suggestions=await comm.complete(body.text))


@router.post("/replies", response_model=SuggestionsOut)
async def suggest_replies(
    body: RoomIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    comm=Depends(get_comm_client),
):
    context = await _recent_context(db, user, body.room_id)
    return SuggestionsOut(suggestions=await comm.suggest_replies(context))


@router.post("/hints", response_model=HintsOut)
async def hints(
    body: RoomIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    comm=Depends(get_comm_client),
):
    context = await _recent_context(db, user, body.room_id)
    return HintsOut(hints=await comm.hints(context))
