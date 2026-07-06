"""COMM-01~05 — 쉬운 문장·문장 완성·답장 추천·대화 힌트 (버튼 실행 시에만, 최근 N=10)."""

import pytest_asyncio

from app.main import app
from app.services.comm import get_comm_client
from tests.conftest import auth_header, register
from tests.test_chat import make_friends, _room, _send
from tests.test_safe import safety  # noqa: F401


class FakeComm:
    def __init__(self):
        self.received_context: list[str] | None = None

    async def simplify(self, text):
        return "쉬운 문장입니다"

    async def complete(self, text):
        return [text + " 완성본"]

    async def suggest_replies(self, messages):
        self.received_context = messages
        return ["좋아요!", "고마워요"]

    async def hints(self, messages):
        self.received_context = messages
        return ["인사로 시작해 보세요"]


@pytest_asyncio.fixture
async def comm():
    fake = FakeComm()
    app.dependency_overrides[get_comm_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_comm_client, None)


async def test_simplify_and_complete(client, comm):
    u = await register(client, "코치유저")
    h = auth_header(u["access_token"])
    s = await client.post("/api/v1/comm/simplify", json={"text": "난해한 문장"}, headers=h)
    assert s.json()["result"] == "쉬운 문장입니다"
    assert s.json()["original"] == "난해한 문장"  # 원문 전환 제공 (COMM-01)
    c = await client.post("/api/v1/comm/complete", json={"text": "오늘 날씨가"}, headers=h)
    assert c.json()["suggestions"] == ["오늘 날씨가 완성본"]


async def test_replies_use_last_10_messages_only(client, comm, safety):  # noqa: F811
    a = await register(client, "코치갑")
    b = await register(client, "코치을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    for i in range(12):
        await _send(client, ha, room["id"], f"메시지 {i}")

    resp = await client.post("/api/v1/comm/replies", json={"room_id": room["id"]}, headers=hb)
    assert resp.status_code == 200
    assert resp.json()["suggestions"] == ["좋아요!", "고마워요"]
    assert len(comm.received_context) == 10  # COMM-05 N=10
    assert comm.received_context[-1] == "메시지 11"  # 최근 순서 유지


async def test_replies_exclude_unrevealed_flagged(client, comm, safety):  # noqa: F811
    a = await register(client, "코치위험갑")
    b = await register(client, "코치위험을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    await _send(client, ha, room["id"], "일반 메시지")
    await _send(client, ha, room["id"], "돈 보내라")  # flagged, 미열람

    await client.post("/api/v1/comm/hints", json={"room_id": room["id"]}, headers=hb)
    assert "돈 보내라" not in comm.received_context


async def test_non_participant_rejected(client, comm, safety):  # noqa: F811
    a = await register(client, "참여자갑")
    b = await register(client, "참여자을")
    outsider = await register(client, "외부인")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    resp = await client.post(
        "/api/v1/comm/replies", json={"room_id": room["id"]},
        headers=auth_header(outsider["access_token"]),
    )
    assert resp.status_code == 404
