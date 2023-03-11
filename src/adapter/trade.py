from src.db.base import session
from src.models.trade import Trade


def read_trades_with_prices(prices: set[float]) -> list[Trade] | None:
    return session.query(Trade).filter(Trade.trade_price.in_(prices)).all()


def create(trade: Trade) -> None:
    session.add(trade)
    session.commit()
