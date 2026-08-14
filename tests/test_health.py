"""헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다."""

from app.api.v1 import health as health_module


class _Connection:
    def __init__(self, error: Exception | None = None):
        self.error = error

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def execute(self, _query):
        if self.error:
            raise self.error


class _Engine:
    def __init__(self, error: Exception | None = None):
        self.error = error

    def connect(self):
        return _Connection(self.error)


class _Redis:
    def __init__(self, error: Exception | None = None):
        self.error = error
        self.closed = False

    async def ping(self):
        if self.error:
            raise self.error

    async def aclose(self):
        self.closed = True


async def test_health_ok(client, monkeypatch):
    redis = _Redis()
    monkeypatch.setattr(health_module, "engine", _Engine())
    monkeypatch.setattr(health_module.aioredis, "from_url", lambda *_a, **_kw: redis)

    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok", "redis": "ok"}
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert redis.closed is True


async def test_health_degraded_is_503_and_hides_exception(client, monkeypatch):
    redis = _Redis(RuntimeError("redis://secret@host"))
    monkeypatch.setattr(health_module, "engine", _Engine(RuntimeError("db-password")))
    monkeypatch.setattr(health_module.aioredis, "from_url", lambda *_a, **_kw: redis)

    response = await client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "db": "error", "redis": "error"}
    assert "secret" not in response.text
    assert "password" not in response.text
    assert redis.closed is True
