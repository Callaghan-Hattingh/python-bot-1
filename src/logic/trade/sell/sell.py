# overall management for sell trades section

from src.adapter.trade import read_x_sell_trades_above_y
from src.core import config
from src.logic.trade.utils import filter_trades
from src.models.candle import Candle
from src.models.trade import TradeStatus

from .sell_to_cancel import sell_to_cancel
from .sell_to_complete import sell_to_complete
from .sell_to_place import sell_to_place


def sell(*, candle: Candle, open_trades: list[dict]) -> None:
    # Step 1 -> check for completed sells
    sell_to_complete(open_trades=open_trades)

    planned_trades = read_x_sell_trades_above_y(
        minimum_price=candle.candle_close, amount_of_trades=config.max_sell_lots
    )
    # Step 2 -> check for sell active
    sell_to_place(trades=filter_trades(trades=planned_trades, status=TradeStatus.spass))

    # Step 3 -> check for unneeded buy active
    sell_to_cancel()
