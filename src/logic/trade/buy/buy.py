# overall management for buy trades section
from src.adapter.trade import read_trades_with_prices
from src.core import config
from src.models.candle import Candle
from src.models.trade import Trade, TradeStatus

from ..utils import filter_trades
from .buy_to_cancel import buy_to_cancel
from .buy_to_complete import buy_to_complete
from .buy_to_create import create_passive_buy_trades
from .buy_to_place import buy_to_place


def buy(*, candle: Candle, open_trades: list[dict]) -> None:
    # Step 0 -> check for completed buys first
    buy_to_complete(open_trades=open_trades, candle=candle)
    # Step 1 -> check if any buy lots should be placed
    planned_trades = create_planned_trades(price=candle.candle_close)
    print(planned_trades)
    trades = read_planned_trades_from_db(planned_trades=planned_trades)
    # Step 3 -> place the buy active
    buy_to_place(trades=filter_trades(trades=trades, status=TradeStatus.bpass))
    # Step 4 -> cancel the unwanted buy active
    buy_to_cancel(planned_trades=planned_trades)


# Step 1 -> check if any buy lots should be placed
def create_planned_trades(*, price: float) -> set[float]:
    """
    To create the set of buy trades that should exist.
    :param price: last traded price
    :return: set of buy prices to be placed
    """
    s = set()
    max_s = ((price - config.tick_size) // config.step) * config.step
    # add a grap of one trade range(will add again if needed)
    for _ in range(config.max_buy_lots):
        s.add(max_s - config.step * _)
    return s


# Step 2 -> check if/which trades exist in db & status of trades
def read_planned_trades_from_db(*, planned_trades: set[float]) -> list[Trade]:
    trades = read_trades_with_prices(prices=planned_trades)

    # check which need to be made
    existing_trades = set()
    for q in trades:
        existing_trades.add(q.trade_price)
    trades_to_create = planned_trades.difference(existing_trades)

    # create need passive buys
    if trades_to_create:
        create_passive_buy_trades(trades_to_create)
        trades = read_trades_with_prices(prices=planned_trades)

    return trades
