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


@router.post("", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
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
