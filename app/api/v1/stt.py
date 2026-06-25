import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.stt import STTResponse
from app.services import stt

router = APIRouter(prefix="/stt", tags=["stt"])

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/webm",
    "audio/mp4",
    "audio/m4a",
    "audio/x-m4a",
    "audio/ogg",
}

# 음성 댓글은 보통 1회성 고유 오디오 → 캐싱 미적용(필요 시 내용 해시 캐싱 추가 가능)


@router.post("/transcribe", response_model=STTResponse)
async def transcribe(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"지원 형식: {', '.join(sorted(ALLOWED_AUDIO_TYPES))}",
        )

    max_bytes = settings.MAX_AUDIO_MB * 1024 * 1024
    data = await file.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"오디오가 {settings.MAX_AUDIO_MB} MB 제한을 초과합니다",
        )

    started = time.perf_counter()
    text = await stt.transcribe(data, file.filename or "audio", file.content_type)
    duration_ms = int((time.perf_counter() - started) * 1000)
    return STTResponse(text=text, duration_ms=duration_ms)
