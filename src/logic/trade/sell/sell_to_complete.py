# check if currency was sold in last candle check with open orders
from src.adapter.trade import read_trades_for_status
from src.adapter.utils import commit
from src.models.trade import Side, Trade, TradeStatus


def sell_open_trades(*, open_trades) -> list[dict]:
    sell_trades = []
    for trade in open_trades:
        if trade.get("side") == "sell":
            sell_trades.append(trade)
    return sell_trades


def determine_sell_trades_completed(
    *, db_trades: list[Trade], valr_trades: list[dict]
) -> list[Trade]:
    live_trades = set()
    sold = []
    for q in valr_trades:
        # print(q.get("price"))
        live_trades.add(float(q.get("price")))
    for w in db_trades:
        if w.price in live_trades:
            # live_trades.remove(w.price)
            continue
        else:
            sold.append(w)
    return sold


def calculate_buy_quantity(
    *, quantity: float, buy_price: float, sell_price: float
) -> float:
    return round(quantity * (sell_price / buy_price), 8)


def create_buy_passive(*, trade: Trade) -> None:
    trade.valr_id = "newBuy"
    trade.side = Side.buy
    trade.quantity = calculate_buy_quantity(
        quantity=trade.quantity, buy_price=trade.trade_price, sell_price=trade.price
    )
    trade.price = trade.trade_price
    trade.trade_status = TradeStatus.bpass
    commit()


def sell_to_complete(*, open_trades: list[dict]) -> None:
    # Step 1 -> get sell active form db and open buy trades from valr
    sell_valr_trades = sell_open_trades(open_trades=open_trades)
    sell_act_trades = read_trades_for_status(status=TradeStatus.sact)

    # Step 2 -> Compare
    sold = determine_sell_trades_completed(
        db_trades=sell_act_trades, valr_trades=sell_valr_trades
    )
    print(sold)

    # Step 3 -> update db as needed
    for trade in sold:
        create_buy_passive(trade=trade)
