"""FEED-01 홈 피드 · POST-01 게시물 · POST-02 수정/삭제 · POST-03 좋아요/댓글."""

import uuid
from datetime import datetime, timezone
from urllib.parse import quote, unquote

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, or_, select, union
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.enums import MediaType, PostStatus
from app.db.session import get_db
from app.models import Block, Comment, Post, PostLike, PostMedia, User
from app.schemas.post import (
    AuthorOut,
    CommentIn,
    CommentListOut,
    CommentOut,
    FeedOut,
    LikeOut,
    MediaOut,
    PostCreateIn,
    PostOut,
    PostPatchIn,
)

router = APIRouter(tags=["posts"])

MAX_IMAGES = 3  # POST-01

WITHDRAWN_NICKNAME = "탈퇴한 사용자"  # §15


def _blocked_ids_subq(me_id: uuid.UUID):
    """나와 어느 방향이든 차단 관계인 사용자 id (BLOCK-01)."""
    return union(
        select(Block.blocked_id).where(Block.blocker_id == me_id),
        select(Block.blocker_id).where(Block.blocked_id == me_id),
    ).subquery()


async def _is_blocked_author(db: AsyncSession, me_id: uuid.UUID, author_id: uuid.UUID | None) -> bool:
    if author_id is None or author_id == me_id:
        return False
    row = (
        await db.execute(
            select(Block.blocker_id).where(
                or_(
                    (Block.blocker_id == me_id) & (Block.blocked_id == author_id),
                    (Block.blocker_id == author_id) & (Block.blocked_id == me_id),
                )
            )
        )
    ).first()
    return row is not None


def _author_out(user: User | None) -> AuthorOut:
    if user is None:
        return AuthorOut(id=None, nickname=WITHDRAWN_NICKNAME)
    return AuthorOut(id=user.id, nickname=user.nickname, profile_image_url=user.profile_image_url)


async def _serialize_posts(db: AsyncSession, me_id: uuid.UUID, posts: list[Post]) -> list[PostOut]:
    if not posts:
        return []
    ids = [p.id for p in posts]
    authors = {
        u.id: u
        for u in (
            await db.execute(select(User).where(User.id.in_({p.author_id for p in posts if p.author_id})))
        ).scalars()
    }
    media_rows = (
        await db.execute(
            select(PostMedia).where(PostMedia.post_id.in_(ids)).order_by(PostMedia.sort_order)
        )
    ).scalars().all()
    like_counts = dict(
        (await db.execute(
            select(PostLike.post_id, func.count()).where(PostLike.post_id.in_(ids)).group_by(PostLike.post_id)
        )).all()
    )
    comment_counts = dict(
        (await db.execute(
            select(Comment.post_id, func.count()).where(Comment.post_id.in_(ids)).group_by(Comment.post_id)
        )).all()
    )
    my_likes = {
        row[0]
        for row in (
            await db.execute(
                select(PostLike.post_id).where(PostLike.post_id.in_(ids), PostLike.user_id == me_id)
            )
        ).all()
    }
    media_by_post: dict[uuid.UUID, list[MediaOut]] = {}
    for m in media_rows:
        media_by_post.setdefault(m.post_id, []).append(
            MediaOut(
                id=m.id, media_type=m.media_type, url=m.url, sort_order=m.sort_order,
                description=m.description, description_status=m.description_status,
                caption=m.caption, caption_status=m.caption_status,
            )
        )
    return [
        PostOut(
            id=p.id,
            author=_author_out(authors.get(p.author_id)),
            content=p.content,
            status=p.status,
            media=media_by_post.get(p.id, []),
            like_count=like_counts.get(p.id, 0),
            comment_count=comment_counts.get(p.id, 0),
            liked_by_me=p.id in my_likes,
            published_at=p.published_at,
            created_at=p.created_at,
        )
        for p in posts
    ]


@router.post("/posts", response_model=PostOut, status_code=201)
async def create_post(
    body: PostCreateIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """텍스트·사진 게시물 — 게시 실행 즉시 공개 (POST-01). 영상은 /media/videos 드래프트 경로."""
    media: list[PostMedia] = []
    if body.media_ids:
        media = (
            await db.execute(select(PostMedia).where(PostMedia.id.in_(body.media_ids)))
        ).scalars().all()
        if len(media) != len(set(body.media_ids)):
            raise HTTPException(status_code=404, detail="존재하지 않는 미디어가 있습니다")
        for m in media:
            if m.uploader_id != user.id or m.post_id is not None:
                raise HTTPException(status_code=403, detail="사용할 수 없는 미디어입니다")
            if m.media_type == MediaType.video.value:
                raise HTTPException(
                    status_code=400, detail="영상 게시물은 영상 업로드 시 만들어진 드래프트로 게시해 주세요"
                )
        if len(media) > MAX_IMAGES:
            raise HTTPException(status_code=400, detail=f"사진은 최대 {MAX_IMAGES}장까지 첨부할 수 있습니다")

    post = Post(
        id=uuid.uuid4(),
        author_id=user.id,
        content=body.content,
        status=PostStatus.published.value,
        published_at=datetime.now(timezone.utc),
    )
    db.add(post)
    await db.flush()
    for i, m in enumerate(media):
        m.post_id = post.id
        m.sort_order = i
    await db.commit()
    return (await _serialize_posts(db, user.id, [post]))[0]


@router.get("/feed", response_model=FeedOut)
async def feed(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    blocked = _blocked_ids_subq(user.id)
    q = (
        select(Post)
        .where(
            Post.status == PostStatus.published.value,
            or_(Post.author_id.is_(None), Post.author_id.not_in(select(blocked.c[0]))),
        )
        .order_by(Post.published_at.desc(), Post.id.desc())
        .limit(limit + 1)
    )
    if cursor:
        try:
            ts_raw, id_raw = unquote(cursor).split("|", 1)
            cur_ts, cur_id = datetime.fromisoformat(ts_raw), uuid.UUID(id_raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="잘못된 커서입니다")
        q = q.where(
            or_(
                Post.published_at < cur_ts,
                (Post.published_at == cur_ts) & (Post.id < cur_id),
            )
        )
    posts = (await db.execute(q)).scalars().all()
    next_cursor = None
    if len(posts) > limit:
        posts = posts[:limit]
        last = posts[-1]
        next_cursor = quote(f"{last.published_at.isoformat()}|{last.id}")
    return FeedOut(items=await _serialize_posts(db, user.id, posts), next_cursor=next_cursor)


async def _get_visible_post(db: AsyncSession, me: User, post_id: uuid.UUID) -> Post:
    post = await db.get(Post, post_id)
    if post is None or await _is_blocked_author(db, me.id, post.author_id):
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    return post


@router.get("/posts/{post_id}", response_model=PostOut)
async def post_detail(
    post_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = await _get_visible_post(db, user, post_id)
    # 드래프트는 작성자 본인만 (POST-01 내부 드래프트)
    if post.status != PostStatus.published.value and post.author_id != user.id:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    return (await _serialize_posts(db, user.id, [post]))[0]


@router.patch("/posts/{post_id}", response_model=PostOut)
async def edit_post(
    post_id: uuid.UUID,
    body: PostPatchIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = await _get_visible_post(db, user, post_id)
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="작성자만 수정할 수 있습니다")
    post.content = body.content
    await db.commit()
    return (await _serialize_posts(db, user.id, [post]))[0]


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = await _get_visible_post(db, user, post_id)
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="작성자만 삭제할 수 있습니다")
    await db.delete(post)
    await db.commit()


async def _like_count(db: AsyncSession, post_id: uuid.UUID) -> int:
    return (
        await db.execute(select(func.count()).select_from(PostLike).where(PostLike.post_id == post_id))
    ).scalar_one()


@router.post("/posts/{post_id}/like", response_model=LikeOut)
async def like_post(
    post_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_visible_post(db, user, post_id)
    exists = await db.get(PostLike, (post_id, user.id))
    if exists is None:
        db.add(PostLike(post_id=post_id, user_id=user.id))
        await db.commit()
    return LikeOut(post_id=post_id, liked=True, like_count=await _like_count(db, post_id))


@router.delete("/posts/{post_id}/like", response_model=LikeOut)
async def unlike_post(
    post_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_visible_post(db, user, post_id)
    await db.execute(
        delete(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == user.id)
    )
    await db.commit()
    return LikeOut(post_id=post_id, liked=False, like_count=await _like_count(db, post_id))


def _comment_out(c: Comment, author: User | None) -> CommentOut:
    return CommentOut(
        id=c.id, post_id=c.post_id, author=_author_out(author),
        content=c.content, created_at=c.created_at, updated_at=c.updated_at,
    )


@router.get("/posts/{post_id}/comments", response_model=CommentListOut)
async def list_comments(
    post_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_visible_post(db, user, post_id)
    rows = (
        await db.execute(
            select(Comment, User)
            .outerjoin(User, User.id == Comment.author_id)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at)
        )
    ).all()
    return CommentListOut(items=[_comment_out(c, u) for c, u in rows])


@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=201)
async def create_comment(
    post_id: uuid.UUID,
    body: CommentIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_visible_post(db, user, post_id)
    comment = Comment(id=uuid.uuid4(), post_id=post_id, author_id=user.id, content=body.content)
    db.add(comment)
    await db.commit()
    return _comment_out(comment, user)


@router.patch("/comments/{comment_id}", response_model=CommentOut)
async def edit_comment(
    comment_id: uuid.UUID,
    body: CommentIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="작성자만 수정할 수 있습니다")
    comment.content = body.content
    await db.commit()
    await db.refresh(comment)  # updated_at(onupdate)은 서버가 생성 — 만료 상태로 두면 lazy IO
    return _comment_out(comment, user)


@router.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="작성자만 삭제할 수 있습니다")
    await db.delete(comment)
    await db.commit()
