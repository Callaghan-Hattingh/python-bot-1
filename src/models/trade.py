from dataclasses import dataclass

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    String,
    text,
    Computed,
)
from sqlalchemy.ext.hybrid import hybrid_property

from src.db.base import Base


@dataclass
class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, nullable=False)
    trade_price = Column(Float, nullable=False, index=True, unique=True)
    change_time = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    valr_id = Column(String(36), nullable=False)  # UUID
    side = Column(Enum("BUY", "SELL", names="side"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    post_only = Column(Boolean, nullable=False)
    customer_order_id = Column(String(50), nullable=False)
    time_in_force = Column(
        Enum("GTC", "FOK", "IOC", names="time_in_force"), nullable=False
    )
    trade_status = Column(
        Enum(
            "buy_passive",
            "buy_active",
            "sell_active",
            "sell_passive",
            names="lot_status",
        ),
        nullable=False,
    )
    amount_of_trades = Column(Integer, nullable=False, default=0)
    batchId = Column(Integer, nullable=False, default=-1)
    value = Column(Float, Computed(price * quantity))  # noqa


@dataclass
class Side:
    buy = "BUY"
    sell = "SELL"


@dataclass
class CurrencyPair:
    btc = "BTCZAR"
    eth = "ETHZAR"
    xrp = "XRPZAR"


@dataclass
class TimeInForce:
    gtc = "GTC"
    fok = "FOK"
    ioc = "IOC"


@dataclass
class TradeStatus:
    bpass = "buy_passive"
    bact = "buy_active"
    spass = "sell_passive"
    sact = "sell_active"
