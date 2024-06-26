# no api calls required

from src.adapter.trade import create
from src.core import config
from src.models.trade import Side, TimeInForce, Trade, TradeStatus


def minimum_quantity_generation(price: float) -> float:
    # should return float not string string requirement should be on api adapter
    if price * float(config.min_base_amount) > config.min_quote_amount:
        return config.min_base_amount
    else:
        return round(
            (config.min_quote_amount + config.tick_size) / price,
            config.base_decimal_places,
        )


# Step 1 -> Create passive buy orders as needed.
def create_passive_buy_trades(trades_to_create: set[float]) -> None:
    for q in trades_to_create:
        t: Trade = Trade(
            trade_price=q,
            valr_id="newBuyPassive",
            side=Side.buy,
            price=q,
            quantity=minimum_quantity_generation(price=q),
            currency_pair=config.currency_pair,
            post_only=config.post_only,
            customer_order_id=f"{config.c_id}{q}".replace(".", "-"),
            time_in_force=TimeInForce.gtc,
            trade_status=TradeStatus.bpass,
        )
        create(t)
