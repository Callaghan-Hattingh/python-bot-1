from src.core.config import currency_pair

# not used
AGGREGATED_ORDERBOOK_UPDATE = {
    "type": "SUBSCRIBE",
    "subscriptions": [
        {
            "event": "AGGREGATED_ORDERBOOK_UPDATE",
            "pairs": ["BTCZAR", "ETHZAR", "XRPZAR"],
        }
    ],
}
# When subscribed to this event for a given currency pair,
# the client receives the top 20 bids and asks from the order book for that
# currency pair.

MARKET_SUMMARY_UPDATE = {
    "type": "SUBSCRIBE",
    "subscriptions": [{"event": "MARKET_SUMMARY_UPDATE", "pairs": [f"{currency_pair}"]}],
}
# When subscribed to this event for a given currency pair,
# the client receives a candle feed with the latest market summary for that
# currency pair.

NEW_TRADE_BUCKET = {
    "type": "SUBSCRIBE",
    "subscriptions": [{"event": "NEW_TRADE_BUCKET", "pairs": [f"{currency_pair}"]}],
}
# When subscribed to this event for a given currency pair,
# the client receives the Open, High, Low, Close data valid for the last 60 seconds.

NEW_TRADE = {
    "type": "SUBSCRIBE",
    "subscriptions": [{"event": "NEW_TRADE", "pairs": [f"{currency_pair}"]}],
}
# When subscribed to this event for a given currency pair,
# the client receives candle feeds with the latest trades that are executed for that
# currency pair.

PING = {"type": "PING"}
