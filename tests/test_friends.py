"""FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단."""

from tests.conftest import auth_header, register


async def _pair(client, n1="갑돌이", n2="을순이"):
    a = await register(client, n1)
    b = await register(client, n2)
    return a, auth_header(a["access_token"]), b, auth_header(b["access_token"])


async def _request(client, h, receiver_id):
    return await client.post("/api/v1/friends/requests", json={"receiver_id": receiver_id}, headers=h)


async def test_request_accept_creates_mutual_friendship(client):
    a, ha, b, hb = await _pair(client)
    req = await _request(client, ha, b["user_id"])
    assert req.status_code == 201, req.text
    req_id = req.json()["id"]

    inbox = await client.get("/api/v1/friends/requests?box=received", headers=hb)
    assert [r["id"] for r in inbox.json()["items"]] == [req_id]

    accept = await client.post(f"/api/v1/friends/requests/{req_id}/accept", headers=hb)
    assert accept.status_code == 200

    for h in (ha, hb):  # 양방향 친구 (FRIEND-01)
        friends = await client.get("/api/v1/friends", headers=h)
        assert len(friends.json()["items"]) == 1


async def test_decline_records_and_duplicate_pending_rejected(client):
    a, ha, b, hb = await _pair(client, "병만이", "정만이")
    req = await _request(client, ha, b["user_id"])
    dup = await _request(client, ha, b["user_id"])
    assert dup.status_code == 400  # pending 중복

    decline = await client.post(f"/api/v1/friends/requests/{req.json()['id']}/decline", headers=hb)
    assert decline.status_code == 200
    assert decline.json()["status"] == "declined"
    assert decline.json()["responded_at"] is not None  # 30일 추천 제외 근거 (MATCH-03)


async def test_cancel_only_by_sender(client):
    a, ha, b, hb = await _pair(client, "무돌이", "기돌이")
    req = await _request(client, ha, b["user_id"])
    req_id = req.json()["id"]
    assert (await client.post(f"/api/v1/friends/requests/{req_id}/cancel", headers=hb)).status_code == 403
    assert (await client.post(f"/api/v1/friends/requests/{req_id}/cancel", headers=ha)).status_code == 200


async def test_unfriend(client):
    a, ha, b, hb = await _pair(client, "경순이", "신순이")
    req = await _request(client, ha, b["user_id"])
    await client.post(f"/api/v1/friends/requests/{req.json()['id']}/accept", headers=hb)
    resp = await client.delete(f"/api/v1/friends/{b['user_id']}", headers=ha)
    assert resp.status_code == 204
    assert (await client.get("/api/v1/friends", headers=hb)).json()["items"] == []


async def test_block_removes_friendship_and_hides_everything(client):
    a, ha, b, hb = await _pair(client, "임오", "계미")
    req = await _request(client, ha, b["user_id"])
    await client.post(f"/api/v1/friends/requests/{req.json()['id']}/accept", headers=hb)

    block = await client.post("/api/v1/blocks", json={"user_id": b["user_id"]}, headers=ha)
    assert block.status_code == 201

    # 친구 해제 (BLOCK-01)
    assert (await client.get("/api/v1/friends", headers=ha)).json()["items"] == []
    # 프로필 상호 숨김
    assert (await client.get(f"/api/v1/users/{b['user_id']}", headers=ha)).status_code == 404
    assert (await client.get(f"/api/v1/users/{a['user_id']}", headers=hb)).status_code == 404
    # 차단 상대에게 친구 요청 — 사유 비노출 통일 메시지
    retry = await _request(client, hb, a["user_id"])
    assert retry.status_code == 404
    assert retry.json()["detail"] == "요청을 보낼 수 없는 상대입니다"

    # 차단 해제
    assert (await client.delete(f"/api/v1/blocks/{b['user_id']}", headers=ha)).status_code == 204
    assert (await client.get(f"/api/v1/users/{b['user_id']}", headers=ha)).status_code == 200


async def test_self_request_rejected(client):
    a = await register(client, "자기자신")
    resp = await _request(client, auth_header(a["access_token"]), a["user_id"])
    assert resp.status_code == 400
