"""Cloud Tasks 전달과 비공개 worker 디스패치 회귀 테스트."""

import uuid

from fastapi import BackgroundTasks

from app.core.config import settings
from app.services import task_queue
from app.services.task_queue import AiTaskKind


async def _local_job(*_args):
    return None


async def test_cloud_task_mode_enqueues_without_local_background(monkeypatch):
    captured = []

    async def create(payload):
        captured.append(payload)

    monkeypatch.setattr(settings, "CLOUD_TASKS_ENABLED", True)
    monkeypatch.setattr(task_queue, "_create_cloud_task", create)
    background = BackgroundTasks()
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()

    await task_queue.enqueue_ai_task(
        background,
        kind=AiTaskKind.caption_post,
        entity_id=entity_id,
        user_id=user_id,
        local_callable=_local_job,
        local_args=("local",),
    )

    assert background.tasks == []
    assert captured == [
        {
            "kind": "caption_post",
            "entity_id": str(entity_id),
            "user_id": str(user_id),
            "media_hash": None,
        }
    ]


async def test_cloud_task_enqueue_failure_falls_back_to_local(monkeypatch):
    async def fail(_payload):
        raise RuntimeError("queue unavailable")

    monkeypatch.setattr(settings, "CLOUD_TASKS_ENABLED", True)
    monkeypatch.setattr(task_queue, "_create_cloud_task", fail)
    background = BackgroundTasks()

    await task_queue.enqueue_ai_task(
        background,
        kind=AiTaskKind.describe_post,
        entity_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        local_callable=_local_job,
        local_args=("fallback",),
    )

    assert len(background.tasks) == 1


async def test_worker_dispatches_caption_post(monkeypatch):
    from app import worker

    marker = object()
    redis = object()
    calls = []

    async def run(session_factory, redis_client, entity_id, user_id, caller):
        calls.append((session_factory, redis_client, entity_id, user_id, caller))

    monkeypatch.setattr(worker, "get_session_factory", lambda: marker)
    monkeypatch.setattr(worker, "get_redis_client", lambda: redis)
    monkeypatch.setattr(worker.ai_media, "get_caption_caller", lambda: "caption-caller")
    monkeypatch.setattr(worker.ai_media, "caption_post_media_job", run)
    entity_id = uuid.uuid4()
    user_id = uuid.uuid4()

    await worker.run_ai_media_task(
        worker.AiTaskIn(
            kind=AiTaskKind.caption_post,
            entity_id=entity_id,
            user_id=user_id,
        )
    )

    assert calls == [(marker, redis, entity_id, user_id, "caption-caller")]


def test_worker_has_no_public_openapi():
    from app.worker import app

    assert app.openapi_url is None
    assert app.docs_url is None
