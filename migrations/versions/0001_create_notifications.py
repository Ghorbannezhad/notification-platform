"""create notifications table

Revision ID: 0001_create_notifications
Revises:
Create Date: 2026-07-07 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_create_notifications"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NOTIFICATION_STATUS_VALUES = ("PENDING", "PROCESSING", "SENT", "FAILED")

notification_status = postgresql.ENUM(
    *NOTIFICATION_STATUS_VALUES,
    name="notification_status",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("notification"):
        return

    bind.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_type WHERE typname = 'notification_status'
                ) THEN
                    CREATE TYPE notification_status AS ENUM (
                        'PENDING',
                        'PROCESSING',
                        'SENT',
                        'FAILED'
                    );
                END IF;
            END
            $$;
            """
        )
    )

    op.create_table(
        "notification",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("status", notification_status, nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_notification_user_id"),
        "notification",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("notification"):
        op.drop_index(op.f("ix_notification_user_id"), table_name="notification")
        op.drop_table("notification")

    bind.execute(sa.text("DROP TYPE IF EXISTS notification_status"))
