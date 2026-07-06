"""MATCH — 후보 제외 규칙은 백엔드 강제, 점수·사유는 모델 서버 (mock/fake)."""

import uuid

import pytest_asyncio
from sqlalchemy import insert

from app.main import app
from app.models import Block, FriendRequest
from app.services.match import get_match_client
from tests.conftest import auth_header, register
from tests.test_chat import make_friends


class FakeMatch:
    def __init__(self):
        self.received: list[dict] = []

    async def score(self, me_features: dict, candidates: list[dict]) -> list[dict]:
        self.received = candidates
        return [
            {
                "user_id": c["user_id"],
                "score": 0.9,
                "reasons": ["관심사가 비슷해요", "시각장애 모드가 같아요"],  # 뒤엣것은 필터돼야 함
            }
            for c in candidates
        ]


@pytest_asyncio.fixture
async def match():
    fake = FakeMatch()
    app.dependency_overrides[get_match_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_match_client, None)


async def test_exclusion_rules_enforced_by_backend(client, db, match):
    me = await register(client, "추천기준", birth="1995-01-01")
    h = auth_header(me["access_token"])
    normal = await register(client, "정상후보", birth="1996-01-01")
    friend = await register(client, "이미친구", birth="1995-06-01")
    blocked = await register(client, "차단상대", birth="1995-06-01")
    declined = await register(client, "거절상대", birth="1995-06-01")
    minor = await register(client, "미성년후보", birth="2010-01-01")

    hf = auth_header(friend["access_token"])
    await make_friends(client, h, hf, friend["user_id"])
    await db.execute(insert(Block).values(
        blocker_id=uuid.UUID(me["user_id"]), blocked_id=uuid.UUID(blocked["user_id"])))
    await db.execute(insert(FriendRequest).values(
        id=uuid.uuid4(), sender_id=uuid.UUID(me["user_id"]),
        receiver_id=uuid.UUID(declined["user_id"]), status="declined",
        responded_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc)))
    await db.commit()

    resp = await client.get("/api/v1/recommendations", headers=h)
    assert resp.status_code == 200
    got_ids = {c["user_id"] for c in match.received}
    assert normal["user_id"] in got_ids
    assert friend["user_id"] not in got_ids  # 이미 친구 제외
    assert blocked["user_id"] not in got_ids  # 차단 제외
    assert declined["user_id"] not in got_ids  # 거절 후 30일 제외
    assert minor["user_id"] not in got_ids  # 미성년↔성인 상호 제외 (§4.5)


async def test_reasons_never_expose_mode(client, match):
    me = await register(client, "사유검사", birth="1995-01-01")
    await register(client, "사유후보", birth="1996-01-01")
    resp = await client.get("/api/v1/recommendations", headers=auth_header(me["access_token"]))
    for item in resp.json()["items"]:
        for reason in item["reasons"]:
            assert "장애" not in reason and "모드" not in reason  # MATCH-04


async def test_empty_pool_message(client, match):
    me = await register(client, "혼자유저", birth="1995-01-01")
    resp = await client.get("/api/v1/recommendations", headers=auth_header(me["access_token"]))
    assert resp.json()["items"] == []
    assert resp.json()["message"] == "추천 정보가 부족합니다"
