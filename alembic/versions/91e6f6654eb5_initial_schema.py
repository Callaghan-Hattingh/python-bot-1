"""initial schema

Revision ID: 91e6f6654eb5
Revises: 
Create Date: 2023-03-21 12:23:03.004030

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "91e6f6654eb5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candle",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column(
            "change_time",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("candle_type", sa.VARCHAR(length=16), nullable=False),
        sa.Column("currency_pair", sa.VARCHAR(length=6), nullable=False),
        sa.Column("bucket_period", sa.INTEGER(), nullable=False),
        sa.Column("start_time", sa.DATETIME(), nullable=False),
        sa.Column("candle_open", sa.FLOAT(), nullable=False),
        sa.Column("candle_high", sa.FLOAT(), nullable=False),
        sa.Column("candle_low", sa.FLOAT(), nullable=False),
        sa.Column("candle_close", sa.FLOAT(), nullable=False),
        sa.Column("volume", sa.FLOAT(), nullable=False),
        sa.Column("quote_volume", sa.FLOAT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "trade",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("trade_price", sa.FLOAT(), nullable=False),
        sa.Column(
            "change_time",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("valr_id", sa.VARCHAR(length=36), nullable=False),
        sa.Column("side", sa.VARCHAR(length=4), nullable=False),
        sa.Column("price", sa.FLOAT(), nullable=False),
        sa.Column("quantity", sa.FLOAT(), nullable=False),
        sa.Column("currency_pair", sa.VARCHAR(length=6), nullable=False),
        sa.Column("post_only", sa.BOOLEAN(), nullable=False),
        sa.Column("customer_order_id", sa.VARCHAR(length=50), nullable=False),
        sa.Column("time_in_force", sa.VARCHAR(length=3), nullable=False),
        sa.Column("trade_status", sa.VARCHAR(length=12), nullable=False),
        sa.Column("amount_of_trades", sa.INTEGER(), nullable=False),
        sa.Column("batchId", sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_trade_trade_price", "trade", ["trade_price"], unique=False)
    pass


def downgrade() -> None:
    op.drop_index("ix_trade_trade_price", table_name="trade")
    op.drop_table("trade")
    op.drop_table("candle")
    pass
