import uuid
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, StringConstraints, model_validator

from app.core.enums import CallKind, CallSignalType
from app.schemas.post import AuthorOut
from app.schemas.common import StrictRequest

ChatContent = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2_000)
]


class RoomCreateIn(StrictRequest):
    user_id: uuid.UUID


class RoomMessagePreviewOut(BaseModel):
    id: uuid.UUID
    type: str
    content: str | None
    mine: bool
    blurred: bool = False
    created_at: datetime


class RoomOut(BaseModel):
    id: uuid.UUID
    state: str
    counterpart: AuthorOut
    requested_by: uuid.UUID | None
    # SAFE-05: 상대(발신자)가 나에게 전송 제한된 상태 — 수신자에게만 의미 있음
    restricted_sender: bool = False
    accepted_at: datetime | None
    created_at: datetime
    unread_count: int = 0
    last_message: RoomMessagePreviewOut | None = None
    last_activity_at: datetime
    counterpart_online: bool = False


class RoomListOut(BaseModel):
    items: list[RoomOut]
    unread_total: int = 0


class MessageIn(StrictRequest):
    content: ChatContent


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
    is_read: bool = False


class MessageListOut(BaseModel):
    items: list[MessageOut]
    next_cursor: str | None = None


class RevealOut(BaseModel):
    id: uuid.UUID
    content: str


class CallCreateIn(StrictRequest):
    kind: CallKind


class CallOut(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    caller_id: uuid.UUID
    callee_id: uuid.UUID
    kind: CallKind
    status: str
    created_at: datetime
    expires_at: datetime


class CallSignalIn(StrictRequest):
    type: CallSignalType
    data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_data(self):
        data_required = self.type in {
            CallSignalType.offer,
            CallSignalType.answer,
            CallSignalType.ice,
        }
        if data_required and not self.data:
            raise ValueError(f"{self.type.value} 시그널에는 data가 필요합니다")
        if not data_required and self.data is not None:
            raise ValueError(f"{self.type.value} 시그널에는 data를 보낼 수 없습니다")
        return self


class CallSignalOut(BaseModel):
    accepted: bool = True
    status: str
