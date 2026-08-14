import asyncio
from weakref import WeakKeyDictionary

import redis.asyncio as aioredis

from app.core.config import settings

_clients: WeakKeyDictionary[asyncio.AbstractEventLoop, aioredis.Redis] = WeakKeyDictionary()


def get_redis_client() -> aioredis.Redis:
    """현재 이벤트 루프 전용 클라이언트.

    asyncio Redis 연결을 다른 루프에서 재사용하면 Future/transport가 깨지므로
    TestClient 재생성·워커 수명 주기에서도 루프 경계를 보존한다.
    """
    loop = asyncio.get_running_loop()
    client = _clients.get(loop)
    if client is None:
        client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        _clients[loop] = client
    return client


async def get_redis() -> aioredis.Redis:
    """FastAPI 의존성. 테스트에서 override 가능하도록 분리."""
    return get_redis_client()
