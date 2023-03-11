# overall management for buy trades section
from src.adapter.trade import read_trades_with_prices
from src.core import config
from src.models.candle import Candle
from src.models.trade import Trade, TradeStatus
from .buy_to_create import create_passive_buy_trades
from .buy_to_place import buy_to_place


# Step 1 -> check if any buy lots should be placed


def buy(*, candle: Candle) -> None:
    planned_trades = create_planned_trades(price=candle.candle_close)
    print(planned_trades)
    trades = read_planned_trades_from_db(planned_trades=planned_trades)
    buy_to_place(trades=filter_trades(trades=trades, status=TradeStatus.bpass))


# Step 1 -> check if any buy lots should be placed
def create_planned_trades(*, price: float) -> set[float]:
    """
    To create the set of buy trades that should exist.
    :param price: last traded price
    :return: set of buy prices to be placed
    """
    s = set()
    max_s = ((price - 1) // config.step) * config.step
    for _ in range(0, config.max_buy_lots):
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


def filter_trades(*, trades: list[Trade], status: str) -> list[Trade]:
    filtered = []
    for q in trades:
        if q.trade_status == status:
            filtered.append(q)
    return filtered


# Step 3 -> place the buy active


# # Step 3 -> sort trades to check which buys need to be placed, cancelled and sells to make
# def sort_trades_into_required_sections(*, trades: list[Trade]) -> dict[list[Trade]] | None:
#     # Step I -> sort based on trade_status
#     sort = {
#         TradeStatus.bpass: [],
#         TradeStatus.bact: [],
#         TradeStatus.spass: []
#     }
#     for q in trades:
#         if q.trade_status == TradeStatus.bpass:
#             sort[TradeStatus.bpass].append(q)
#         elif q.trade_status == TradeStatus.bact:
#             sort[TradeStatus.bact].append(q)
#         else:
#             continue
#     print(sort)
