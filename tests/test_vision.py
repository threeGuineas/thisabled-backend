"""F02_S04 GPT-4o Vision 해설 — 실제 OpenAI 호출 없이 mock 으로 검증."""

import base64

from app.services import vision as vision_service
from tests.conftest import auth_header, register

# 1x1 투명 PNG
_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


async def _upload_png(client, token: str) -> str:
    resp = await client.post(
        "/api/v1/upload",
        headers=auth_header(token),
        files={"file": ("test.png", _PNG, "image/png")},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["url"]


def _patch_vision(monkeypatch):
    """generate_description 을 호출 횟수를 세는 스텁으로 교체."""
    calls = {"n": 0}

    async def fake(image_bytes, content_type):
        calls["n"] += 1
        return "노란 배경에 작은 점이 하나 있는 단순한 이미지입니다."

    monkeypatch.setattr(vision_service, "generate_description", fake)
    return calls


async def test_describe_returns_description(client, monkeypatch):
    calls = _patch_vision(monkeypatch)
    data = await register(client, "visiona")
    url = await _upload_png(client, data["access_token"])

    resp = await client.post(
        "/api/v1/vision/describe",
        json={"image_url": url},
        headers=auth_header(data["access_token"]),
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "이미지" in body["description"]
    assert body["cached"] is False
    assert calls["n"] == 1


async def test_describe_uses_cache(client, monkeypatch):
    calls = _patch_vision(monkeypatch)
    data = await register(client, "visionb")
    token = data["access_token"]
    url = await _upload_png(client, token)

    first = await client.post(
        "/api/v1/vision/describe", json={"image_url": url}, headers=auth_header(token)
    )
    second = await client.post(
        "/api/v1/vision/describe", json={"image_url": url}, headers=auth_header(token)
    )
    assert first.json()["cached"] is False
    assert second.json()["cached"] is True
    # 동일 이미지 → GPT 호출은 1회뿐 (캐시 적중)
    assert calls["n"] == 1


async def test_describe_requires_auth(client, monkeypatch):
    _patch_vision(monkeypatch)
    resp = await client.post(
        "/api/v1/vision/describe", json={"image_url": "/uploads/whatever.png"}
    )
    assert resp.status_code == 401


async def test_describe_missing_image(client, monkeypatch):
    _patch_vision(monkeypatch)
    data = await register(client, "visionc")
    resp = await client.post(
        "/api/v1/vision/describe",
        json={"image_url": "/uploads/does-not-exist.png"},
        headers=auth_header(data["access_token"]),
    )
    assert resp.status_code == 404


async def test_describe_rejects_external_url(client, monkeypatch):
    _patch_vision(monkeypatch)
    data = await register(client, "visiond")
    resp = await client.post(
        "/api/v1/vision/describe",
        json={"image_url": "https://evil.example.com/x.png"},
        headers=auth_header(data["access_token"]),
    )
    assert resp.status_code == 400
