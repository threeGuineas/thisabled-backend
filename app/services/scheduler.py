"""APScheduler 크론 — 드래프트 청소·자막 작업 복구·SAFE 재분석."""

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.core.config import settings
from app.core.enums import AiStatus, MediaType, PostStatus
from app.models import ChatMessage, Post, PostMedia
from app.services import ai_media
from app.services.ai_media import file_path_from_url

_scheduler: AsyncIOScheduler | None = None
logger = logging.getLogger(__name__)


async def cleanup_stale_drafts(session_factory=None) -> int:
    """CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제.

    이미 성공한 자막 생성의 일일 횟수 차감은 복원하지 않는다.
    """
    if session_factory is None:
        from app.db.session import AsyncSessionLocal

        session_factory = AsyncSessionLocal

    cutoff = datetime.now(timezone.utc) - timedelta(hours=settings.DRAFT_TTL_HOURS)
    deleted = 0
    async with session_factory() as db:
        stale = (
            await db.execute(
                select(Post).where(
                    Post.status == PostStatus.processing.value, Post.created_at < cutoff
                )
            )
        ).scalars().all()
        for post in stale:
            media_rows = (
                await db.execute(select(PostMedia).where(PostMedia.post_id == post.id))
            ).scalars().all()
            for m in media_rows:
                try:
                    file_path_from_url(m.url).unlink(missing_ok=True)
                except OSError:
                    pass
            await db.delete(post)  # post_media는 FK CASCADE
            deleted += 1
        await db.commit()
    return deleted


async def _reanalyze_job() -> None:
    """§18.3: 모델 복구 감지용 주기 재분석 (unanalyzed·pending 텍스트)."""
    from app.db.redis import get_redis_client
    from app.db.session import AsyncSessionLocal
    from app.services.chat import reanalyze_unanalyzed
    from app.services.safety import SafetyClient

    await reanalyze_unanalyzed(AsyncSessionLocal, get_redis_client(), SafetyClient())


async def recover_processing_captions(
    session_factory=None,
    redis=None,
    caller=None,
) -> int:
    """재시작 등으로 유실된 processing 자막 작업을 Redis 잠금 아래 재실행한다."""
    if session_factory is None:
        from app.db.session import AsyncSessionLocal

        session_factory = AsyncSessionLocal
    if redis is None:
        from app.db.redis import get_redis_client

        redis = get_redis_client()
    if caller is None:
        caller = ai_media.get_caption_caller()

    jobs = []
    async with session_factory() as db:
        post_media = (
            await db.execute(
                select(PostMedia).where(
                    PostMedia.media_type == MediaType.video.value,
                    PostMedia.caption_status == AiStatus.processing.value,
                    PostMedia.uploader_id.is_not(None),
                )
            )
        ).scalars().all()
        chat_messages = (
            await db.execute(
                select(ChatMessage).where(
                    ChatMessage.type == MediaType.video.value,
                    ChatMessage.caption_status == AiStatus.processing.value,
                    ChatMessage.sender_id.is_not(None),
                )
            )
        ).scalars().all()

        for media in post_media:
            jobs.append(
                ai_media.caption_post_media_job(
                    session_factory, redis, media.id, media.uploader_id, caller
                )
            )
        for message in chat_messages:
            if message.media_url is None:
                continue
            path = file_path_from_url(message.media_url)
            media_hash = ai_media.media_hash_from_path(path) if path.is_file() else "missing"
            jobs.append(
                ai_media.caption_chat_message_job(
                    session_factory,
                    redis,
                    message.id,
                    media_hash,
                    message.sender_id,
                    caller,
                )
            )

    if jobs:
        results = await asyncio.gather(*jobs, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(
                    "caption recovery job failed",
                    exc_info=(type(result), result, result.__traceback__),
                )
    return len(jobs)


def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler(timezone="UTC")
        _scheduler.add_job(cleanup_stale_drafts, "interval", hours=1, id="cleanup_stale_drafts")
        _scheduler.add_job(
            recover_processing_captions,
            "interval",
            minutes=1,
            id="recover_processing_captions",
            next_run_time=datetime.now(timezone.utc),
            max_instances=1,
            coalesce=True,
        )
        _scheduler.add_job(_reanalyze_job, "interval", minutes=10, id="reanalyze_unanalyzed")
        _scheduler.start()
    return _scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
