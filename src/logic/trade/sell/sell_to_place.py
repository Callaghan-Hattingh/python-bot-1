# need to place the sell trades on valr and change sell passive to sell active
from datetime import datetime

from src.adapter.utils import commit
from src.core import config
from src.models.enums import OrderTypes
from src.models.trade import Trade, TradeStatus
from src.valr.apis import batch_orders


def batch_sell_active_gen(
    *, batch: list[Trade], order_type: str
) -> list[dict[str, str | dict]]:
    orders = []
    for b in batch:
        orders.append(
            {
                "type": order_type,
                "data": {
                    "pair": b.currency_pair,
                    "side": b.side,
                    "quantity": f"{b.quantity:.8f}",
                    "price": f"{b.price}",
                    "postOnly": str(b.post_only),
                    "timeInForce": b.time_in_force,
                    "customerOrderId": b.customer_order_id,
                },
            }
        )
        b.valr_id = "placingSellTrade"
        commit()
    return orders


def sell_to_place(*, trades: list[Trade]) -> None:
    # Step 1 separate trades into batches
    size = config.batch_lot_size
    batches = [trades[x : x + size] for x in range(0, len(trades), size)]
    for batch in batches:
        # Step 2 create batch trade and update db
        batch_order = batch_sell_active_gen(
            batch=batch, order_type=OrderTypes.place_limit
        )

        # Step 3 post batch
        resp = batch_orders(data=batch_order)

        # Step 4 check post and update db
        print(resp)
        for q, w in zip(resp["outcomes"], batch):
            if q.get("accepted"):
                w.valr_id = q.get("orderId")
                w.trade_status = TradeStatus.sact
                w.batchId = resp.get("batchId")
                w.change_time = datetime.utcnow()
                commit()
            else:
                print(f"fail sell act: {w.customer_order_id}")
