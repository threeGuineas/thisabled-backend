"""APScheduler 인프로세스 크론 — 24h 드래프트 청소 (+ Task 11에서 미분석 재분석 추가)."""

from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.core.config import settings
from app.core.enums import PostStatus
from app.models import Post, PostMedia
from app.services.ai_media import file_path_from_url

_scheduler: AsyncIOScheduler | None = None


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


def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler(timezone="UTC")
        _scheduler.add_job(cleanup_stale_drafts, "interval", hours=1, id="cleanup_stale_drafts")
        _scheduler.add_job(_reanalyze_job, "interval", minutes=10, id="reanalyze_unanalyzed")
        _scheduler.start()
    return _scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
