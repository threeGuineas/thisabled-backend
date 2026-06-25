from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.core.deps import get_current_user
from app.core.config import settings
from app.core.storage import ALLOWED_CONTENT_TYPES, save_upload
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["upload"])

MAX_BYTES = settings.MAX_UPLOAD_MB * 1024 * 1024


class UploadResponse(BaseModel):
    url: str


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="이미지 업로드",
    description=f"multipart `file`. 최대 {settings.MAX_UPLOAD_MB}MB, jpg·png·gif·webp. "
    "응답 `url`을 게시글 `image_url` 또는 Vision `image_url`에 그대로 사용.",
)
async def upload_image(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}",
        )

    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_UPLOAD_MB} MB limit",
        )

    url = await save_upload(data, file.content_type)
    return UploadResponse(url=url)
