"""FEED-01 피드 · POST-01~03 게시물·댓글·좋아요."""

import uuid

from app.models import Block, Post
from tests.conftest import auth_header, register


async def _post(client, h, content="테스트 글", *, title=None, category="daily"):
    resp = await client.post(
        "/api/v1/posts",
        json={"title": title or content, "category": category, "content": content},
        headers=h,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def test_text_post_publishes_immediately_and_appears_in_feed(client):
    u = await register(client, "글쓴이")
    h = auth_header(u["access_token"])
    post = await _post(client, h, "첫 글입니다")
    assert post["status"] == "published"
    assert post["title"] == "첫 글입니다"
    assert post["category"] == "daily"

    feed = await client.get("/api/v1/feed", headers=h)
    assert feed.status_code == 200
    items = feed.json()["items"]
    assert [p["content"] for p in items] == ["첫 글입니다"]
    assert items[0]["author"]["nickname"] == "글쓴이"
    assert items[0]["like_count"] == 0 and items[0]["comment_count"] == 0


async def test_processing_draft_excluded_from_feed(client, db):
    u = await register(client, "드래프터")
    h = auth_header(u["access_token"])
    db.add(Post(id=uuid.uuid4(), author_id=uuid.UUID(u["user_id"]),
                content="영상 드래프트", status="processing"))
    await db.commit()
    feed = await client.get("/api/v1/feed", headers=h)
    assert feed.json()["items"] == []


async def test_blocked_users_posts_hidden_both_ways(client, db):
    a = await register(client, "차단자")
    b = await register(client, "피차단자")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    post_b = await _post(client, hb, "B의 글")
    db.add(Block(blocker_id=uuid.UUID(a["user_id"]), blocked_id=uuid.UUID(b["user_id"])))
    await db.commit()

    feed_a = await client.get("/api/v1/feed", headers=ha)
    assert all(p["content"] != "B의 글" for p in feed_a.json()["items"])
    detail = await client.get(f"/api/v1/posts/{post_b['id']}", headers=ha)
    assert detail.status_code == 404
    # 반대 방향도 차단 (B가 A의 글을 못 봄)
    post_a = await _post(client, ha, "A의 글")
    detail_b = await client.get(f"/api/v1/posts/{post_a['id']}", headers=hb)
    assert detail_b.status_code == 404


async def test_edit_delete_requires_author(client):
    a = await register(client, "작성자")
    b = await register(client, "타인")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    post = await _post(client, ha)
    assert (await client.patch(f"/api/v1/posts/{post['id']}", json={"content": "수정"}, headers=hb)).status_code == 403
    assert (await client.delete(f"/api/v1/posts/{post['id']}", headers=hb)).status_code == 403
    assert (await client.patch(f"/api/v1/posts/{post['id']}", json={"content": "수정"}, headers=ha)).status_code == 200
    assert (await client.delete(f"/api/v1/posts/{post['id']}", headers=ha)).status_code == 204


async def test_like_is_idempotent(client):
    u = await register(client, "좋아요유저")
    h = auth_header(u["access_token"])
    post = await _post(client, h)
    for _ in range(2):
        resp = await client.post(f"/api/v1/posts/{post['id']}/like", headers=h)
        assert resp.status_code == 200
        assert resp.json()["like_count"] == 1
    off = await client.delete(f"/api/v1/posts/{post['id']}/like", headers=h)
    assert off.json()["like_count"] == 0


async def test_comment_crud_and_count(client):
    a = await register(client, "댓글작성자")
    h = auth_header(a["access_token"])
    post = await _post(client, h)
    c = await client.post(f"/api/v1/posts/{post['id']}/comments", json={"content": "첫 댓글"}, headers=h)
    assert c.status_code == 201
    comment_id = c.json()["id"]

    listing = await client.get(f"/api/v1/posts/{post['id']}/comments", headers=h)
    assert [x["content"] for x in listing.json()["items"]] == ["첫 댓글"]

    detail = await client.get(f"/api/v1/posts/{post['id']}", headers=h)
    assert detail.json()["comment_count"] == 1

    assert (await client.patch(f"/api/v1/comments/{comment_id}", json={"content": "수정"}, headers=h)).status_code == 200
    assert (await client.delete(f"/api/v1/comments/{comment_id}", headers=h)).status_code == 204


async def test_feed_cursor_pagination(client):
    u = await register(client, "페이지유저")
    h = auth_header(u["access_token"])
    for i in range(5):
        await _post(client, h, f"글{i}")
    page1 = await client.get("/api/v1/feed?limit=2", headers=h)
    assert len(page1.json()["items"]) == 2
    cursor = page1.json()["next_cursor"]
    assert cursor
    page2 = await client.get(f"/api/v1/feed?limit=2&cursor={cursor}", headers=h)
    contents1 = {p["content"] for p in page1.json()["items"]}
    contents2 = {p["content"] for p in page2.json()["items"]}
    assert contents1.isdisjoint(contents2)


async def test_feed_filters_category_and_searches_title_or_content(client):
    user = await register(client, "검색유저")
    headers = auth_header(user["access_token"])
    await _post(client, headers, "라일락 향기를 맡았어요", title="공원 산책", category="daily")
    await _post(client, headers, "도서관 신간 안내", title="이번 주 책", category="info")
    await _post(client, headers, "주말에 함께 걸어요", title="한강 걷기 모임", category="meetup")

    category_feed = await client.get("/api/v1/feed?category=info", headers=headers)
    assert [item["category"] for item in category_feed.json()["items"]] == ["info"]

    title_search = await client.get("/api/v1/feed?q=한강", headers=headers)
    assert [item["title"] for item in title_search.json()["items"]] == ["한강 걷기 모임"]

    content_search = await client.get("/api/v1/feed?q=라일락", headers=headers)
    assert [item["title"] for item in content_search.json()["items"]] == ["공원 산책"]


async def test_post_contract_rejects_missing_or_blank_metadata(client):
    user = await register(client, "계약검증자")
    headers = auth_header(user["access_token"])
    missing = await client.post("/api/v1/posts", json={"content": "본문"}, headers=headers)
    assert missing.status_code == 422
    blank = await client.post(
        "/api/v1/posts",
        json={"title": "   ", "category": "daily", "content": "본문"},
        headers=headers,
    )
    assert blank.status_code == 422
    invalid = await client.post(
        "/api/v1/posts",
        json={"title": "제목", "category": "unknown", "content": "본문"},
        headers=headers,
    )
    assert invalid.status_code == 422
    typo = await client.post(
        "/api/v1/posts",
        json={
            "title": "제목",
            "category": "daily",
            "content": "본문",
            "catgory": "info",
        },
        headers=headers,
    )
    assert typo.status_code == 422


async def test_post_and_comment_input_limits(client):
    user = await register(client, "입력상한유저")
    headers = auth_header(user["access_token"])
    too_long = await client.post(
        "/api/v1/posts",
        json={"title": "긴 글", "category": "daily", "content": "가" * 10001},
        headers=headers,
    )
    assert too_long.status_code == 422
    too_many_media = await client.post(
        "/api/v1/posts",
        json={
            "title": "사진 수",
            "category": "daily",
            "content": "본문",
            "media_ids": [str(uuid.uuid4()) for _ in range(4)],
        },
        headers=headers,
    )
    assert too_many_media.status_code == 422

    post = await _post(client, headers, "댓글 상한 검사")
    for content in ("   ", "댓" * 2001):
        response = await client.post(
            f"/api/v1/posts/{post['id']}/comments",
            json={"content": content},
            headers=headers,
        )
        assert response.status_code == 422
