"""VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소."""

import uuid
from datetime import datetime, timedelta, timezone

import pytest_asyncio
from sqlalchemy import select, update

from app.main import app
from app.models import Post, PostMedia
from app.services import ai_media
from app.services.quota import vision_keys
from app.services.scheduler import cleanup_stale_drafts
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
    yield {"describe": describe, "caption": caption, "text": text}
    for key in (ai_media.get_describe_caller, ai_media.get_caption_caller, ai_media.get_text_transcriber):
        app.dependency_overrides.pop(key, None)


async def _upload_images(client, h, n=1, name_prefix="img"):
    files = [("files", (f"{name_prefix}{i}.png", PNG + bytes([i]), "image/png")) for i in range(n)]
    return await client.post("/api/v1/media/images", files=files, headers=h)


async def test_image_upload_limit_3(client, fake_ai):
    u = await register(client, "사진업로더")
    h = auth_header(u["access_token"])
    assert (await _upload_images(client, h, 3)).status_code == 201
    assert (await _upload_images(client, h, 4)).status_code == 400


async def test_photo_post_gets_description_on_publish(client, db, fake_ai):
    u = await register(client, "사진게시자")
    h = auth_header(u["access_token"])
    up = await _upload_images(client, h, 1)
    media_id = up.json()["items"][0]["media_id"]
    resp = await client.post("/api/v1/posts", json={"content": "사진 글", "media_ids": [media_id]}, headers=h)
    assert resp.status_code == 201

    media = await db.get(PostMedia, uuid.UUID(media_id))
    await db.refresh(media)
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
        r = await client.post("/api/v1/posts", json={"content": "글", "media_ids": [mid]}, headers=h)
        assert r.status_code == 201
    assert fake_ai["describe"].calls == 1  # 두 번째는 ai_result_cache 적중


async def test_vision_quota_exceeded_publishes_without_description(client, db, test_redis, fake_ai):
    u = await register(client, "한도유저")
    h = auth_header(u["access_token"])
    # 일일 한도 소진 상태 재현
    day_key = vision_keys(u["user_id"])[0][0]
    await test_redis.set(day_key, 20)

    up = await _upload_images(client, h, 1, name_prefix="quota")
    mid = up.json()["items"][0]["media_id"]
    resp = await client.post("/api/v1/posts", json={"content": "한도 글", "media_ids": [mid]}, headers=h)
    assert resp.status_code == 201  # 설명 없이 게시 정상 (VISION-01 예외)

    media = await db.get(PostMedia, uuid.UUID(mid))
    await db.refresh(media)
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

    pub = await client.post(f"/api/v1/posts/{post_id}/publish", json={}, headers=h)
    assert pub.status_code == 200, pub.text
    assert pub.json()["status"] == "published"
    assert pub.json()["media"][0]["caption"] == [{"start": 0.0, "end": 2.0, "text": "안녕하세요"}]


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

    no_choice = await client.post(f"/api/v1/posts/{post_id}/publish", json={}, headers=h)
    assert no_choice.status_code == 400
    ok = await client.post(
        f"/api/v1/posts/{post_id}/publish", json={"allow_no_caption": True}, headers=h
    )
    assert ok.status_code == 200
    assert ok.json()["media"][0]["caption_status"] == "failed"  # '자막 없음' 라벨 근거


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
