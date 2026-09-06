"""Cloud Tasks/Scheduler 전용 비공개 Cloud Run worker 애플리케이션."""

import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings
from app.db.redis import close_redis_client, get_redis_client
from app.db.session import get_session_factory
from app.services import ai_media
from app.services.scheduler import cleanup_stale_drafts, recover_processing_captions
from app.services.chat import reanalyze_unanalyzed
from app.services.safety import SafetyClient
from app.services.task_queue import AiTaskKind


class AiTaskIn(BaseModel):
    kind: AiTaskKind
    entity_id: uuid.UUID
    user_id: uuid.UUID
    media_hash: str | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    try:
        yield
    finally:
        await close_redis_client()


app = FastAPI(
    title="ThisAbled private worker",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)


@app.post("/tasks/ai-media", status_code=204)
async def run_ai_media_task(body: AiTaskIn) -> None:
    session_factory = get_session_factory()
    redis = get_redis_client()
    if body.kind == AiTaskKind.describe_post:
        await ai_media.describe_post_media_job(
            session_factory, redis, body.entity_id, body.user_id, ai_media.get_describe_caller()
        )
    elif body.kind == AiTaskKind.describe_chat:
        await ai_media.describe_chat_message_job(
            session_factory,
            redis,
            body.entity_id,
            body.media_hash or "",
            body.user_id,
            ai_media.get_describe_caller(),
        )
    elif body.kind == AiTaskKind.caption_post:
        await ai_media.caption_post_media_job(
            session_factory, redis, body.entity_id, body.user_id, ai_media.get_caption_caller()
        )
    else:
        await ai_media.caption_chat_message_job(
            session_factory,
            redis,
            body.entity_id,
            body.media_hash or "",
            body.user_id,
            ai_media.get_caption_caller(),
        )


@app.post("/tasks/maintenance", status_code=204)
async def run_maintenance() -> None:
    session_factory = get_session_factory()
    redis = get_redis_client()
    await cleanup_stale_drafts(session_factory=session_factory)
    await recover_processing_captions(session_factory=session_factory, redis=redis)
    await reanalyze_unanalyzed(session_factory, redis, SafetyClient())


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}
