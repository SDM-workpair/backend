"""add group_id column to notification table

Revision ID: e6bb448bbe23
Revises: a517ce3b246a
Create Date: 2023-05-24 16:30:36.189201

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e6bb448bbe23"
down_revision = "a517ce3b246a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("Notification")
    op.create_table(
        "Notification",
        sa.Column("notification_uuid", sa.UUID(), nullable=False),
        sa.Column("receiver_uuid", sa.UUID(), nullable=False),
        sa.Column("sender_uuid", sa.UUID(), nullable=True),
        sa.Column("send_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("template_uuid", sa.String(), nullable=False),
        sa.Column("f_string", sa.String(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("group_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["receiver_uuid"],
            ["User.user_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_uuid"],
            ["User.user_uuid"],
        ),
        sa.PrimaryKeyConstraint("notification_uuid"),
    )


def downgrade() -> None:
    pass
