"""게시물 제목·단일 카테고리와 피드 조회 인덱스 추가.

Revision ID: c2d4e6f8a0b1
Revises: a31f5b6c8d9e
"""

from alembic import op
import sqlalchemy as sa


revision = "c2d4e6f8a0b1"
down_revision = "a31f5b6c8d9e"
branch_labels = None
depends_on = None


POST_CATEGORIES = ("daily", "info", "hobby", "concern", "meetup")


def upgrade() -> None:
    op.add_column("posts", sa.Column("title", sa.String(length=100), nullable=True))
    op.add_column("posts", sa.Column("category", sa.String(length=20), nullable=True))

    # 기존 공개 글은 본문의 첫 100자를 제목으로, 일상 카테고리로 안전하게 이관한다.
    # processing 내부 드래프트는 공개 시점에 새 API 계약으로 값을 받는다.
    op.execute(
        """
        UPDATE posts
           SET title = COALESCE(
                   NULLIF(LEFT(TRIM(REGEXP_REPLACE(content, E'\\s+', ' ', 'g')), 100), ''),
                   '게시물'
               ),
               category = 'daily'
         WHERE status = 'published'
        """
    )
    allowed = ", ".join(f"'{value}'" for value in POST_CATEGORIES)
    op.create_check_constraint(
        "ck_posts_category_value",
        "posts",
        f"category IS NULL OR category IN ({allowed})",
    )
    op.create_check_constraint(
        "ck_posts_published_metadata",
        "posts",
        "status <> 'published' OR (title IS NOT NULL AND BTRIM(title) <> '' AND category IS NOT NULL)",
    )
    op.create_index(
        "ix_posts_feed_category_published",
        "posts",
        ["status", "category", sa.text("published_at DESC"), sa.text("id DESC")],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_posts_feed_category_published", table_name="posts")
    op.drop_constraint("ck_posts_published_metadata", "posts", type_="check")
    op.drop_constraint("ck_posts_category_value", "posts", type_="check")
    op.drop_column("posts", "category")
    op.drop_column("posts", "title")
