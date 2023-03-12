import json
from src.models.candle import Candle
from src.adapter.candle import create
from src.core import config
from src.logic.trade.utils import open_trades_for_currency_pair

from dateutil import parser

from .trade.buy.buy import buy


def candle_hander(candle):
    candle = json.loads(candle)
    if int(candle.get("data").get("bucketPeriodInSeconds")) == 60:
        assert candle.get("currencyPairSymbol") == candle.get("data").get(
            "currencyPairSymbol"
        )
        c: Candle = Candle(
            candle_type=candle.get("type"),
            currency_pair=candle.get("currencyPairSymbol"),
            bucket_period=int(candle.get("data").get("bucketPeriodInSeconds")),
            start_time=parser.parse(candle.get("data").get("startTime")),
            candle_open=float(candle.get("data").get("open"))
            - config.correction_number,
            candle_high=float(candle.get("data").get("high"))
            - config.correction_number,
            candle_low=float(candle.get("data").get("low")) - config.correction_number,
            candle_close=float(candle.get("data").get("close"))
            - config.correction_number,
            volume=float(candle.get("data").get("volume")),
            quote_volume=float(candle.get("data").get("quoteVolume")),
        )
        create(c)
        candle_controller(c)


def candle_controller(candle: Candle) -> None:
    print(candle.start_time, " ", candle.candle_close)
    open_trades = open_trades_for_currency_pair()
    buy(candle=candle, open_trades=open_trades)
