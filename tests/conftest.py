"""테스트 공용 픽스처.

각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다.
앱 코드가 `await db.commit()` 을 호출해도 join_transaction_mode="create_savepoint"
덕분에 세이브포인트만 해제될 뿐 외부 트랜잭션은 유지 → 테스트 간 완전 격리.
(forbidden_nicknames·interest_tags 시드처럼 이미 커밋된 데이터는 그대로 보인다.)
"""

import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import app.models  # noqa: F401 — ORM 모델 등록
from app.core.config import settings
from app.db.redis import get_redis
from app.db.session import get_db, get_session_factory
from app.main import app


@pytest.fixture(autouse=True)
def _force_oauth_mock():
    """.env의 실키·OAUTH_MOCK=false는 배포용 — 테스트는 항상 mock 제공자로 결정론적으로 실행한다.
    개별 테스트(test_oauth_real)가 monkeypatch로 다시 False를 켜는 것은 정상 동작."""
    original = settings.OAUTH_MOCK
    settings.OAUTH_MOCK = True
    yield
    settings.OAUTH_MOCK = original


def _test_redis_url() -> str:
    # 운영 db(0) 대신 테스트용 db(1) 사용
    base = settings.REDIS_URL.rsplit("/", 1)[0]
    return f"{base}/1"


@pytest_asyncio.fixture
async def _conn():
    engine = create_async_engine(settings.DATABASE_URL)
    connection = await engine.connect()
    trans = await connection.begin()
    yield connection
    await trans.rollback()
    await connection.close()
    await engine.dispose()


@pytest_asyncio.fixture
async def _session_factory(_conn):
    return async_sessionmaker(
        bind=_conn,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )


@pytest_asyncio.fixture
async def db(_session_factory):
    """테스트가 직접 DB를 만질 때 사용 — client와 같은 커넥션을 공유한다."""
    async with _session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def test_redis():
    r = aioredis.from_url(_test_redis_url(), decode_responses=True)
    await r.flushdb()
    yield r
    await r.aclose()


@pytest_asyncio.fixture
async def client(_session_factory, test_redis):
    async def override_get_db():
        async with _session_factory() as session:
            yield session

    async def override_get_redis():
        return test_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_session_factory] = lambda: _session_factory
    # https: COOKIE_SECURE=true 환경에서도 Secure 쿠키(refresh)가 전송되도록
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as c:
        yield c
    app.dependency_overrides.clear()
    await test_redis.aclose()


async def register(
    client: AsyncClient,
    nickname: str,
    *,
    uid: str | None = None,
    birth: str = "2000-01-01",
    mode: str = "visual",
) -> dict:
    """mock OAuth 가입 헬퍼 → {access_token, user_id, ...}."""
    cb = await client.get(f"/api/v1/auth/mock/callback?code=mock:{uid or nickname}")
    assert cb.status_code == 200, cb.text
    body = cb.json()
    if not body["is_new_user"]:
        return body
    resp = await client.post(
        "/api/v1/auth/signup",
        json={
            "signup_token": body["signup_token"],
            "nickname": nickname,
            "birth_date": birth,
            "ui_mode": mode,
            "agreements": {"terms": True, "privacy": True, "ai_notice": True},
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
