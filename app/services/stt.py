"""OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).

엔드포인트는 `stt.transcribe(...)` 를 호출한다.
테스트는 이 함수를 monkeypatch 해서 실제 OpenAI 호출 없이 검증한다.
"""

import asyncio
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.caption_errors import CaptionTranscriptionError

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise CaptionTranscriptionError(
                "CAPTION_CONFIGURATION_ERROR", auto_retryable=False
            )
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


async def _extract_audio_to_m4a(media_path: Path) -> Path:
    """최대 200MB 영상을 STT 상한 안의 단일 채널 M4A 음성으로 정규화한다."""
    with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as temp:
        output_path = Path(temp.name)
    try:
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(media_path),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "aac",
            "-b:a",
            "64k",
            str(output_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
    except OSError as exc:
        output_path.unlink(missing_ok=True)
        raise CaptionTranscriptionError(
            "CAPTION_PROCESSOR_UNAVAILABLE", auto_retryable=False
        ) from exc
    _stdout, _stderr = await process.communicate()
    if process.returncode != 0:
        output_path.unlink(missing_ok=True)
        raise CaptionTranscriptionError(
            "CAPTION_AUDIO_EXTRACTION_FAILED", auto_retryable=False
        )
    return output_path


def _segment_value(segment: Any, field: str) -> Any:
    if isinstance(segment, Mapping):
        return segment.get(field)
    return getattr(segment, field, None)


def _normalize_segments(segments: list[Any] | None) -> list[dict]:
    """OpenAI SDK 버전별 dict/Pydantic 세그먼트를 공통 JSON 형태로 바꾼다."""
    normalized: list[dict] = []
    for segment in segments or []:
        start = _segment_value(segment, "start")
        end = _segment_value(segment, "end")
        text = _segment_value(segment, "text")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise CaptionTranscriptionError(
                "CAPTION_RESPONSE_INVALID",
                auto_retryable=False,
                external_call_made=True,
            )
        if not isinstance(text, str):
            raise CaptionTranscriptionError(
                "CAPTION_RESPONSE_INVALID",
                auto_retryable=False,
                external_call_made=True,
            )
        normalized.append(
            {"start": float(start), "end": float(end), "text": text.strip()}
        )
    return normalized


async def transcribe_segments(media_path: Path, content_type: str) -> list[dict]:
    """영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01)."""
    # MP4/WebM/MOV 및 과거 .bin 모두 ffmpeg가 실제 컨테이너를 판독한다.
    # 영상 원본(최대 200MB)을 그대로 외부로 보내지 않아 STT 25MB 상한도 지킨다.
    converted_path = await _extract_audio_to_m4a(media_path)
    try:
        with converted_path.open("rb") as media_file:
            resp = await _get_client().audio.transcriptions.create(
                model=settings.STT_MODEL,
                file=(converted_path.name, media_file, "audio/mp4"),
                language="ko",
                response_format="verbose_json",
            )
    finally:
        converted_path.unlink(missing_ok=True)
    raw_segments = (
        resp.get("segments")
        if isinstance(resp, Mapping)
        else getattr(resp, "segments", None)
    )
    return _normalize_segments(raw_segments)
