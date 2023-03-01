from dataclasses import dataclass

from sqlalchemy import Column, Enum, Float, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


@dataclass
class Candle(Base):
    __tablename__ = "Candle"

    id = Column(Integer, primary_key=True, nullable=False)
    change_time = Column(TIMESTAMP(timezone=False), nullable=False)
    trade_type = Column(
        Enum("NEW_TRADE_BUCKET", "NEW_TRADE", names="trade_type"), nullable=False
    )
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    start_time = Column(TIMESTAMP, nullable=False)
    candle_open = Column(Float, nullable=False)
    candle_high = Column(Float, nullable=False)
    candle_low = Column(Float, nullable=False)
    candle_close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    quote_volume = Column(Float, nullable=False)
