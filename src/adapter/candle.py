from sqlalchemy import desc

from src.db.base import session
from src.models.candle import Candle
from sqlalchemy.sql import func


def create(candle: Candle) -> None:
    session.add(candle)
    session.commit()


def read_avg_candle_close(*, period: int) -> float:
    candles = (
        session.query(Candle.candle_close)
        .order_by(desc(Candle.change_time))
        .limit(period)
        .subquery()
    )
    avg_candles = session.query(
        func.avg(candles.c.candle_close).label(f"avg_last_{period}_candles")
    ).one()
    return avg_candles


def read_std_dev_candle_close(*, period: int) -> float:
    candles = (
        session.query(Candle.candle_close)
        .order_by(desc(Candle.change_time))
        .limit(period)
        .subquery()
    )
    std_candles = session.query(
        func.sqrt(
            func.avg(candles.c.candle_close * candles.c.candle_close)
            - func.avg(candles.c.candle_close) * func.avg(candles.c.candle_close)
        ).label(f"std_last_{period}_candles")
    ).one()
    return std_candles
