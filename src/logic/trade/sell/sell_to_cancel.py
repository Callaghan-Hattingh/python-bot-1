# cancel all the buy actives below the planned minimum
# keep ten lowest sell amounts
from src.adapter.trade import read_trades_for_status
from src.adapter.utils import commit
from src.core import config
from src.models.enums import OrderTypes
from src.models.trade import Trade, TradeStatus
from src.valr.apis import batch_orders


def batch_sell_passive_gen(
    *, batch: list[Trade], order_type: str
) -> list[dict[str, str | dict]]:
    orders = []
    for b in batch:
        orders.append(
            {
                "type": order_type,
                "data": {
                    "orderId": b.valr_id,
                    "pair": b.currency_pair,
                },
            }
        )
    return orders


def sell_to_cancel() -> None:
    # Step 1 -> get sell active trades
    sell_act_trades = read_trades_for_status(status=TradeStatus.sact)
    to_delete = []

    # Step 2 -> determine which trades need to be deleted
    for num, trade in enumerate(sell_act_trades):
        if num > 3 + config.max_buy_lots:
            to_delete.append(trade)

    # Step 3 -> delete the unneeded trades
    size = config.batch_lot_size
    batches = [to_delete[x : x + size] for x in range(0, len(to_delete), size)]
    for batch in batches:
        batch_delete = batch_sell_passive_gen(
            batch=batch, order_type=OrderTypes.cancel_order
        )
        resp = batch_orders(data=batch_delete)
        print(resp)
        for q, w in zip(resp["outcomes"], batch):
            if q.get("accepted"):
                w.valr_id = "tradeSellDeleted"
                w.trade_status = TradeStatus.spass
                w.batchId = resp.get("batchId")
                commit()
