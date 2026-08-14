"""자막 생성 실패 코드 저장.

Revision ID: b5d7f9a1c3e4
Revises: e4f6a8c0d2e3
"""

from alembic import op
import sqlalchemy as sa


revision = "b5d7f9a1c3e4"
down_revision = "e4f6a8c0d2e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "post_media",
        sa.Column("caption_failure_code", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "chat_messages",
        sa.Column("caption_failure_code", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("chat_messages", "caption_failure_code")
    op.drop_column("post_media", "caption_failure_code")
