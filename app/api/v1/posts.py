import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
    description="`image_url`은 선택. 넣을 경우 `POST /upload` 응답 `url`(/uploads/...)을 그대로 사용.",
)
async def create_post(
    body: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = Post(user_id=current_user.id, content=body.content, image_url=body.image_url)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get(
    "",
    response_model=list[PostResponse],
    summary="피드 목록",
    description="최신순. `offset`/`limit`(기본 0/20)로 페이지네이션. 인증 불필요(공개 피드).",
)
async def list_posts(
    offset: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Post).order_by(Post.created_at.desc()).offset(offset).limit(limit)
    )
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostResponse, summary="게시글 단건 조회")
async def get_post(post_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글 삭제",
    description="작성자 본인만 삭제 가능(타인 글은 403).",
)
async def delete_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")
    await db.delete(post)
    await db.commit()
