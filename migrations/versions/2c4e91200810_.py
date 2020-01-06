"""empty message

Revision ID: 2c4e91200810
Revises: 13ec0ac4d518
Create Date: 2020-01-06 15:48:01.464419

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2c4e91200810"
down_revision = "13ec0ac4d518"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=True),
        sa.Column("user_uuid", postgresql.UUID(), nullable=False),
        sa.Column("board_uuid", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["board_uuid"], ["boards.uuid"]),
        sa.ForeignKeyConstraint(["user_uuid"], ["users.uuid"]),
        sa.PrimaryKeyConstraint("id", "uuid"),
        sa.UniqueConstraint(
            "board_uuid", "user_uuid", name="unique_board_owner_permission"
        ),
        sa.UniqueConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("permissions")
    # ### end Alembic commands ###
