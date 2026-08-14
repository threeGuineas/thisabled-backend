"""테스트 공용 픽스처.

각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다.
앱 코드가 `await db.commit()` 을 호출해도 join_transaction_mode="create_savepoint"
덕분에 세이브포인트만 해제될 뿐 외부 트랜잭션은 유지 → 테스트 간 완전 격리.
(forbidden_nicknames·interest_tags 시드처럼 이미 커밋된 데이터는 그대로 보인다.)
"""

from urllib.parse import parse_qs, urlsplit

import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
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


@pytest.fixture(autouse=True)
def _isolate_upload_directory(tmp_path, monkeypatch):
    """미디어 테스트가 Docker 전용 기본 경로(`/app/uploads`)에 쓰지 않도록 격리한다."""
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(tmp_path / "uploads"))


def _test_redis_url() -> str:
    # 운영 db(0) 대신 테스트용 db(1) 사용
    base = settings.REDIS_URL.rsplit("/", 1)[0]
    return f"{base}/1"


def _test_database_url() -> str:
    """테스트 전용 DB만 허용한다. 명시값이 없으면 현재 DB명에 `_test`를 붙인다."""
    source = make_url(settings.TEST_DATABASE_URL or settings.DATABASE_URL)
    if settings.TEST_DATABASE_URL is None and source.database:
        database = source.database if source.database.endswith("_test") else f"{source.database}_test"
        source = source.set(database=database)
    if not source.database or not source.database.endswith("_test"):
        raise RuntimeError("테스트 DB 이름은 반드시 _test로 끝나야 합니다")
    return source.render_as_string(hide_password=False)


@pytest_asyncio.fixture
async def _conn():
    engine = create_async_engine(_test_database_url())
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
async def _session(_session_factory):
    async with _session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def db(_session):
    """테스트와 API 요청이 같은 세션을 사용해 중첩 savepoint 간 간섭을 막는다."""
    yield _session


class _BorrowedSession:
    """백그라운드 잡이 테스트 공유 세션을 닫지 않도록 하는 async context manager."""

    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, *_args):
        return None


@pytest_asyncio.fixture
async def test_redis():
    r = aioredis.from_url(_test_redis_url(), decode_responses=True)
    await r.flushdb()
    yield r
    await r.aclose()


@pytest_asyncio.fixture
async def client(_session, test_redis):
    async def override_get_db():
        yield _session

    async def override_get_redis():
        return test_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_session_factory] = lambda: (
        lambda: _BorrowedSession(_session)
    )
    # https: COOKIE_SECURE=true 환경에서도 Secure 쿠키(refresh)가 전송되도록
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as c:
        yield c
    app.dependency_overrides.clear()
    await test_redis.aclose()


def callback_params(resp) -> dict:
    """콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict."""
    assert resp.status_code == 302, resp.text
    location = resp.headers["location"]
    assert location.startswith(settings.FRONTEND_URL), location
    return {k: v[0] for k, v in parse_qs(urlsplit(location).query).items()}


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
    params = callback_params(cb)
    if params["is_new_user"] == "false":
        # 기가입자 — 리다이렉트 쿼리로 전달된 access_token만 보장된다
        return {"is_new_user": False, "access_token": params["access_token"]}
    resp = await client.post(
        "/api/v1/auth/signup",
        json={
            "signup_token": params["signup_token"],
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
