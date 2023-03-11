from dataclasses import dataclass


@dataclass
class OrderTypes:
    place_limit = "PLACE_LIMIT"
    place_market = "PLACE_MARKET"
    place_stop_limit = "PLACE_STOP_LIMIT"
    cancel_order = "CANCEL_ORDER"
