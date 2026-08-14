import uuid

from pydantic import BaseModel

from app.schemas.common import StrictRequest

from app.core.enums import PostCategory
from app.schemas.post import PostContent, PostTitle


class UploadedMediaOut(BaseModel):
    media_id: uuid.UUID
    url: str


class ImageUploadOut(BaseModel):
    items: list[UploadedMediaOut]


class VideoUploadOut(BaseModel):
    """영상 업로드 = 내부 드래프트 생성 (POST-01). post_id로 자막 상태 폴링·게시."""

    post_id: uuid.UUID
    media_id: uuid.UUID
    caption_status: str


class CaptionStatusOut(BaseModel):
    caption_status: str


class TranscribeOut(BaseModel):
    text: str


class PublishIn(StrictRequest):
    """자막 실패(재시도 소진) 시 '자막 없이 게시' 명시 선택 (CAPTION-01 예외)."""

    title: PostTitle
    category: PostCategory
    content: PostContent
    allow_no_caption: bool = False
