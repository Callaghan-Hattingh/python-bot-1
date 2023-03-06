import json
from src.models.candle import Candle
from src.adapter.candle import create

from dateutil import parser


def candle_hander(candle):
    candle = json.loads(candle)
    if int(candle.get("data").get("bucketPeriodInSeconds")) == 60:
        assert candle.get("currencyPairSymbol") == candle.get("data").get(
            "currencyPairSymbol"
        )
        c: Candle = Candle(
            candle_type=candle.get("type"),
            currency_pair=candle.get("currencyPairSymbol"),
            bucket_period=candle.get("data").get("bucketPeriodInSeconds"),
            start_time=parser.parse(candle.get("data").get("startTime")),
            candle_open=candle.get("data").get("open"),
            candle_high=candle.get("data").get("high"),
            candle_low=candle.get("data").get("low"),
            candle_close=candle.get("data").get("close"),
            volume=candle.get("data").get("volume"),
            quote_volume=candle.get("data").get("quoteVolume"),
        )
        print(c.candle_open)
        create(c)
