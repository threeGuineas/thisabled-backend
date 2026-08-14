"""사용자 알림 그룹 설정 추가.

Revision ID: d3e5f7a9b1c2
Revises: c2d4e6f8a0b1
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "d3e5f7a9b1c2"
down_revision = "c2d4e6f8a0b1"
branch_labels = None
depends_on = None


DEFAULTS = (
    "jsonb_build_object("
    "'friend_activity', true, 'post_activity', true, "
    "'chat_activity', true, 'ai_results', true)"
)


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "notification_settings",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text(DEFAULTS),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "notification_settings")
