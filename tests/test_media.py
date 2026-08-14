"""VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소."""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest_asyncio
from sqlalchemy import select, update

from app.main import app
from app.models import Post, PostMedia
from app.core.config import settings
from app.core.storage import _ext_from_content_type
from app.services import ai_media, media_probe, stt
from app.services.quota import caption_global_key, vision_keys
from app.services.scheduler import cleanup_stale_drafts, recover_processing_captions
from tests.conftest import auth_header, register

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 64


class CallCounter:
    def __init__(self, result=None, error=None):
        self.calls = 0
        self.result = result
        self.error = error

    async def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


@pytest_asyncio.fixture
async def fake_ai():
    """외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints)."""
    describe = CallCounter(result="파란 하늘 아래 공원 사진")
    caption = CallCounter(result=[{"start": 0.0, "end": 2.0, "text": "안녕하세요"}])
    text = CallCounter(result="음성 입력 결과 텍스트")
    app.dependency_overrides[ai_media.get_describe_caller] = lambda: describe
    app.dependency_overrides[ai_media.get_caption_caller] = lambda: caption
    app.dependency_overrides[ai_media.get_text_transcriber] = lambda: text
    app.dependency_overrides[media_probe.get_video_probe] = lambda: (
        lambda _path, _content_type: _fake_duration()
    )
    yield {"describe": describe, "caption": caption, "text": text}
    for key in (
        ai_media.get_describe_caller,
        ai_media.get_caption_caller,
        ai_media.get_text_transcriber,
        media_probe.get_video_probe,
    ):
        app.dependency_overrides.pop(key, None)


async def _fake_duration():
    return 60.0


async def _upload_images(client, h, n=1, name_prefix="img"):
    files = [("files", (f"{name_prefix}{i}.png", PNG + bytes([i]), "image/png")) for i in range(n)]
    return await client.post("/api/v1/media/images", files=files, headers=h)


async def _wait_media_status(db, media_id: str, expected: str) -> PostMedia:
    """새 Starlette에서는 응답 본문 뒤 background task가 별도 스케줄될 수 있어 완료를 기다린다."""
    # 테스트는 모든 세션이 한 DB 커넥션을 공유한다. 잡이 커밋하기 전에 조회를 시작하면
    # 커넥션을 선점하므로, fake 잡이 먼저 실행될 기회를 준 뒤 상태를 읽는다.
    await asyncio.sleep(0.05)
    media = await db.get(PostMedia, uuid.UUID(media_id))
    await db.refresh(media)
    assert media.description_status == expected
    return media


async def test_image_upload_limit_3(client, fake_ai):
    u = await register(client, "사진업로더")
    h = auth_header(u["access_token"])
    assert (await _upload_images(client, h, 3)).status_code == 201
    assert (await _upload_images(client, h, 4)).status_code == 400


async def test_invalid_image_batch_leaves_no_orphan_file(client, monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(tmp_path))
    user = await register(client, "사진원자성")
    response = await client.post(
        "/api/v1/media/images",
        files=[
            ("files", ("valid.png", PNG, "image/png")),
            ("files", ("invalid.txt", b"not image", "text/plain")),
        ],
        headers=auth_header(user["access_token"]),
    )
    assert response.status_code == 400
    assert list(tmp_path.iterdir()) == []


async def test_photo_post_gets_description_on_publish(client, db, fake_ai):
    u = await register(client, "사진게시자")
    h = auth_header(u["access_token"])
    up = await _upload_images(client, h, 1)
    media_id = up.json()["items"][0]["media_id"]
    resp = await client.post(
        "/api/v1/posts",
        json={"title": "사진 글", "category": "daily", "content": "사진 글", "media_ids": [media_id]},
        headers=h,
    )
    assert resp.status_code == 201
    assert fake_ai["describe"].calls == 1

    media = await _wait_media_status(db, media_id, "done")
    assert media.description_status == "done"
    assert media.description == "파란 하늘 아래 공원 사진"
    assert fake_ai["describe"].calls == 1


async def test_same_image_hash_uses_cache(client, db, fake_ai):
    u = await register(client, "캐시유저")
    h = auth_header(u["access_token"])
    for _ in range(2):  # 동일 바이트 → 동일 해시
        up = await client.post(
            "/api/v1/media/images",
            files=[("files", ("same.png", PNG, "image/png"))], headers=h,
        )
        mid = up.json()["items"][0]["media_id"]
        r = await client.post(
            "/api/v1/posts",
            json={"title": "글", "category": "daily", "content": "글", "media_ids": [mid]},
            headers=h,
        )
        assert r.status_code == 201
        await _wait_media_status(db, mid, "done")
    assert fake_ai["describe"].calls == 1  # 두 번째는 ai_result_cache 적중


async def test_vision_quota_exceeded_publishes_without_description(client, db, test_redis, fake_ai):
    u = await register(client, "한도유저")
    h = auth_header(u["access_token"])
    # 일일 한도 소진 상태 재현
    day_key = vision_keys(u["user_id"])[0][0]
    await test_redis.set(day_key, 20)

    up = await _upload_images(client, h, 1, name_prefix="quota")
    mid = up.json()["items"][0]["media_id"]
    resp = await client.post(
        "/api/v1/posts",
        json={"title": "한도 글", "category": "daily", "content": "한도 글", "media_ids": [mid]},
        headers=h,
    )
    assert resp.status_code == 201  # 설명 없이 게시 정상 (VISION-01 예외)

    media = await _wait_media_status(db, mid, "failed")
    assert media.description is None
    assert media.description_status == "failed"
    assert fake_ai["describe"].calls == 0


async def test_video_upload_creates_draft_then_publish(client, db, fake_ai):
    u = await register(client, "영상업로더")
    h = auth_header(u["access_token"])
    up = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"fakevideo", "video/mp4")},
        data={"duration_seconds": "60"},
        headers=h,
    )
    assert up.status_code == 201, up.text
    body = up.json()
    post_id = body["post_id"]

    status = await client.get(f"/api/v1/posts/{post_id}/caption-status", headers=h)
    assert status.json()["caption_status"] == "done"  # fake caller 즉시 완료

    pub = await client.post(
        f"/api/v1/posts/{post_id}/publish",
        json={"title": "영상 글", "category": "hobby", "content": "영상 본문"},
        headers=h,
    )
    assert pub.status_code == 200, pub.text
    assert pub.json()["status"] == "published"
    assert pub.json()["media"][0]["caption"] == [{"start": 0.0, "end": 2.0, "text": "안녕하세요"}]


def test_video_content_types_keep_supported_extensions():
    assert _ext_from_content_type("video/mp4") == ".mp4"
    assert _ext_from_content_type("video/webm") == ".webm"
    assert _ext_from_content_type("video/quicktime") == ".mov"


async def test_stt_receives_extension_and_content_type(tmp_path, monkeypatch):
    captured = {}

    class Transcriptions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(segments=[])

    fake_client = SimpleNamespace(audio=SimpleNamespace(transcriptions=Transcriptions()))
    monkeypatch.setattr(stt, "_get_client", lambda: fake_client)
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"video")
    extracted_path = tmp_path / "extracted.m4a"

    async def extract(_path):
        extracted_path.write_bytes(b"audio")
        return extracted_path

    monkeypatch.setattr(stt, "_extract_audio_to_m4a", extract)

    assert await stt.transcribe_segments(media_path, "video/mp4") == []
    filename, _file, content_type = captured["file"]
    assert filename == "extracted.m4a"
    assert content_type == "audio/mp4"
    assert not extracted_path.exists()


async def test_caption_failure_requires_explicit_choice_and_refunds(client, db, test_redis, fake_ai):
    fake_ai["caption"].error = RuntimeError("stt down")
    u = await register(client, "자막실패자")
    h = auth_header(u["access_token"])
    up = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"failvideo", "video/mp4")},
        data={"duration_seconds": "60"},
        headers=h,
    )
    post_id = up.json()["post_id"]
    status = await client.get(f"/api/v1/posts/{post_id}/caption-status", headers=h)
    assert status.json()["caption_status"] == "failed"

    # 재시도 소진 → 일일 횟수 복원 (CAPTION-01): 카운터가 0으로 복귀
    from app.services.quota import caption_key
    assert int(await test_redis.get(caption_key(u["user_id"])[0]) or 0) == 0

    publish_body = {"title": "자막 실패", "category": "info", "content": "영상 본문"}
    no_choice = await client.post(
        f"/api/v1/posts/{post_id}/publish", json=publish_body, headers=h
    )
    assert no_choice.status_code == 400
    ok = await client.post(
        f"/api/v1/posts/{post_id}/publish",
        json={**publish_body, "allow_no_caption": True},
        headers=h,
    )
    assert ok.status_code == 200
    assert ok.json()["media"][0]["caption_status"] == "failed"  # '자막 없음' 라벨 근거


async def test_failed_caption_can_be_retried(client, db, test_redis, fake_ai):
    fake_ai["caption"].error = RuntimeError("stt down")
    u = await register(client, "자막재시도")
    h = auth_header(u["access_token"])
    up = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"retryvideo", "video/mp4")},
        data={"duration_seconds": "60"},
        headers=h,
    )
    post_id = up.json()["post_id"]
    assert (
        await client.get(f"/api/v1/posts/{post_id}/caption-status", headers=h)
    ).json()["caption_status"] == "failed"

    fake_ai["caption"].error = None
    retried = await client.post(f"/api/v1/posts/{post_id}/caption/retry", headers=h)
    assert retried.status_code == 202, retried.text
    assert (
        await client.get(f"/api/v1/posts/{post_id}/caption-status", headers=h)
    ).json()["caption_status"] == "done"


async def test_global_caption_limit_blocks_upload(client, test_redis, fake_ai):
    u = await register(client, "전체자막한도")
    key, limit, _ttl = caption_global_key()
    await test_redis.set(key, limit)
    response = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"budgetvideo", "video/mp4")},
        data={"duration_seconds": "60"},
        headers=auth_header(u["access_token"]),
    )
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "STT_DAILY_BUDGET_EXCEEDED"


async def test_video_limits(client, fake_ai):
    u = await register(client, "영상제한")
    h = auth_header(u["access_token"])
    too_long = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"x", "video/mp4")},
        data={"duration_seconds": "181"},
        headers=h,
    )
    assert too_long.status_code == 400
    invalid = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"x", "video/mp4")},
        data={"duration_seconds": "0"},
        headers=h,
    )
    assert invalid.status_code == 400


async def test_transcribe_voice_input(client, fake_ai):
    u = await register(client, "음성입력자")
    h = auth_header(u["access_token"])
    resp = await client.post(
        "/api/v1/media/transcribe",
        files={"file": ("rec.webm", b"fakeaudio", "audio/webm")},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["text"] == "음성 입력 결과 텍스트"


async def test_cleanup_deletes_stale_drafts(client, db, _session_factory, fake_ai):
    u = await register(client, "드래프트청소")
    h = auth_header(u["access_token"])
    up = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"stalevideo", "video/mp4")},
        data={"duration_seconds": "10"},
        headers=h,
    )
    post_id = uuid.UUID(up.json()["post_id"])
    # 25시간 전 업로드로 조작
    await db.execute(
        update(Post).where(Post.id == post_id).values(
            created_at=datetime.now(timezone.utc) - timedelta(hours=25)
        )
    )
    await db.commit()

    await cleanup_stale_drafts(session_factory=_session_factory)
    assert await db.get(Post, post_id) is None  # 미디어는 FK CASCADE


async def test_recovery_restarts_processing_caption(
    client, db, _session_factory, test_redis, fake_ai
):
    u = await register(client, "자막복구")
    h = auth_header(u["access_token"])
    up = await client.post(
        "/api/v1/media/videos",
        files={"file": ("v.mp4", b"recovervideo", "video/mp4")},
        data={"duration_seconds": "60"},
        headers=h,
    )
    media = await db.get(PostMedia, uuid.UUID(up.json()["media_id"]))
    media.caption = None
    media.caption_status = "processing"
    await db.commit()

    recovered = await recover_processing_captions(
        session_factory=_session_factory,
        redis=test_redis,
        caller=fake_ai["caption"],
    )
    await db.refresh(media)
    assert recovered >= 1
    assert media.caption_status == "done"
