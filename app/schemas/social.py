import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.post import AuthorOut


class FriendRequestIn(BaseModel):
    receiver_id: uuid.UUID


class FriendRequestOut(BaseModel):
    id: uuid.UUID
    sender: AuthorOut
    receiver: AuthorOut
    status: str
    created_at: datetime
    responded_at: datetime | None


class FriendRequestListOut(BaseModel):
    items: list[FriendRequestOut]


class FriendListOut(BaseModel):
    items: list[AuthorOut]


class BlockIn(BaseModel):
    user_id: uuid.UUID


class BlockListOut(BaseModel):
    items: list[AuthorOut]
