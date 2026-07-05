"""SAFE-01~05 — 동기 분석·블러·내용 보기·성능저하 모드·관계 단위 전송 제한."""

import pytest_asyncio

from app.main import app
from app.services.safety import SafetyUnavailable, get_safety_client
from tests.conftest import auth_header, register
from tests.test_chat import FakeSafety, make_friends, _room, _send


@pytest_asyncio.fixture
async def safety():
    fake = FakeSafety()
    app.dependency_overrides[get_safety_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_safety_client, None)


async def _friend_room(client, n1, n2):
    a = await register(client, n1)
    b = await register(client, n2)
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    return a, ha, b, hb, room["id"]


async def test_flagged_message_blurred_until_reveal(client, safety):
    a, ha, b, hb, room_id = await _friend_room(client, "위험발신", "위험수신")
    sent = await _send(client, ha, room_id, "돈 좀 보내줘")
    assert sent.status_code == 201
    assert sent.json()["safety_status"] is None  # 발신자 비노출

    msgs = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)).json()
    m = msgs["items"][0]
    assert m["safety_status"] == "flagged"
    assert m["blurred"] is True and m["content"] is None  # 블러 (SAFE-03)

    reveal = await client.post(f"/api/v1/chat/messages/{m['id']}/reveal", headers=hb)
    assert reveal.status_code == 200
    assert reveal.json()["content"] == "돈 좀 보내줘"

    again = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)).json()
    assert again["items"][0]["blurred"] is False

    # 발신자 자신의 목록에서는 원문 그대로, 판정 없음
    mine = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=ha)).json()
    assert mine["items"][0]["content"] == "돈 좀 보내줘"
    assert mine["items"][0]["safety_status"] is None


async def test_degraded_mode_friend_vs_request(client, safety):
    # 친구: unanalyzed로 전달 (§18.3 성능저하 모드)
    a, ha, b, hb, room_id = await _friend_room(client, "장애발신", "장애수신")
    safety.fail = True
    sent = await _send(client, ha, room_id, "모델 죽었을 때 메시지")
    assert sent.status_code == 201
    msgs = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)).json()
    assert msgs["items"][0]["safety_status"] == "unanalyzed"
    assert msgs["items"][0]["content"] == "모델 죽었을 때 메시지"  # 전달은 유지

    # 비친구 요청: pending 보류 — 요청함에 표시되지 않음 (동기 원칙 유지)
    c = await register(client, "보류발신")
    d = await register(client, "보류수신")
    hc, hd = auth_header(c["access_token"]), auth_header(d["access_token"])
    req_room = (await _room(client, hc, d["user_id"])).json()
    held = await _send(client, hc, req_room["id"], "안전 확인 중 메시지")
    assert held.status_code == 201
    inbox = await client.get("/api/v1/chat/requests", headers=hd)
    assert inbox.json()["items"] == []  # 분석 완료 전 비표시


async def test_safe05_restriction_cycle(client, safety):
    a, ha, b, hb, room_id = await _friend_room(client, "누적발신", "누적수신")

    for i in range(3):  # 최근 3일 내 주의 3회 누적
        assert (await _send(client, ha, room_id, f"돈 보내라 {i}")).status_code == 201

    fourth = await _send(client, ha, room_id, "정상 인사")
    assert fourth.status_code == 403
    assert fourth.json()["detail"] == "메시지를 보낼 수 없습니다"  # 사유 비노출 (SAFE-05-4)

    # 수신자에게는 제한 상태 노출
    room_info = (await client.get("/api/v1/chat/rooms", headers=hb)).json()["items"][0]
    assert room_info["restricted_sender"] is True

    # 수신자가 직접 해제 → 카운터 리셋 (SAFE-05-7)
    release = await client.post(f"/api/v1/chat/restrictions/{a['user_id']}/release", headers=hb)
    assert release.status_code == 200
    assert (await _send(client, ha, room_id, "다시 인사")).status_code == 201

    # 해제 후 다시 3회 누적 → 재제한 (SAFE-05 예외 처리)
    for i in range(3):
        assert (await _send(client, ha, room_id, f"또 돈 얘기 {i}")).status_code == 201
    assert (await _send(client, ha, room_id, "재차 시도")).status_code == 403


async def test_reveal_still_counts_for_safe05(client, safety):
    """수신자가 '내용 보기'를 실행한 메시지도 누적 집계에 포함 (SAFE-05-6)."""
    a, ha, b, hb, room_id = await _friend_room(client, "열람발신", "열람수신")
    for i in range(3):
        await _send(client, ha, room_id, f"돈 필요해 {i}")
        msgs = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)).json()
        newest = msgs["items"][0]
        if newest["blurred"]:
            await client.post(f"/api/v1/chat/messages/{newest['id']}/reveal", headers=hb)
    assert (await _send(client, ha, room_id, "인사")).status_code == 403


async def test_block_overrides_restriction(client, safety):
    a, ha, b, hb, room_id = await _friend_room(client, "차단발신", "차단수신")
    await client.post("/api/v1/blocks", json={"user_id": a["user_id"]}, headers=hb)
    resp = await _send(client, ha, room_id, "차단 후 메시지")
    assert resp.status_code in (403, 404)  # BLOCK-01 우선
