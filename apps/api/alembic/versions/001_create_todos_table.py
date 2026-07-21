"""create todos table

Revision ID: 001_create_todos
Revises:
Create Date: 2026-07-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_create_todos"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todos_latitude", "todos", ["latitude"], unique=False)
    op.create_index("ix_todos_longitude", "todos", ["longitude"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_todos_longitude", table_name="todos")
    op.drop_index("ix_todos_latitude", table_name="todos")
    op.drop_table("todos")
