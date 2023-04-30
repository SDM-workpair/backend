"""update schema of notification related tables

Revision ID: e93d0123c41f
Revises: 3e4e9958b6c2
Create Date: 2023-04-30 13:21:36.727755

"""
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e93d0123c41f'
down_revision = '3e4e9958b6c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "NotificationTemplate",
        sa.Column("template_uuid", sa.UUID(), nullable=False),
        sa.Column("template_id", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("template_uuid"),
        sa.UniqueConstraint("template_id"),
    )
    op.create_table(
        "Notification",
        sa.Column("notification_uuid", sa.UUID(), nullable=False),
        sa.Column("receiver_uuid", sa.UUID(), nullable=False),
        sa.Column("sender_uuid", sa.UUID(), nullable=True),
        sa.Column("send_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("template_uuid", sa.String(), nullable=False),
        sa.Column("f_string", sa.String(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False),
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
