"""VISION-01 사진 설명 · CAPTION-01 자막 — 캐시·쿼터·재시도 오케스트레이션.

외부 호출은 콜러블 주입(DI)으로 받아 테스트에서 fake로 대체한다.
파이프라인: ai_result_cache 조회 → 쿼터 → 호출(재시도 ≤ AI_RETRY_MAX) → 캐시 저장.
실패는 감추지 않되(§19.3) 게시물·채팅 기본 흐름을 막지 않는다 (§18.3).
"""

import hashlib
import logging
import uuid
from dataclasses import dataclass
from pathlib import Path

import redis.asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.enums import AiStatus
from app.core.storage import content_type_from_path
from app.models import AiResultCache, ChatMessage, ChatRoom, PostMedia
from app.services import stt, vision
from app.services.caption_errors import CaptionTranscriptionError
from app.services.quota import (
    consume_caption_retry_attempt,
    refund,
    refund_caption_once,
    try_consume,
    vision_keys,
)

logger = logging.getLogger(__name__)

_RELEASE_LOCK_LUA = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
  return redis.call('DEL', KEYS[1])
end
return 0
"""


@dataclass(frozen=True)
class CaptionGenerationResult:
    segments: list | None
    failure_code: str | None = None


def media_hash_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def media_hash_from_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as media_file:
        while chunk := media_file.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def file_path_from_url(url: str) -> Path:
    """'/uploads/<name>' → 컨테이너 로컬 경로."""
    return Path(settings.UPLOAD_DIR) / Path(url).name


# ── DI 지점: 테스트는 이 의존성들을 fake로 override ──────────────

def get_describe_caller():
    """(image_bytes, content_type) -> 설명 텍스트. 실구현: GPT 계열 Vision."""
    return vision.generate_description


def get_caption_caller():
    """(media_path, content_type) -> [{start,end,text}] 세그먼트. 실구현: Whisper."""
    return stt.transcribe_segments


def get_text_transcriber():
    """VIS-03 음성 입력용 (bytes, filename, content_type) -> text."""
    return stt.transcribe


# ── 캐시 ────────────────────────────────────────────────────────

async def _cache_get(db: AsyncSession, kind: str, media_hash: str) -> dict | None:
    row = (
        await db.execute(
            select(AiResultCache.result).where(
                AiResultCache.kind == kind, AiResultCache.media_hash == media_hash
            )
        )
    ).scalar_one_or_none()
    return row


async def _cache_put(db: AsyncSession, kind: str, media_hash: str, result: dict) -> None:
    if await _cache_get(db, kind, media_hash) is None:
        db.add(AiResultCache(id=uuid.uuid4(), kind=kind, media_hash=media_hash, result=result))


# ── VISION-01 ───────────────────────────────────────────────────

async def consume_vision(redis: aioredis.Redis, user_id) -> bool:
    """일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백."""
    day, minute = vision_keys(user_id)
    if not await try_consume(redis, *day):
        return False
    if not await try_consume(redis, *minute):
        await refund(redis, day[0])
        return False
    return True


async def describe_image(
    db: AsyncSession,
    redis: aioredis.Redis,
    *,
    user_id,
    media_hash: str,
    image_bytes: bytes,
    content_type: str,
    caller,
) -> str | None:
    """사진 설명 생성. 실패·한도 초과 시 None (게시·전송은 정상 유지)."""
    cached = await _cache_get(db, "vision", media_hash)
    if cached is not None:
        return cached.get("description")

    if not await consume_vision(redis, user_id):
        return None

    for _ in range(1 + settings.AI_RETRY_MAX):
        try:
            description = await caller(image_bytes, content_type)
        except Exception:
            continue
        await _cache_put(db, "vision", media_hash, {"description": description})
        return description
    return None


async def generate_caption(
    db: AsyncSession,
    redis: aioredis.Redis,
    *,
    user_id,
    media_hash: str,
    media_path: Path,
    content_type: str,
    kind: str,
    entity_id,
    caller,
) -> CaptionGenerationResult:
    """자막 세그먼트 생성. 쿼터는 업로드 시점에 이미 차감 — 실패(재시도 소진) 시 복원."""
    cached = await _cache_get(db, "caption", media_hash)
    if cached is not None:
        # 전역 상한은 외부 STT 비용 방어용이므로 캐시 적중 예약은 복원한다.
        await refund_caption_once(
            redis, scope="global", kind=kind, entity_id=entity_id, user_id=user_id
        )
        return CaptionGenerationResult(segments=cached.get("segments"))

    failure_code = "CAPTION_TRANSCRIPTION_FAILED"
    for attempt in range(1 + settings.AI_RETRY_MAX):
        if attempt > 0 and not await consume_caption_retry_attempt(redis):
            logger.warning(
                "caption retry skipped by global budget kind=%s entity_id=%s attempt=%s",
                kind,
                entity_id,
                attempt + 1,
            )
            break
        try:
            segments = await caller(media_path, content_type)
        except CaptionTranscriptionError as exc:
            failure_code = exc.code
            logger.warning(
                "caption processing failed kind=%s entity_id=%s attempt=%s code=%s",
                kind,
                entity_id,
                attempt + 1,
                exc.code,
                exc_info=True,
            )
            if not exc.external_call_made:
                await refund_caption_once(
                    redis,
                    scope="global",
                    kind=kind,
                    entity_id=entity_id,
                    user_id=user_id,
                )
            if not exc.auto_retryable:
                break
        except Exception:
            logger.warning(
                "caption transcription failed kind=%s entity_id=%s attempt=%s",
                kind,
                entity_id,
                attempt + 1,
                exc_info=True,
            )
            continue
        else:
            await _cache_put(db, "caption", media_hash, {"segments": segments})
            return CaptionGenerationResult(segments=segments)

    await refund_caption_once(
        redis, scope="user", kind=kind, entity_id=entity_id, user_id=user_id
    )
    return CaptionGenerationResult(segments=None, failure_code=failure_code)


async def _acquire_caption_lock(redis: aioredis.Redis, kind: str, entity_id) -> tuple[str, str] | None:
    key = f"lock:caption:{kind}:{entity_id}"
    token = uuid.uuid4().hex
    acquired = await redis.set(key, token, nx=True, ex=settings.CAPTION_JOB_LOCK_SECONDS)
    return (key, token) if acquired else None


async def _release_caption_lock(redis: aioredis.Redis, lock: tuple[str, str] | None) -> None:
    if lock is not None:
        await redis.eval(_RELEASE_LOCK_LUA, 1, lock[0], lock[1])


async def _refund_unattempted_caption(redis, *, kind: str, entity_id, user_id) -> None:
    # 파일 유실 등 STT 호출 전 실패는 사용자·전역 예약 모두 복원한다.
    await refund_caption_once(
        redis, scope="user", kind=kind, entity_id=entity_id, user_id=user_id
    )
    await refund_caption_once(
        redis, scope="global", kind=kind, entity_id=entity_id, user_id=user_id
    )


async def _notify_post_caption(
    db, redis, media: PostMedia, user_id, succeeded: bool, failure_code: str | None = None
) -> None:
    from app.services import notify as noti

    await noti.notify(
        db,
        redis,
        user_id,
        noti.CAPTION_DONE if succeeded else noti.CAPTION_FAILED,
        {
            "post_id": str(media.post_id),
            "media_id": str(media.id),
            "failure_code": failure_code,
        },
    )


async def _notify_chat_caption(
    db, redis, msg: ChatMessage, succeeded: bool, failure_code: str | None = None
) -> None:
    from app.services import notify as noti

    room = await db.get(ChatRoom, msg.room_id)
    if room is None:
        return
    recipients = {room.user_a, room.user_b}
    recipients.discard(None)
    for recipient_id in recipients:
        await noti.notify(
            db,
            redis,
            recipient_id,
            noti.CAPTION_DONE if succeeded else noti.CAPTION_FAILED,
            {
                "room_id": str(msg.room_id),
                "message_id": str(msg.id),
                "failure_code": failure_code,
            },
        )


# ── 백그라운드 잡 (BackgroundTasks에서 실행) ─────────────────────

async def describe_post_media_job(
    session_factory: async_sessionmaker, redis: aioredis.Redis, media_id, user_id, caller
) -> None:
    async with session_factory() as db:
        media = await db.get(PostMedia, media_id)
        if media is None:
            return
        path = file_path_from_url(media.url)
        try:
            data = path.read_bytes()
        except OSError:
            media.description_status = AiStatus.failed.value
            await db.commit()
            return
        description = await describe_image(
            db, redis,
            user_id=user_id, media_hash=media.media_hash,
            image_bytes=data, content_type=f"image/{path.suffix.lstrip('.') or 'png'}",
            caller=caller,
        )
        media.description = description
        media.description_status = (
            AiStatus.done.value if description is not None else AiStatus.failed.value
        )
        await db.commit()


async def describe_chat_message_job(
    session_factory: async_sessionmaker, redis: aioredis.Redis, message_id, media_hash, user_id, caller
) -> None:
    """채팅 사진: 즉시 전달 후 설명을 비동기 부착 (VISION-01 채팅 사진 처리)."""
    async with session_factory() as db:
        msg = await db.get(ChatMessage, message_id)
        if msg is None or msg.media_url is None:
            return
        path = file_path_from_url(msg.media_url)
        try:
            data = path.read_bytes()
        except OSError:
            msg.description_status = AiStatus.failed.value
            await db.commit()
            return
        description = await describe_image(
            db, redis,
            user_id=user_id, media_hash=media_hash,
            image_bytes=data, content_type=f"image/{path.suffix.lstrip('.') or 'png'}",
            caller=caller,
        )
        msg.description = description
        msg.description_status = (
            AiStatus.done.value if description is not None else AiStatus.failed.value
        )
        await db.commit()


async def caption_chat_message_job(
    session_factory: async_sessionmaker, redis: aioredis.Redis, message_id, media_hash, user_id, caller
) -> None:
    """채팅 영상: 즉시 전달 후 자막을 비동기 부착 (CAPTION-01 채팅 영상 처리)."""
    lock = await _acquire_caption_lock(redis, "chat", message_id)
    if lock is None:
        return
    try:
        async with session_factory() as db:
            msg = await db.get(ChatMessage, message_id)
            if (
                msg is None
                or msg.media_url is None
                or msg.caption_status != AiStatus.processing.value
            ):
                return
            path = file_path_from_url(msg.media_url)
            if not path.is_file():
                await _refund_unattempted_caption(
                    redis, kind="chat", entity_id=message_id, user_id=user_id
                )
                msg.caption_status = AiStatus.failed.value
                msg.caption_failure_code = "CAPTION_SOURCE_MISSING"
                await db.commit()
                await _notify_chat_caption(
                    db, redis, msg, False, msg.caption_failure_code
                )
                return
            result = await generate_caption(
                db,
                redis,
                user_id=user_id,
                media_hash=media_hash,
                media_path=path,
                content_type=content_type_from_path(path),
                kind="chat",
                entity_id=message_id,
                caller=caller,
            )
            msg.caption = result.segments
            msg.caption_status = (
                AiStatus.done.value
                if result.segments is not None
                else AiStatus.failed.value
            )
            msg.caption_failure_code = result.failure_code
            await db.commit()
            await _notify_chat_caption(
                db,
                redis,
                msg,
                result.segments is not None,
                result.failure_code,
            )
    finally:
        await _release_caption_lock(redis, lock)


async def caption_post_media_job(
    session_factory: async_sessionmaker, redis: aioredis.Redis, media_id, user_id, caller
) -> None:
    lock = await _acquire_caption_lock(redis, "post", media_id)
    if lock is None:
        return
    try:
        async with session_factory() as db:
            media = await db.get(PostMedia, media_id)
            if media is None or media.caption_status != AiStatus.processing.value:
                return
            path = file_path_from_url(media.url)
            if not path.is_file():
                await _refund_unattempted_caption(
                    redis, kind="post", entity_id=media_id, user_id=user_id
                )
                media.caption_status = AiStatus.failed.value
                media.caption_failure_code = "CAPTION_SOURCE_MISSING"
                await db.commit()
                await _notify_post_caption(
                    db, redis, media, user_id, False, media.caption_failure_code
                )
                return
            result = await generate_caption(
                db,
                redis,
                user_id=user_id,
                media_hash=media.media_hash,
                media_path=path,
                content_type=content_type_from_path(path),
                kind="post",
                entity_id=media_id,
                caller=caller,
            )
            media.caption = result.segments
            media.caption_status = (
                AiStatus.done.value
                if result.segments is not None
                else AiStatus.failed.value
            )
            media.caption_failure_code = result.failure_code
            await db.commit()
            await _notify_post_caption(
                db,
                redis,
                media,
                user_id,
                result.segments is not None,
                result.failure_code,
            )
    finally:
        await _release_caption_lock(redis, lock)
