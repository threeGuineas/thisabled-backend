"""Redis TTL 카운터 — VISION-01·CAPTION-01 사용자·서비스 전체 호출 한도.

키는 날짜/분 단위로 자연 만료(TTL)되고, 자막 실패(재시도 소진) 시 refund로 복원한다.
"""

from datetime import datetime, timezone

import redis.asyncio as aioredis

from app.core.config import settings

CAPTION_ALLOWED = "allowed"
CAPTION_USER_LIMIT = "user_limit"
CAPTION_GLOBAL_LIMIT = "global_limit"

_CONSUME_CAPTION_LUA = """
local user_count = tonumber(redis.call('GET', KEYS[1]) or '0')
local global_count = tonumber(redis.call('GET', KEYS[2]) or '0')
if user_count >= tonumber(ARGV[1]) then return 1 end
if global_count >= tonumber(ARGV[2]) then return 2 end
local next_user = redis.call('INCR', KEYS[1])
local next_global = redis.call('INCR', KEYS[2])
if next_user == 1 then redis.call('EXPIRE', KEYS[1], ARGV[3]) end
if next_global == 1 then redis.call('EXPIRE', KEYS[2], ARGV[3]) end
return 0
"""

_REFUND_ONCE_LUA = """
if redis.call('SET', KEYS[1], '1', 'NX', 'EX', ARGV[1]) then
  local count = tonumber(redis.call('GET', KEYS[2]) or '0')
  if count > 0 then redis.call('DECR', KEYS[2]) end
  return 1
end
return 0
"""


async def try_consume(redis: aioredis.Redis, key: str, limit: int, ttl_seconds: int) -> bool:
    """카운터 1 증가. 한도 초과면 롤백 후 False."""
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, ttl_seconds)
    if count > limit:
        await redis.decr(key)
        return False
    return True


async def refund(redis: aioredis.Redis, key: str) -> None:
    """CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원."""
    if int(await redis.get(key) or 0) > 0:
        await redis.decr(key)


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _minute() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M")


def vision_keys(user_id) -> list[tuple[str, int, int]]:
    """이미지 1장 = 1회, 게시물·채팅 합산 (VISION-01). [(키, 한도, TTL), ...]"""
    return [
        (f"quota:vision:day:{user_id}:{_today()}", settings.VISION_DAILY_LIMIT, 86400),
        (f"quota:vision:min:{user_id}:{_minute()}", settings.VISION_MINUTE_LIMIT, 60),
    ]


def caption_key(user_id) -> tuple[str, int, int]:
    """영상 업로드 = 1회 차감, 게시물·채팅 합산 (CAPTION-01)."""
    return (f"quota:caption:day:{user_id}:{_today()}", settings.CAPTION_DAILY_LIMIT, 86400)


def caption_global_key() -> tuple[str, int, int]:
    return (
        f"quota:caption:global:day:{_today()}",
        settings.CAPTION_GLOBAL_DAILY_LIMIT,
        86400,
    )


async def consume_caption(redis: aioredis.Redis, user_id) -> str:
    """사용자·서비스 전체 일일 한도를 원자적으로 예약한다."""
    user_key, user_limit, ttl = caption_key(user_id)
    global_key, global_limit, _ = caption_global_key()
    result = int(
        await redis.eval(
            _CONSUME_CAPTION_LUA,
            2,
            user_key,
            global_key,
            user_limit,
            global_limit,
            ttl,
        )
    )
    return {
        0: CAPTION_ALLOWED,
        1: CAPTION_USER_LIMIT,
        2: CAPTION_GLOBAL_LIMIT,
    }[result]


async def consume_caption_retry_attempt(redis: aioredis.Redis) -> bool:
    """내부 재시도도 실제 STT 1회이므로 서비스 전체 상한에 추가 반영한다."""
    key, limit, ttl = caption_global_key()
    return await try_consume(redis, key, limit, ttl)


def caption_refund_marker(scope: str, kind: str, entity_id) -> str:
    return f"quota:caption:refund:{scope}:{kind}:{entity_id}"


async def refund_caption_once(
    redis: aioredis.Redis,
    *,
    scope: str,
    kind: str,
    entity_id,
    user_id,
) -> bool:
    """복구 잡이 중복 실행돼도 같은 시도의 차감은 한 번만 복원한다."""
    counter_key = caption_key(user_id)[0] if scope == "user" else caption_global_key()[0]
    marker = caption_refund_marker(scope, kind, entity_id)
    return bool(await redis.eval(_REFUND_ONCE_LUA, 2, marker, counter_key, 172800))


async def reset_caption_refund_markers(redis: aioredis.Redis, kind: str, entity_id) -> None:
    """사용자가 명시적으로 재시도하면 새 예약에 대한 복원이 가능해야 한다."""
    await redis.delete(
        caption_refund_marker("user", kind, entity_id),
        caption_refund_marker("global", kind, entity_id),
    )
