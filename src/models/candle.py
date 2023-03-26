from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Enum, Float, Integer, text
from sqlalchemy.ext.hybrid import hybrid_property

from src.db.base import Base


@dataclass
class Candle(Base):
    __tablename__ = "candle"

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

    @hybrid_property
    def avg(self, period: int) -> float:
        from src.adapter.candle import read_avg_candle_close

        return read_avg_candle_close(period=period)

    @hybrid_property
    def std_dev(self, period: int) -> float:
        from src.adapter.candle import read_std_dev_candle_close

        return read_std_dev_candle_close(period=period)
