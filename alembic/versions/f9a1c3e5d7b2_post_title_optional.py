"""공개 게시물 제목을 선택 메타데이터로 정정.

Revision ID: f9a1c3e5d7b2
Revises: b5d7f9a1c3e4
"""

from alembic import op


revision = "f9a1c3e5d7b2"
down_revision = "b5d7f9a1c3e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("ck_posts_published_metadata", "posts", type_="check")
    op.create_check_constraint(
        "ck_posts_published_metadata",
        "posts",
        "status <> 'published' OR category IS NOT NULL",
    )


def downgrade() -> None:
    # 선택 제목이 없는 공개 글도 이전 필수 계약으로 되돌릴 수 있게 먼저 채운다.
    op.execute(
        """
        UPDATE posts
           SET title = COALESCE(
                   NULLIF(LEFT(TRIM(REGEXP_REPLACE(content, E'\\s+', ' ', 'g')), 100), ''),
                   '게시물'
               )
         WHERE status = 'published'
           AND (title IS NULL OR BTRIM(title) = '')
        """
    )
    op.drop_constraint("ck_posts_published_metadata", "posts", type_="check")
    op.create_check_constraint(
        "ck_posts_published_metadata",
        "posts",
        "status <> 'published' OR (title IS NOT NULL AND BTRIM(title) <> '' AND category IS NOT NULL)",
    )
