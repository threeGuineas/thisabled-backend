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


async def test_settings_update(client):
    body = await register(client, "설정유저")
    h = auth_header(body["access_token"])
    resp = await client.patch(
        "/api/v1/users/me/settings",
        json={"stranger_requests_allowed": False, "mode_settings": {"font_scale": 1.5}},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["stranger_requests_allowed"] is False
    assert resp.json()["mode_settings"] == {"font_scale": 1.5}


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
