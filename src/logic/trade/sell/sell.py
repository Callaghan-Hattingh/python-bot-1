# overall management for sell trades section


from src.models.candle import Candle
from .sell_to_complete import sell_to_complete


def sell(*, candle: Candle, open_trades: list[dict]) -> None:
    # Step 1 -> check for completed sells
    sell_to_complete(open_trades=open_trades)

    # Step 2 -> check for sell active
    # Step 3 -> check for unneeded buy active
