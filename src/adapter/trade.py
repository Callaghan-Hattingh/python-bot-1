from src.db.base import session
from src.models.trade import Trade


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


def read_trades_for_status(status: str) -> list[Trade] | None:
    return session.query(Trade).filter(Trade.trade_status == status).all()


def create(trade: Trade) -> None:
    session.add(trade)
    session.commit()
