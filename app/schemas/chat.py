import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.post import AuthorOut


class RoomCreateIn(BaseModel):
    user_id: uuid.UUID


class RoomOut(BaseModel):
    id: uuid.UUID
    state: str
    counterpart: AuthorOut
    requested_by: uuid.UUID | None
    # SAFE-05: 상대(발신자)가 나에게 전송 제한된 상태 — 수신자에게만 의미 있음
    restricted_sender: bool = False
    accepted_at: datetime | None
    created_at: datetime


class RoomListOut(BaseModel):
    items: list[RoomOut]


class MessageIn(BaseModel):
    content: str = Field(min_length=1)


class MessageOut(BaseModel):
    """수신자 관점: flagged & 미열람 → content=None, blurred=True (SAFE-03).

    발신자 관점: 원문 유지, safety_status=None (판정 비노출).
    """

    id: uuid.UUID
    room_id: uuid.UUID
    sender: AuthorOut
    mine: bool
    type: str
    content: str | None
    blurred: bool = False
    safety_status: str | None = None
    media_url: str | None = None
    description: str | None = None
    description_status: str = "none"
    caption: list | None = None
    caption_status: str = "none"
    created_at: datetime


class MessageListOut(BaseModel):
    items: list[MessageOut]
    next_cursor: str | None = None


class RevealOut(BaseModel):
    id: uuid.UUID
    content: str
