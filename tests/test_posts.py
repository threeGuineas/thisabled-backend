"""게시글 CRUD (UUID) 검증."""

import uuid

from tests.conftest import auth_header, register


async def test_create_and_get_post(client):
    data = await register(client, "poster1")
    headers = auth_header(data["access_token"])

    created = await client.post(
        "/api/v1/posts", json={"content": "첫 게시글"}, headers=headers
    )
    assert created.status_code == 201
    post = created.json()
    # id 가 UUID 형식인지 확인
    uuid.UUID(post["id"])
    assert post["user_id"] == data["user_id"]

    fetched = await client.get(f"/api/v1/posts/{post['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["content"] == "첫 게시글"


async def test_list_posts(client):
    data = await register(client, "poster2")
    headers = auth_header(data["access_token"])
    await client.post("/api/v1/posts", json={"content": "a"}, headers=headers)
    await client.post("/api/v1/posts", json={"content": "b"}, headers=headers)

    resp = await client.get("/api/v1/posts")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


async def test_create_post_requires_auth(client):
    resp = await client.post("/api/v1/posts", json={"content": "익명"})
    assert resp.status_code == 401


async def test_get_missing_post_404(client):
    resp = await client.get(f"/api/v1/posts/{uuid.uuid4()}")
    assert resp.status_code == 404


async def test_delete_own_post(client):
    data = await register(client, "poster3")
    headers = auth_header(data["access_token"])
    created = await client.post("/api/v1/posts", json={"content": "삭제대상"}, headers=headers)
    pid = created.json()["id"]

    deleted = await client.delete(f"/api/v1/posts/{pid}", headers=headers)
    assert deleted.status_code == 204
    assert (await client.get(f"/api/v1/posts/{pid}")).status_code == 404


async def test_delete_others_post_forbidden(client):
    owner = await register(client, "owner1")
    created = await client.post(
        "/api/v1/posts", json={"content": "남의 글"}, headers=auth_header(owner["access_token"])
    )
    pid = created.json()["id"]

    intruder = await register(client, "intruder1")
    resp = await client.delete(
        f"/api/v1/posts/{pid}", headers=auth_header(intruder["access_token"])
    )
    assert resp.status_code == 403
