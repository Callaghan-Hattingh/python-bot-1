import datetime

from src.db.base import create_tables
from src.valr.wsocket import ws_new_trade_bucket


def bot():
    while True:
        now = datetime.datetime.utcnow()
        if now.second == 30:
            ws_new_trade_bucket()


def controller() -> None:
    create_tables()
    bot()
