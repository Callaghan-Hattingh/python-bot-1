from src.db.base import session
from src.models.candle import Candle


def create(candle: Candle) -> None:
    session.add(candle)
    session.commit()


def hour_avg():
    session.query(Candle).limit(60)
