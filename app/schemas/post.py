import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AuthorOut(BaseModel):
    """author_id가 None이면 '탈퇴한 사용자' (§15)."""

    id: uuid.UUID | None
    nickname: str
    profile_image_url: str | None = None


class MediaOut(BaseModel):
    id: uuid.UUID
    media_type: str
    url: str
    sort_order: int
    description: str | None = None
    description_status: str
    caption: list | None = None
    caption_status: str


class PostOut(BaseModel):
    id: uuid.UUID
    author: AuthorOut
    content: str
    status: str
    media: list[MediaOut]
    like_count: int
    comment_count: int
    liked_by_me: bool
    published_at: datetime | None
    created_at: datetime


class FeedOut(BaseModel):
    items: list[PostOut]
    next_cursor: str | None = None


class PostCreateIn(BaseModel):
    content: str = Field(min_length=1)
    media_ids: list[uuid.UUID] = []


class PostPatchIn(BaseModel):
    content: str = Field(min_length=1)


class LikeOut(BaseModel):
    post_id: uuid.UUID
    liked: bool
    like_count: int


class CommentOut(BaseModel):
    id: uuid.UUID
    post_id: uuid.UUID
    author: AuthorOut
    content: str
    created_at: datetime
    updated_at: datetime | None


class CommentListOut(BaseModel):
    items: list[CommentOut]


class CommentIn(BaseModel):
    content: str = Field(min_length=1)
