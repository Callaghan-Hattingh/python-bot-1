# Create a basic trading config per currency
import argparse

info = {
    "valr": {
        "pairs": {
            # "btczar": {
            #     "currency_pair": "BTCZAR",
            #     "customer_id": "",
            #     "post_only": True,
            #     "batch_lot_size": 20,
            #     "max_sell_trades": 50,
            #     "max_buy_trades": 50,
            #     "step": 200,
            #     "tick_size": 1,
            #     "correction_number": 0,
            #     "percentage_gain": 0.01,
            #     "min_base_amount": 0.000_01,
            #     "min_quote_amount": 10,
            #     "base_decimal_places": 8,
            # },
            "ethwzar": {
                "currency_pair": "ETHWZAR",
                "customer_id": "PYTHON-BOT1PROD-V1-3",
                "post_only": True,
                "batch_lot_size": 20,
                "max_sell_trades": 10,
                "max_buy_trades": 10,
                "step": 2,
                "tick_size": 1,
                "correction_number": 0,
                "percentage_gain": 0.05,
                "min_base_amount": 0.01,
                "min_quote_amount": 10,
                "base_decimal_places": 4,
            },
            "xrpzar": {
                "currency_pair": "XRPZAR",
                "customer_id": "PYTHON-BOT1PROD-V1-3",
                "post_only": True,
                "batch_lot_size": 20,
                "max_sell_trades": 10,
                "max_buy_trades": 10,
                "step": 1,
                "tick_size": 0.01,
                "correction_number": 0,
                "percentage_gain": 0.05,
                "min_base_amount": 3,
                "min_quote_amount": 10,
                "base_decimal_places": 4,
            },
        }
    }
}


def validate_pair(*, pair: str) -> None:
    if PAIR is None:
        print("Error pair cant be None")
        exit(code=-1)
    result = info["valr"]["pairs"].get(pair.lower())
    if not result:
        print("Error pair is invade, please correct")
        exit(code=-1)


parser = argparse.ArgumentParser()
parser.add_argument("--pair", help="Select trading currency", default=None)
args = parser.parse_args()

PAIR = args.pair
validate_pair(pair=PAIR)


def get_setup_value(pair: str = PAIR, *, value: str):
    try:
        return info["valr"]["pairs"].get(pair.lower()).get(value.lower())
    except AttributeError:
        print("pair or value key error")
