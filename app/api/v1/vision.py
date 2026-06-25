import hashlib
import time
from pathlib import Path

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.deps import get_current_user
from app.db.redis import get_redis
from app.models.user import User
from app.schemas.vision import VisionRequest, VisionResponse
from app.services import vision

router = APIRouter(prefix="/vision", tags=["vision"])

_CACHE_PREFIX = "vision:desc:"
_EXT_CONTENT_TYPE = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _resolve_upload_path(image_url: str) -> Path:
    """/uploads/<name> → 로컬 파일 경로. 경로 탈출 방지(basename만 사용)."""
    if not image_url.startswith("/uploads/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="image_url 은 /uploads/ 로 시작하는 업로드 경로여야 합니다",
        )
    name = Path(image_url).name
    path = Path(settings.UPLOAD_DIR) / name
    if not name or path.parent != Path(settings.UPLOAD_DIR):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 경로")
    return path


@router.post("/describe", response_model=VisionResponse)
async def describe_image(
    body: VisionRequest,
    redis: aioredis.Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    path = _resolve_upload_path(body.image_url)
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="이미지를 찾을 수 없습니다")

    image_bytes = path.read_bytes()
    content_hash = hashlib.sha256(image_bytes).hexdigest()
    cache_key = f"{_CACHE_PREFIX}{content_hash}"

    cached = await redis.get(cache_key)
    if cached is not None:
        return VisionResponse(description=cached, duration_ms=0, cached=True)

    content_type = _EXT_CONTENT_TYPE.get(path.suffix.lower(), "image/png")
    started = time.perf_counter()
    description = await vision.generate_description(image_bytes, content_type)
    duration_ms = int((time.perf_counter() - started) * 1000)

    await redis.set(cache_key, description, ex=settings.VISION_CACHE_TTL_SECONDS)
    return VisionResponse(description=description, duration_ms=duration_ms, cached=False)
