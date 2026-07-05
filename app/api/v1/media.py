"""미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력."""

import uuid
from datetime import datetime, timezone

import redis.asyncio as aioredis
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.enums import AiStatus, MediaType, PostStatus
from app.core.storage import ALLOWED_CONTENT_TYPES, save_upload
from app.db.redis import get_redis
from app.db.session import get_db, get_session_factory
from app.models import Post, PostMedia, User
from app.schemas.media import ImageUploadOut, TranscribeOut, UploadedMediaOut, VideoUploadOut
from app.services import ai_media
from app.services.quota import caption_key, try_consume

router = APIRouter(prefix="/media", tags=["media"])

MAX_IMAGES = 3  # POST-01

ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}


@router.post("/images", response_model=ImageUploadOut, status_code=201)
async def upload_images(
    files: list[UploadFile] = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다."""
    if len(files) > MAX_IMAGES:
        raise HTTPException(status_code=400, detail=f"사진은 최대 {MAX_IMAGES}장까지 업로드할 수 있습니다")
    items: list[UploadedMediaOut] = []
    for f in files:
        if f.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="지원하지 않는 이미지 형식입니다")
        data = await f.read()
        if len(data) > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"이미지는 {settings.MAX_UPLOAD_MB}MB 이하만 가능합니다")
        url = await save_upload(data, f.content_type)
        media = PostMedia(
            id=uuid.uuid4(),
            uploader_id=user.id,
            media_type=MediaType.image.value,
            url=url,
            media_hash=ai_media.media_hash_of(data),
        )
        db.add(media)
        items.append(UploadedMediaOut(media_id=media.id, url=url))
    await db.commit()
    return ImageUploadOut(items=items)


@router.post("/videos", response_model=VideoUploadOut, status_code=201)
async def upload_video(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    duration_seconds: int = Form(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    session_factory: async_sessionmaker = Depends(get_session_factory),
    caption_caller=Depends(ai_media.get_caption_caller),
):
    """영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01).

    길이(≤3분)는 FE가 측정해 신고(서버에 ffprobe 없음), 크기(≤200MB)는 서버 실검증.
    업로드 = 일일 자막 횟수 1회 차감, 실패(재시도 소진) 시 복원.
    """
    if duration_seconds > settings.MAX_VIDEO_SECONDS:
        raise HTTPException(
            status_code=400, detail=f"영상은 최대 {settings.MAX_VIDEO_SECONDS // 60}분까지 올릴 수 있습니다"
        )
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="지원하지 않는 영상 형식입니다")
    data = await file.read()
    if len(data) > settings.MAX_VIDEO_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"영상은 {settings.MAX_VIDEO_MB}MB 이하만 가능합니다")

    key, limit, ttl = caption_key(user.id)
    if not await try_consume(redis, key, limit, ttl):
        raise HTTPException(
            status_code=429, detail=f"영상 업로드는 하루 {limit}회까지 가능합니다 (게시물·채팅 합산)"
        )

    url = await save_upload(data, file.content_type)
    post = Post(id=uuid.uuid4(), author_id=user.id, content="", status=PostStatus.processing.value)
    db.add(post)
    await db.flush()
    media = PostMedia(
        id=uuid.uuid4(),
        post_id=post.id,
        uploader_id=user.id,
        media_type=MediaType.video.value,
        url=url,
        media_hash=ai_media.media_hash_of(data),
        caption_status=AiStatus.processing.value,
    )
    db.add(media)
    await db.commit()

    background.add_task(
        ai_media.caption_post_media_job, session_factory, redis, media.id, user.id, caption_caller
    )
    return VideoUploadOut(post_id=post.id, media_id=media.id, caption_status=media.caption_status)


@router.post("/transcribe", response_model=TranscribeOut)
async def transcribe_voice(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    transcriber=Depends(ai_media.get_text_transcriber),
):
    """VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)."""
    data = await file.read()
    if len(data) > settings.MAX_AUDIO_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"음성 파일은 {settings.MAX_AUDIO_MB}MB 이하만 가능합니다")
    try:
        text = await transcriber(data, file.filename or "voice.webm", file.content_type or "audio/webm")
    except Exception:
        raise HTTPException(status_code=502, detail="음성 변환에 실패했습니다. 다시 말하기를 시도해 주세요")
    return TranscribeOut(text=text)
