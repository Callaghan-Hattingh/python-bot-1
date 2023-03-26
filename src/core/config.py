import os

from dotenv import load_dotenv

from src.core.setup import get_setup_value

load_dotenv()

# Get from environment
api_secret: str = os.getenv("API_SECRET")
api_key: str = os.getenv("API_KEY")
root_url: str = os.getenv("ROOT_URL")
batch_cancel_type: str = os.getenv("BATCH_CANCEL_TYPE")

# Get from setup
currency_pair: str = str(get_setup_value(value="currency_pair"))
c_id: str = str(get_setup_value(value="customer_id"))
post_only: bool = bool(get_setup_value(value="post_only"))
batch_lot_size: int = int(get_setup_value(value="batch_lot_size"))
max_sell_lots: int = int(get_setup_value(value="max_sell_trades"))
max_buy_lots: int = int(get_setup_value(value="max_buy_trades"))
step: int = int(get_setup_value(value="step"))
tick_size: int = int(get_setup_value(value="tick_size"))
correction_number: int = int(get_setup_value(value="correction_number"))
percentage_gain: float = float(get_setup_value(value="percentage_gain"))
min_base_amount: float = float(get_setup_value(value="min_base_amount"))
min_quote_amount: float = float(get_setup_value(value="min_quote_amount"))
base_decimal_places: int = int(get_setup_value(value="base_decimal_places"))
