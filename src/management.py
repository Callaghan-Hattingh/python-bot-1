from src.valr.wsocket import ws_new_trade_bucket
import datetime


def bot():
    while True:
        now = datetime.datetime.utcnow()
        if now.second == 30:
            ws_new_trade_bucket()
