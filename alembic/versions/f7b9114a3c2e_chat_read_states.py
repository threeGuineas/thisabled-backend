"""chat read states

Revision ID: f7b9114a3c2e
Revises: 84e58e0eefae
Create Date: 2026-07-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f7b9114a3c2e"
down_revision: Union[str, None] = "84e58e0eefae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_read_states",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("room_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("last_read_message_id", sa.Uuid(), nullable=True),
        sa.Column("last_read_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["room_id"], ["chat_rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "user_id"),
    )
    op.create_index(
        "ix_chat_read_states_user_room",
        "chat_read_states",
        ["user_id", "room_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_chat_read_states_user_room", table_name="chat_read_states")
    op.drop_table("chat_read_states")
