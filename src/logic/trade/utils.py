from src.core import config
from src.models.trade import Trade
from src.valr.apis import get_all_open_orders


def open_trades_for_currency_pair(*, pair: str = config.currency_pair) -> list[dict]:
    oo = get_all_open_orders()
    foo = []
    for i in oo:
        if i["currencyPair"] == pair:
            foo.append(i)
    return foo


def filter_trades(*, trades: list[Trade], status: str) -> list[Trade]:
    filtered = []
    for q in trades:
        if q.trade_status == status:
            filtered.append(q)
    return filtered
