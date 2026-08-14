"""CHAT-05 음성·영상 통화 — Redis 세션, 정책, WebSocket 시그널."""

import json
import uuid

from app.models import SendRestriction
from app.services.events import user_channel
from app.services.presence import mark_online
from tests.conftest import auth_header, register
from tests.test_chat import _room, make_friends


async def _next_event(pubsub):
    for _ in range(5):
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message is not None:
            return json.loads(message["data"])
    raise AssertionError("실시간 통화 이벤트가 전달되지 않았습니다")


async def _friends_with_room(client, test_redis, name_a="통화갑", name_b="통화을"):
    a = await register(client, name_a)
    b = await register(client, name_b)
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    await mark_online(test_redis, uuid.UUID(b["user_id"]))
    return a, b, ha, hb, room


async def test_call_invite_signal_lifecycle_and_participant_privacy(client, test_redis):
    a, b, ha, hb, room = await _friends_with_room(client, test_redis)
    outsider = await register(client, "통화외부인")
    ho = auth_header(outsider["access_token"])
    pubsub = test_redis.pubsub()
    await pubsub.subscribe(user_channel(b["user_id"]))
    try:
        started = await client.post(
            f"/api/v1/chat/rooms/{room['id']}/calls",
            json={"kind": "video"},
            headers=ha,
        )
        assert started.status_code == 201, started.text
        call = started.json()
        assert call["status"] == "ringing"
        assert call["kind"] == "video"
        invited = await _next_event(pubsub)
        assert invited["type"] == "call.invited"
        assert invited["payload"]["id"] == call["id"]

        busy = await client.post(
            f"/api/v1/chat/rooms/{room['id']}/calls",
            json={"kind": "audio"},
            headers=ha,
        )
        assert busy.status_code == 409
        assert (await client.get(f"/api/v1/chat/calls/{call['id']}", headers=hb)).status_code == 200
        assert (await client.get(f"/api/v1/chat/calls/{call['id']}", headers=ho)).status_code == 404

        offer = await client.post(
            f"/api/v1/chat/calls/{call['id']}/signals",
            json={"type": "offer", "data": {"sdp": "offer-sdp"}},
            headers=ha,
        )
        assert offer.status_code == 202
        signal_event = await _next_event(pubsub)
        assert signal_event == {
            "type": "call.signal",
            "payload": {
                "call_id": call["id"],
                "room_id": room["id"],
                "from_user_id": a["user_id"],
                "signal": "offer",
                "data": {"sdp": "offer-sdp"},
            },
        }
        accepted = await client.post(
            f"/api/v1/chat/calls/{call['id']}/signals",
            json={"type": "accept"},
            headers=hb,
        )
        assert accepted.json()["status"] == "active"
        answer = await client.post(
            f"/api/v1/chat/calls/{call['id']}/signals",
            json={"type": "answer", "data": {"sdp": "answer-sdp"}},
            headers=hb,
        )
        assert answer.status_code == 202
        ended = await client.post(
            f"/api/v1/chat/calls/{call['id']}/signals",
            json={"type": "end"},
            headers=ha,
        )
        assert ended.json()["status"] == "ended"
        assert (await client.get(f"/api/v1/chat/calls/{call['id']}", headers=ha)).status_code == 404
        restarted = await client.post(
            f"/api/v1/chat/rooms/{room['id']}/calls",
            json={"kind": "audio"},
            headers=ha,
        )
        assert restarted.status_code == 201
    finally:
        await pubsub.unsubscribe(user_channel(b["user_id"]))
        await pubsub.aclose()


async def test_call_requires_online_active_same_age_friend(client, test_redis):
    a = await register(client, "통화정책갑", birth="1990-01-01")
    b = await register(client, "통화정책을", birth="1991-01-01")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()
    offline = await client.post(
        f"/api/v1/chat/rooms/{room['id']}/calls", json={"kind": "audio"}, headers=ha
    )
    assert offline.status_code == 409

    stranger = await register(client, "통화낯선이")
    hs = auth_header(stranger["access_token"])
    request_room = (await _room(client, hs, b["user_id"])).json()
    await mark_online(test_redis, uuid.UUID(b["user_id"]))
    request_call = await client.post(
        f"/api/v1/chat/rooms/{request_room['id']}/calls",
        json={"kind": "audio"},
        headers=hs,
    )
    assert request_call.status_code == 403

    minor = await register(client, "통화미성년", birth="2010-01-01")
    hm = auth_header(minor["access_token"])
    await make_friends(client, ha, hm, minor["user_id"])
    mixed_room = (await _room(client, ha, minor["user_id"])).json()
    await mark_online(test_redis, uuid.UUID(minor["user_id"]))
    mixed = await client.post(
        f"/api/v1/chat/rooms/{mixed_room['id']}/calls",
        json={"kind": "video"},
        headers=ha,
    )
    assert mixed.status_code == 403


async def test_call_rejects_restriction_invalid_role_and_oversized_signal(
    client, test_redis, db
):
    a, b, ha, hb, room = await _friends_with_room(
        client, test_redis, "통화제한갑", "통화제한을"
    )
    restriction = SendRestriction(
        id=uuid.uuid4(),
        sender_id=uuid.UUID(a["user_id"]),
        receiver_id=uuid.UUID(b["user_id"]),
    )
    db.add(restriction)
    await db.commit()
    restricted = await client.post(
        f"/api/v1/chat/rooms/{room['id']}/calls", json={"kind": "audio"}, headers=ha
    )
    assert restricted.status_code == 403

    restriction.active = False
    await db.commit()
    started = await client.post(
        f"/api/v1/chat/rooms/{room['id']}/calls", json={"kind": "audio"}, headers=ha
    )
    assert started.status_code == 201
    call_id = started.json()["id"]
    invalid_role = await client.post(
        f"/api/v1/chat/calls/{call_id}/signals",
        json={"type": "accept"},
        headers=ha,
    )
    assert invalid_role.status_code == 409
    oversized = await client.post(
        f"/api/v1/chat/calls/{call_id}/signals",
        json={"type": "ice", "data": {"candidate": "x" * 40000}},
        headers=hb,
    )
    assert oversized.status_code == 413
