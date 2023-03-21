from sqlalchemy import asc
from sqlalchemy.sql.expression import or_

from src.db.base import session
from src.models.trade import Trade, TradeStatus


def read_trades_with_prices(prices: set[float]) -> list[Trade] | None:
    return session.query(Trade).filter(Trade.trade_price.in_(prices)).all()


def read_trades_for_status_lower_than_price(
    price: float, status: str
) -> list[Trade] | None:
    return (
        session.query(Trade)
        .filter(Trade.trade_status == status)
        .filter(Trade.price < price)
        .all()
    )


def read_trades_for_status(*, status: str) -> list[Trade] | None:
    return (
        session.query(Trade)
        .filter(Trade.trade_status == status)
        .order_by(asc(Trade.price))  # noqa
        .all()
    )


def read_x_sell_trades_above_y(
    *, minimum_price: float, amount_of_trades: int
) -> list[Trade] | None:
    return (
        session.query(Trade)
        .filter(Trade.price > minimum_price)
        .filter(
            or_(
                Trade.trade_status == TradeStatus.sact,
                Trade.trade_status == TradeStatus.spass,
            )
        )
        .order_by(asc(Trade.price))
        .limit(amount_of_trades)
    )


def create(trade: Trade) -> None:
    session.add(trade)
    session.commit()
