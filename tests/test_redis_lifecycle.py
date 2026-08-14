"""이벤트 루프별 Redis 클라이언트 생성·종료 수명주기."""

from app.db import redis as redis_module


async def test_current_loop_redis_client_is_reused_and_closed(monkeypatch):
    created = []

    class FakeRedis:
        closed = False

        async def aclose(self):
            self.closed = True

    def create(*_args, **_kwargs):
        client = FakeRedis()
        created.append(client)
        return client

    await redis_module.close_redis_client()
    monkeypatch.setattr(redis_module.aioredis, "from_url", create)
    first = redis_module.get_redis_client()
    assert redis_module.get_redis_client() is first
    await redis_module.close_redis_client()
    assert first.closed is True
    assert redis_module.get_redis_client() is not first
    await redis_module.close_redis_client()
