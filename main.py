from src.db.base import create_tables
from src.valr.wsocket import ws_new_trade_bucket

if __name__ == "__main__":
    create_tables()
    ws_new_trade_bucket()
