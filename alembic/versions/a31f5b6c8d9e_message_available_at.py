"""message availability timestamp"""

from alembic import op
import sqlalchemy as sa

revision = "a31f5b6c8d9e"
down_revision = "f7b9114a3c2e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("chat_messages", sa.Column("available_at", sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE chat_messages SET available_at = created_at WHERE safety_status != 'pending'")
    op.alter_column("chat_read_states", "last_read_at", new_column_name="last_read_available_at")


def downgrade() -> None:
    op.alter_column("chat_read_states", "last_read_available_at", new_column_name="last_read_at")
    op.drop_column("chat_messages", "available_at")
