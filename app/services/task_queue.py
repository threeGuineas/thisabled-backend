"""AI 미디어 작업을 로컬 BackgroundTasks 또는 Cloud Tasks로 전달한다."""

import json
import logging
from enum import StrEnum

from fastapi import BackgroundTasks

from app.core.config import settings

logger = logging.getLogger(__name__)


class AiTaskKind(StrEnum):
    describe_post = "describe_post"
    describe_chat = "describe_chat"
    caption_post = "caption_post"
    caption_chat = "caption_chat"


async def _create_cloud_task(payload: dict) -> None:
    if not all(
        (
            settings.GCP_PROJECT_ID,
            settings.TASK_WORKER_URL,
            settings.TASK_OIDC_SERVICE_ACCOUNT,
        )
    ):
        raise RuntimeError("Cloud Tasks 설정이 완전하지 않습니다")

    from google.cloud import tasks_v2

    client = tasks_v2.CloudTasksAsyncClient()
    parent = client.queue_path(
        settings.GCP_PROJECT_ID,
        settings.GCP_REGION,
        settings.CLOUD_TASKS_QUEUE,
    )
    await client.create_task(
        request={
            "parent": parent,
            "task": {
                "http_request": {
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": f"{settings.TASK_WORKER_URL.rstrip('/')}/tasks/ai-media",
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(payload).encode(),
                    "oidc_token": {
                        "service_account_email": settings.TASK_OIDC_SERVICE_ACCOUNT,
                        "audience": settings.TASK_WORKER_URL,
                    },
                }
            },
        }
    )


async def enqueue_ai_task(
    background: BackgroundTasks,
    *,
    kind: AiTaskKind,
    entity_id,
    user_id,
    local_callable,
    local_args: tuple,
    media_hash: str | None = None,
) -> None:
    """운영 큐 장애 시 기존 로컬 실행으로 폴백해 작업 유실을 줄인다."""
    if settings.CLOUD_TASKS_ENABLED:
        payload = {
            "kind": kind.value,
            "entity_id": str(entity_id),
            "user_id": str(user_id),
            "media_hash": media_hash,
        }
        try:
            await _create_cloud_task(payload)
            return
        except Exception:
            logger.exception("Cloud Tasks enqueue failed; falling back to local background task")
    background.add_task(local_callable, *local_args)
