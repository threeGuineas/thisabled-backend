"""CHAT-05 WebRTC 시그널링 세션.

미디어는 전달·저장하지 않는다. Redis에는 참여자와 짧은 수명의 연결 상태만 둔다.
"""

import json
import uuid
from datetime import datetime, timedelta, timezone

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.enums import CallKind, CallSignalType


class CallNotFound(Exception):
    pass


class CallBusy(Exception):
    pass


class InvalidCallSignal(Exception):
    pass


def call_key(call_id: uuid.UUID) -> str:
    return f"chat:call:{call_id}"


def user_call_key(user_id: uuid.UUID) -> str:
    return f"chat:call:user:{user_id}"


_RESERVE_CALL = """
if redis.call('EXISTS', KEYS[2]) == 1 or redis.call('EXISTS', KEYS[3]) == 1 then
  return 0
end
redis.call('SET', KEYS[1], ARGV[1], 'EX', ARGV[2])
redis.call('SET', KEYS[2], ARGV[3], 'EX', ARGV[2])
redis.call('SET', KEYS[3], ARGV[3], 'EX', ARGV[2])
return 1
"""

_UPDATE_CALL = """
if redis.call('EXISTS', KEYS[1]) == 0 then
  return 0
end
if redis.call('GET', KEYS[2]) ~= ARGV[3] or redis.call('GET', KEYS[3]) ~= ARGV[3] then
  return 0
end
redis.call('SET', KEYS[1], ARGV[1], 'EX', ARGV[2])
redis.call('EXPIRE', KEYS[2], ARGV[2])
redis.call('EXPIRE', KEYS[3], ARGV[2])
return 1
"""

_CLOSE_CALL = """
if redis.call('EXISTS', KEYS[1]) == 0 then
  return 0
end
if redis.call('GET', KEYS[2]) ~= ARGV[1] or redis.call('GET', KEYS[3]) ~= ARGV[1] then
  return 0
end
redis.call('DEL', KEYS[1])
redis.call('DEL', KEYS[2])
redis.call('DEL', KEYS[3])
return 1
"""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _serialize(call: dict) -> str:
    return json.dumps(call, ensure_ascii=False, separators=(",", ":"))


def public_call(call: dict) -> dict:
    return {
        "id": call["id"],
        "room_id": call["room_id"],
        "caller_id": call["caller_id"],
        "callee_id": call["callee_id"],
        "kind": call["kind"],
        "status": call["status"],
        "created_at": call["created_at"],
        "expires_at": call["expires_at"],
    }


async def create_call(
    redis: aioredis.Redis,
    *,
    room_id: uuid.UUID,
    caller_id: uuid.UUID,
    callee_id: uuid.UUID,
    kind: CallKind,
) -> dict:
    call_id = uuid.uuid4()
    now = _now()
    expires_at = now + timedelta(seconds=settings.CALL_RING_TTL_SECONDS)
    call = {
        "id": str(call_id),
        "room_id": str(room_id),
        "caller_id": str(caller_id),
        "callee_id": str(callee_id),
        "kind": kind.value,
        "status": "ringing",
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    reserved = await redis.eval(
        _RESERVE_CALL,
        3,
        call_key(call_id),
        user_call_key(caller_id),
        user_call_key(callee_id),
        _serialize(call),
        settings.CALL_RING_TTL_SECONDS,
        str(call_id),
    )
    if reserved != 1:
        raise CallBusy()
    return call


async def get_call(
    redis: aioredis.Redis, call_id: uuid.UUID, user_id: uuid.UUID
) -> dict:
    raw = await redis.get(call_key(call_id))
    if raw is None:
        raise CallNotFound()
    call = json.loads(raw)
    if str(user_id) not in (call["caller_id"], call["callee_id"]):
        raise CallNotFound()
    return call


def counterpart(call: dict, user_id: uuid.UUID) -> uuid.UUID:
    mine = str(user_id)
    return uuid.UUID(call["callee_id"] if mine == call["caller_id"] else call["caller_id"])


def validate_signal(call: dict, user_id: uuid.UUID, signal_type: CallSignalType) -> None:
    is_caller = str(user_id) == call["caller_id"]
    if signal_type == CallSignalType.offer and not is_caller:
        raise InvalidCallSignal()
    if signal_type in {
        CallSignalType.accept,
        CallSignalType.answer,
        CallSignalType.decline,
    } and is_caller:
        raise InvalidCallSignal()
    if call["status"] == "ringing" and signal_type == CallSignalType.answer:
        raise InvalidCallSignal()
    if call["status"] == "active" and signal_type in {
        CallSignalType.offer,
        CallSignalType.accept,
        CallSignalType.decline,
    }:
        raise InvalidCallSignal()


async def update_call_for_signal(
    redis: aioredis.Redis,
    call: dict,
    signal_type: CallSignalType,
) -> tuple[dict, bool]:
    terminal = signal_type in {CallSignalType.decline, CallSignalType.end}
    if terminal:
        call["status"] = "declined" if signal_type == CallSignalType.decline else "ended"
        if not await close_call(redis, call):
            raise CallNotFound()
        return call, True

    if signal_type in {CallSignalType.accept, CallSignalType.answer}:
        call["status"] = "active"
        ttl = settings.CALL_ACTIVE_TTL_SECONDS
    else:
        ttl = (
            settings.CALL_ACTIVE_TTL_SECONDS
            if call["status"] == "active"
            else settings.CALL_RING_TTL_SECONDS
        )
    call["expires_at"] = (_now() + timedelta(seconds=ttl)).isoformat()
    updated = await redis.eval(
        _UPDATE_CALL,
        3,
        call_key(uuid.UUID(call["id"])),
        user_call_key(uuid.UUID(call["caller_id"])),
        user_call_key(uuid.UUID(call["callee_id"])),
        _serialize(call),
        ttl,
        call["id"],
    )
    if updated != 1:
        raise CallNotFound()
    return call, False


async def close_call(redis: aioredis.Redis, call: dict) -> bool:
    closed = await redis.eval(
        _CLOSE_CALL,
        3,
        call_key(uuid.UUID(call["id"])),
        user_call_key(uuid.UUID(call["caller_id"])),
        user_call_key(uuid.UUID(call["callee_id"])),
        call["id"],
    )
    return closed == 1
