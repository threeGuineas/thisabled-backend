"""서버가 직접 영상 컨테이너와 재생 시간을 검증한다."""

import asyncio
import json
from pathlib import Path


class InvalidVideo(Exception):
    pass


_EXPECTED_FORMATS = {
    "video/mp4": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    "video/quicktime": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    "video/webm": {"matroska", "webm"},
}


async def probe_video_duration(path: Path, content_type: str) -> float:
    process = await asyncio.create_subprocess_exec(
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_entries",
        "format=format_name,duration:stream=codec_type",
        "-of",
        "json",
        str(path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _stderr = await process.communicate()
    if process.returncode != 0:
        raise InvalidVideo("영상 파일을 분석할 수 없습니다")
    try:
        result = json.loads(stdout)
        duration = float(result["format"]["duration"])
        formats = set(result["format"]["format_name"].split(","))
        has_video_stream = any(
            stream.get("codec_type") == "video" for stream in result.get("streams", [])
        )
    except (KeyError, TypeError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        raise InvalidVideo("영상 정보를 확인할 수 없습니다") from exc
    if duration <= 0:
        raise InvalidVideo("영상 길이가 올바르지 않습니다")
    if not has_video_stream:
        raise InvalidVideo("비디오 트랙이 없는 파일입니다")
    expected_formats = _EXPECTED_FORMATS.get(content_type, set())
    if not formats.intersection(expected_formats):
        raise InvalidVideo("파일 내용과 영상 형식이 일치하지 않습니다")
    return duration


def get_video_probe():
    return probe_video_duration
