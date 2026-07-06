"""OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).

엔드포인트는 `stt.transcribe(...)` 를 호출한다.
테스트는 이 함수를 monkeypatch 해서 실제 OpenAI 호출 없이 검증한다.
"""

from openai import AsyncOpenAI

from app.core.config import settings

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY 가 설정되지 않았습니다 (.env 확인)")
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def transcribe(audio_bytes: bytes, filename: str, content_type: str) -> str:
    """오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력)"""
    resp = await _get_client().audio.transcriptions.create(
        model=settings.STT_MODEL,
        file=(filename, audio_bytes, content_type),
        language="ko",
    )
    return (resp.text or "").strip()


async def transcribe_segments(media_bytes: bytes, filename: str) -> list[dict]:
    """영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01)."""
    resp = await _get_client().audio.transcriptions.create(
        model=settings.STT_MODEL,
        file=(filename, media_bytes),
        language="ko",
        response_format="verbose_json",
    )
    return [
        {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
        for seg in (resp.segments or [])
    ]
