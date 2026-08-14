"""대칭 친구 요청의 동시 pending 중복 방지.

Revision ID: e4f6a8c0d2e3
Revises: d3e5f7a9b1c2
"""

from alembic import op
import sqlalchemy as sa


revision = "e4f6a8c0d2e3"
down_revision = "d3e5f7a9b1c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 과거 경쟁 요청이 있다면 가장 오래된 pending 한 건만 유지한다.
    op.execute(
        """
        DELETE FROM friend_requests newer
        USING friend_requests older
        WHERE newer.status = 'pending'
          AND older.status = 'pending'
          AND LEAST(newer.sender_id, newer.receiver_id)
              = LEAST(older.sender_id, older.receiver_id)
          AND GREATEST(newer.sender_id, newer.receiver_id)
              = GREATEST(older.sender_id, older.receiver_id)
          AND (newer.created_at, newer.id) > (older.created_at, older.id)
        """
    )
    op.create_index(
        "uq_friend_requests_pending_pair",
        "friend_requests",
        [
            sa.text("LEAST(sender_id, receiver_id)"),
            sa.text("GREATEST(sender_id, receiver_id)"),
        ],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )


def downgrade() -> None:
    op.drop_index("uq_friend_requests_pending_pair", table_name="friend_requests")
