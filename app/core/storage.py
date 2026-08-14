import hashlib
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import aiofiles

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "video/quicktime": ".mov",
}

EXTENSION_CONTENT_TYPES = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
}


class UploadReader(Protocol):
    async def read(self, size: int = -1) -> bytes: ...


class UploadTooLarge(Exception):
    pass


@dataclass(frozen=True)
class SavedUpload:
    url: str
    path: Path
    size: int
    media_hash: str


def _ext_from_content_type(content_type: str) -> str:
    return CONTENT_TYPE_EXTENSIONS.get(content_type, ".bin")


def content_type_from_path(path: Path) -> str:
    """STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다."""
    return EXTENSION_CONTENT_TYPES.get(path.suffix.lower(), "application/octet-stream")


async def save_upload(data: bytes, content_type: str) -> str:
    """Save file locally and return the public URL path."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{_ext_from_content_type(content_type)}"
    dest = upload_dir / filename

    async with aiofiles.open(dest, "wb") as f:
        await f.write(data)

    return f"/uploads/{filename}"


async def save_upload_stream(
    reader: UploadReader,
    content_type: str,
    *,
    max_bytes: int,
    chunk_size: int = 1024 * 1024,
) -> SavedUpload:
    """업로드를 메모리에 통째로 올리지 않고 저장하며 크기와 SHA-256을 계산한다."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{_ext_from_content_type(content_type)}"
    dest = upload_dir / filename
    digest = hashlib.sha256()
    size = 0

    try:
        async with aiofiles.open(dest, "wb") as output:
            while chunk := await reader.read(chunk_size):
                size += len(chunk)
                if size > max_bytes:
                    raise UploadTooLarge
                digest.update(chunk)
                await output.write(chunk)
    except Exception:
        dest.unlink(missing_ok=True)
        raise

    return SavedUpload(
        url=f"/uploads/{filename}",
        path=dest,
        size=size,
        media_hash=digest.hexdigest(),
    )


def delete_upload(url: str) -> None:
    (Path(settings.UPLOAD_DIR) / Path(url).name).unlink(missing_ok=True)
