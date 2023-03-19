# cancel all the buy actives below the planned minimum
from datetime import datetime

from src.adapter.trade import read_trades_for_status_lower_than_price
from src.adapter.utils import commit
from src.core import config
from src.models.enums import OrderTypes
from src.models.trade import Trade, TradeStatus
from src.valr.apis import batch_orders


def batch_buy_passive_gen(
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


def buy_to_cancel(*, planned_trades: set[float]) -> None:
    # Step 1 -> get minimum amount and query db
    minimum = min(planned_trades)
    to_delete = read_trades_for_status_lower_than_price(
        price=minimum, status=TradeStatus.bact
    )

    # Step 2 -> del valr orders as needed and update status
    size = config.batch_lot_size
    batches = [to_delete[x : x + size] for x in range(0, len(to_delete), size)]
    for batch in batches:
        batch_delete = batch_buy_passive_gen(
            batch=batch, order_type=OrderTypes.cancel_order
        )
        resp = batch_orders(data=batch_delete)
        print(resp)
        for q, w in zip(resp["outcomes"], batch):
            if q.get("accepted"):
                w.valr_id = "tradeBuyDeleted"
                w.trade_status = TradeStatus.bpass
                w.batchId = resp.get("batchId")
                w.change_time = datetime.utcnow()
                commit()
