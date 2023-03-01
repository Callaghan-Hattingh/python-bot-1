from src.db.base import session
from src.models import Candle


def create(candle: Candle) -> None:
    session.add(candle)
    session.commit()
