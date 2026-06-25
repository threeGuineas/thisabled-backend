"""F02_S05 Whisper STT — 실제 OpenAI 호출 없이 mock 으로 검증."""

from app.services import stt as stt_service
from tests.conftest import auth_header, register


def _patch_stt(monkeypatch):
    calls = {"n": 0}

    async def fake(audio_bytes, filename, content_type):
        calls["n"] += 1
        return "안녕하세요 음성 댓글 테스트입니다"

    monkeypatch.setattr(stt_service, "transcribe", fake)
    return calls


async def test_transcribe_returns_text(client, monkeypatch):
    calls = _patch_stt(monkeypatch)
    data = await register(client, "stta")
    resp = await client.post(
        "/api/v1/stt/transcribe",
        headers=auth_header(data["access_token"]),
        files={"file": ("comment.webm", b"fake-audio-bytes", "audio/webm")},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["text"] == "안녕하세요 음성 댓글 테스트입니다"
    assert "duration_ms" in body
    assert calls["n"] == 1


async def test_transcribe_requires_auth(client, monkeypatch):
    _patch_stt(monkeypatch)
    resp = await client.post(
        "/api/v1/stt/transcribe",
        files={"file": ("comment.webm", b"x", "audio/webm")},
    )
    assert resp.status_code == 401


async def test_transcribe_rejects_non_audio(client, monkeypatch):
    _patch_stt(monkeypatch)
    data = await register(client, "sttb")
    resp = await client.post(
        "/api/v1/stt/transcribe",
        headers=auth_header(data["access_token"]),
        files={"file": ("note.txt", b"not audio", "text/plain")},
    )
    assert resp.status_code == 415


async def test_transcribe_rejects_too_large(client, monkeypatch):
    _patch_stt(monkeypatch)
    monkeypatch.setattr(stt_service.settings, "MAX_AUDIO_MB", 0)
    data = await register(client, "sttc")
    resp = await client.post(
        "/api/v1/stt/transcribe",
        headers=auth_header(data["access_token"]),
        files={"file": ("big.webm", b"some-bytes", "audio/webm")},
    )
    assert resp.status_code == 413
