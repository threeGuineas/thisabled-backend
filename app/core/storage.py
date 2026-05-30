import uuid
from pathlib import Path

import aiofiles

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def _ext_from_content_type(content_type: str) -> str:
    return {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }.get(content_type, ".bin")


async def save_upload(data: bytes, content_type: str) -> str:
    """Save file locally and return the public URL path."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{_ext_from_content_type(content_type)}"
    dest = upload_dir / filename

    async with aiofiles.open(dest, "wb") as f:
        await f.write(data)

    return f"/uploads/{filename}"
