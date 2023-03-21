"""tidy db

Revision ID: abf4ef960a62
Revises: 91e6f6654eb5
Create Date: 2023-03-21 15:54:05.873284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abf4ef960a62'
down_revision = '91e6f6654eb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('ix_trade_trade_price', table_name='trade')
    op.create_index(op.f('ix_trade_trade_price'), 'trade', ['trade_price'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_trade_trade_price'), table_name='trade')
    op.create_index('ix_trade_trade_price', 'trade', ['trade_price'], unique=False)
