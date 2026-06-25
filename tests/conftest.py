"""테스트 공용 픽스처.

각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다.
앱 코드가 `await db.commit()` 을 호출해도 join_transaction_mode="create_savepoint"
덕분에 세이브포인트만 해제될 뿐 외부 트랜잭션은 유지 → 테스트 간 완전 격리.
(forbidden_nicknames 시드처럼 이미 커밋된 데이터는 그대로 보인다.)
"""

import pytest_asyncio
import redis.asyncio as aioredis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import app.models  # noqa: F401 — ORM 모델 등록
from app.core.config import settings
from app.db.redis import get_redis
from app.db.session import get_db
from app.main import app


def _test_redis_url() -> str:
    # 운영 db(0) 대신 테스트용 db(1) 사용
    base = settings.REDIS_URL.rsplit("/", 1)[0]
    return f"{base}/1"


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(settings.DATABASE_URL)
    connection = await engine.connect()
    trans = await connection.begin()

    TestSession = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async def override_get_db():
        async with TestSession() as session:
            yield session

    test_redis = aioredis.from_url(_test_redis_url(), decode_responses=True)
    await test_redis.flushdb()

    async def override_get_redis():
        return test_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

    await test_redis.aclose()
    await trans.rollback()
    await connection.close()
    await engine.dispose()


async def register(client: AsyncClient, nickname: str, password: str = "pass1234") -> dict:
    """가입 헬퍼 → signup 응답 JSON 반환 (access_token, user_id, recovery_code)."""
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": nickname, "password": password}
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
