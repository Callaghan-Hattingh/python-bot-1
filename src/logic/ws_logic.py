import json
from datetime import datetime


def trade_sorter(trade):
    trade = json.loads(trade)
    if int(trade.get("data").get("bucketPeriodInSeconds")) == 60:
        assert trade.get("currencyPairSymbol") == trade.get("data").get(
            "currencyPairSymbol"
        )
        print(trade)
        print(trade.get("type"))
        print(trade.get("currencyPairSymbol"))
        print(trade.get("data").get("bucketPeriodInSeconds"))
        print(datetime.utcnow())
        print(trade.get("data").get("startTime"))
        print(trade.get("data").get("open"))
        print(trade.get("data").get("high"))
        print(trade.get("data").get("low"))
        print(trade.get("data").get("close"))
        print(trade.get("data").get("volume"))
        print(trade.get("data").get("quoteVolume"))
