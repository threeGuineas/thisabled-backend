import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, model_validator

from app.core.enums import PostCategory
from app.schemas.common import StrictRequest

PostTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
PostContent = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=10_000)
]
CommentContent = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2_000)
]


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
    caption_failure_code: str | None = None
    caption_failure_message: str | None = None
    caption_retryable: bool = False


class PostOut(BaseModel):
    id: uuid.UUID
    author: AuthorOut
    title: str | None
    category: PostCategory | None
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


class PostCreateIn(StrictRequest):
    title: PostTitle | None = None
    category: PostCategory
    content: PostContent
    media_ids: list[uuid.UUID] = Field(default_factory=list, max_length=3)


class PostPatchIn(StrictRequest):
    title: PostTitle | None = None
    category: PostCategory | None = None
    content: PostContent | None = None

    @model_validator(mode="after")
    def require_change(self):
        if self.title is None and self.category is None and self.content is None:
            raise ValueError("수정할 필드를 하나 이상 보내야 합니다")
        return self


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


class CommentIn(StrictRequest):
    content: CommentContent
