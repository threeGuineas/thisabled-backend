"""F02 적응형 UI 모드 명세 검증."""

from tests.conftest import auth_header, register


async def test_get_mode_default(client):
    data = await register(client, "modeuser1")
    resp = await client.get(
        "/api/v1/users/me/mode", headers=auth_header(data["access_token"])
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "default"
    assert body["settings"]["font_scale"] == 1.0


async def test_put_mode_visual_returns_settings(client):
    data = await register(client, "modeuser2")
    resp = await client.put(
        "/api/v1/users/me/mode",
        json={"mode": "visual"},
        headers=auth_header(data["access_token"]),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "visual"
    assert body["settings"]["high_contrast"] is True
    assert body["settings"]["tts"] is True
    assert body["changed_at"] is not None


async def test_put_mode_persists(client):
    data = await register(client, "modeuser3")
    headers = auth_header(data["access_token"])
    await client.put("/api/v1/users/me/mode", json={"mode": "developmental"}, headers=headers)
    resp = await client.get("/api/v1/users/me/mode", headers=headers)
    assert resp.json()["mode"] == "developmental"
    assert resp.json()["settings"]["simplified"] is True


async def test_put_mode_invalid_value(client):
    data = await register(client, "modeuser4")
    resp = await client.put(
        "/api/v1/users/me/mode",
        json={"mode": "telepathy"},
        headers=auth_header(data["access_token"]),
    )
    assert resp.status_code == 422


async def test_put_mode_requires_auth(client):
    resp = await client.put("/api/v1/users/me/mode", json={"mode": "visual"})
    assert resp.status_code == 401
