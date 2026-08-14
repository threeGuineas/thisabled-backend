"""ACC-03 프로필 · TAG-01 태그 · §15 설정 · §5.2 모드 변경."""

from sqlalchemy import func, select

from app.models import UserModeHistory
from tests.conftest import auth_header, register


async def test_me_includes_profile_and_derived_minor(client):
    body = await register(client, "나조회", birth="2010-01-01")
    resp = await client.get("/api/v1/users/me", headers=auth_header(body["access_token"]))
    assert resp.status_code == 200
    me = resp.json()
    assert me["nickname"] == "나조회"
    assert me["is_minor"] is True
    assert me["ui_mode"] == "visual"
    assert me["tags"] == []
    assert me["stats"] == {
        "post_count": 0,
        "comment_count": 0,
        "received_like_count": 0,
    }
    assert me["notification_settings"] == {
        "friend_activity": True,
        "post_activity": True,
        "chat_activity": True,
        "ai_results": True,
    }


async def test_patch_me_rejects_contact_in_bio(client):
    body = await register(client, "연락처검사")
    h = auth_header(body["access_token"])
    for bad in ["연락줘 010-1234-5678", "메일 me@example.com 으로", "카톡 아이디 abc123"]:
        resp = await client.patch("/api/v1/users/me", json={"bio": bad}, headers=h)
        assert resp.status_code == 400, bad
    ok = await client.patch("/api/v1/users/me", json={"bio": "영화와 야구를 좋아해요"}, headers=h)
    assert ok.status_code == 200
    assert ok.json()["bio"] == "영화와 야구를 좋아해요"


async def test_tags_catalog_and_replace(client):
    body = await register(client, "태그유저")
    h = auth_header(body["access_token"])
    catalog = await client.get("/api/v1/tags")
    assert catalog.status_code == 200
    codes = [t["code"] for t in catalog.json()["tags"]]
    assert len(codes) == 43 and "walking" in codes

    resp = await client.put("/api/v1/users/me/tags", json={"tag_codes": codes[:10]}, headers=h)
    assert resp.status_code == 200
    assert len(resp.json()["tags"]) == 10

    too_many = await client.put("/api/v1/users/me/tags", json={"tag_codes": codes[:11]}, headers=h)
    assert too_many.status_code == 400

    unknown = await client.put("/api/v1/users/me/tags", json={"tag_codes": ["없는코드"]}, headers=h)
    assert unknown.status_code == 404


async def test_mode_change_records_history(client, db):
    body = await register(client, "모드변경", mode="visual")
    h = auth_header(body["access_token"])
    resp = await client.put("/api/v1/users/me/mode", json={"ui_mode": "hearing"}, headers=h)
    assert resp.status_code == 200
    assert resp.json()["ui_mode"] == "hearing"
    count = (
        await db.execute(select(func.count()).select_from(UserModeHistory))
    ).scalar_one()
    assert count == 1


async def test_default_mode_is_accepted_at_signup_and_mode_change(client):
    body = await register(client, "기본모드", mode="default")
    h = auth_header(body["access_token"])
    assert (await client.get("/api/v1/users/me", headers=h)).json()["ui_mode"] == "default"
    changed = await client.put("/api/v1/users/me/mode", json={"ui_mode": "visual"}, headers=h)
    assert changed.status_code == 200


async def test_settings_update(client):
    body = await register(client, "설정유저")
    h = auth_header(body["access_token"])
    resp = await client.patch(
        "/api/v1/users/me/settings",
        json={
            "stranger_requests_allowed": False,
            "mode_settings": {"font_scale": 1.5},
            "notification_settings": {"post_activity": False},
        },
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["stranger_requests_allowed"] is False
    assert resp.json()["mode_settings"] == {"font_scale": 1.5}
    assert resp.json()["notification_settings"] == {
        "friend_activity": True,
        "post_activity": False,
        "chat_activity": True,
        "ai_results": True,
    }

    invalid = await client.patch(
        "/api/v1/users/me/settings",
        json={"notification_settings": {"unknown_group": False}},
        headers=h,
    )
    assert invalid.status_code == 422


async def test_public_profile_hides_mode_and_birth(client):
    a = await register(client, "공개프로필")
    b = await register(client, "조회자")
    resp = await client.get(
        f"/api/v1/users/{a['user_id']}", headers=auth_header(b["access_token"])
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["nickname"] == "공개프로필"
    assert "ui_mode" not in body
    assert "birth_date" not in body
    assert "is_minor" not in body
    assert body["relationship"] == {"status": "none", "request_id": None}


async def test_profile_activity_relationship_and_authored_posts(client):
    author = await register(client, "활동작성자")
    viewer = await register(client, "활동조회자")
    ha = auth_header(author["access_token"])
    hv = auth_header(viewer["access_token"])
    post = (
        await client.post(
            "/api/v1/posts",
            json={"title": "작성한 게시물", "category": "daily", "content": "프로필에서 보여요"},
            headers=ha,
        )
    ).json()
    await client.post(
        f"/api/v1/posts/{post['id']}/comments", json={"content": "작성자의 댓글"}, headers=ha
    )
    await client.post(f"/api/v1/posts/{post['id']}/like", headers=hv)

    profile = await client.get(f"/api/v1/users/{author['user_id']}", headers=hv)
    assert profile.json()["stats"] == {
        "post_count": 1,
        "comment_count": 1,
        "received_like_count": 1,
    }
    posts = await client.get(f"/api/v1/users/{author['user_id']}/posts", headers=hv)
    assert [item["title"] for item in posts.json()["items"]] == ["작성한 게시물"]

    request = await client.post(
        "/api/v1/friends/requests",
        json={"receiver_id": author["user_id"]},
        headers=hv,
    )
    sent = await client.get(f"/api/v1/users/{author['user_id']}", headers=hv)
    assert sent.json()["relationship"] == {
        "status": "request_sent",
        "request_id": request.json()["id"],
    }
    received = await client.get(f"/api/v1/users/{viewer['user_id']}", headers=ha)
    assert received.json()["relationship"]["status"] == "request_received"

    await client.post(
        f"/api/v1/friends/requests/{request.json()['id']}/accept", headers=ha
    )
    friends = await client.get(f"/api/v1/users/{author['user_id']}", headers=hv)
    assert friends.json()["relationship"] == {"status": "friends", "request_id": None}
