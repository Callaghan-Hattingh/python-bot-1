from dataclasses import dataclass

from sqlalchemy import Column, Enum, Float, Integer, DateTime, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


@dataclass
class Candle(Base):
    __tablename__ = "Candle"

    id = Column(Integer, primary_key=True, nullable=False)
    change_time = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    candle_type = Column(Enum("NEW_TRADE_BUCKET", names="candle_type"), nullable=False)
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    bucket_period = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    candle_open = Column(Float, nullable=False)
    candle_high = Column(Float, nullable=False)
    candle_low = Column(Float, nullable=False)
    candle_close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    quote_volume = Column(Float, nullable=False)
