"""add value column

Revision ID: f3c5d5d9616e
Revises: abf4ef960a62
Create Date: 2023-03-21 16:03:56.789853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3c5d5d9616e"
down_revision = "abf4ef960a62"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "trade",
        sa.Column(
            "value",
            sa.Float(),
            sa.Computed(
                "price * quantity",
            ),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("trade", "value")
