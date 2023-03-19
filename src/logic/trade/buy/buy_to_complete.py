# check if currency was bought in last candle check with open orders
import math
from datetime import datetime

from src.adapter.trade import read_trades_for_status
from src.adapter.utils import commit
from src.models.candle import Candle
from src.models.trade import Side, Trade, TradeStatus


def buy_open_trades(*, open_trades) -> list[dict]:
    buy_trades = []
    for trade in open_trades:
        if trade.get("side") == "buy":
            buy_trades.append(trade)
    return buy_trades


def determine_buy_trades_completed(
    *, db_trades: list[Trade], valr_trades: list[dict]
) -> list[Trade]:
    live_trades = set()
    bought = []
    for q in valr_trades:
        live_trades.add(float(q.get("price")))
    for w in db_trades:
        if w.price in live_trades:
            # live_trades.remove(w.price)
            continue
        else:
            bought.append(w)
    return bought


def calculate_sell_price(*, price: float, last_traded_at: float) -> float:
    amount = float(math.ceil(price * 1.01))
    if last_traded_at > amount:
        amount = float(math.ceil(last_traded_at * 1.001))
    if amount % 2 == 0:
        return amount + 1
    return amount


def create_sell_passive(*, trade: Trade, close: float) -> None:
    trade.valr_id = "newSell"
    trade.side = Side.sell
    trade.price = calculate_sell_price(price=trade.trade_price, last_traded_at=close)
    trade.trade_status = TradeStatus.spass
    trade.change_time = datetime.utcnow()
    commit()


def buy_to_complete(*, open_trades: list[dict], candle: Candle) -> None:
    # Step 1 -> get buy active form db and open buy trades from valr
    buy_valr_trades = buy_open_trades(open_trades=open_trades)
    buy_act_trades = read_trades_for_status(status=TradeStatus.bact)

    # Step 2 -> Compare
    bought = determine_buy_trades_completed(
        db_trades=buy_act_trades, valr_trades=buy_valr_trades
    )
    print(bought)

    # Step 3 -> update db as needed
    for trade in bought:
        create_sell_passive(trade=trade, close=candle.candle_close)
