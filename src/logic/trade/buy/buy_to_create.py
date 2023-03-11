# no api calls required

from src.models.trade import Trade
from src.core import config


# Step 1 -> Create passive buy orders as needed.
def create_passive_buy_trades(trades_to_create: set[float]) -> list[Trade]:
    for q in trades_to_create:
        pass
        # t:Trade = Trade(
        #     trade_price=q,
        #     valr_id="newBuyPassive",
        #     side="BUY",
        #     price=q,
        #     quantity=config.quantity,
        #     currency_pair=config.currency_pair,
        #     post_only=config.post_only,
        #     customer_order_id=f'{config.c_id}{q}'
        #     time_in_force=
        # )

    pass


