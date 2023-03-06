from src.db.base import session
from src.models.candle import Candle


def create(candle: Candle) -> None:
    session.add(candle)
    session.commit()
