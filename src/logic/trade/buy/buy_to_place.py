# need to place the buy trades on valr and change buy passive to buy active
from src.models.trade import Trade
from src.models.enums import OrderTypes
from src.adapter.utils import commit
from src.core import config
from src.valr.apis import batch_orders


def batch_buy_active_gen(
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
                    "quantity": f'{b.quantity:.8f}',
                    # "quantity": b.quantity,
                    "price": f'{b.price}',
                    "postOnly": str(b.post_only),
                    "timeInForce": b.time_in_force,
                    "customerOrderId": b.customer_order_id
                },
            }
        )
        b.valr_id = "placingTrade"
        commit()
    # print(orders)
    return orders


def buy_to_place(*, trades: list[Trade]) -> None:
    # Step 1 separate trades into batches
    size = config.batch_lot_size
    batches = [trades[x : x + size] for x in range(0, len(trades), size)]
    for batch in batches:

        # Step 2 create batch trade and update db
        batch_order = batch_buy_active_gen(
            batch=batch, order_type=OrderTypes.place_limit
        )
        # Step 3 post batch
        resp = batch_orders(data=batch_order)

        # Step 4 check post and update db
        print(resp)
        # print(batch_order)





