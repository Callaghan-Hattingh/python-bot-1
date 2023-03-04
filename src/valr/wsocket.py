import json

import websocket
from time import time
from src.valr.subscriptions import NEW_TRADE_BUCKET
from src.valr.auth import sign_request, get_headers
from src.logic.ws_logic import candle_hander


def on_message(ws, message):
    candle_hander(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("Connection closed")


def on_open(ws):
    return ws.send(json.dumps(NEW_TRADE_BUCKET))


def ws_new_trade_bucket():
    timestamp = int(time() * 1000)
    verb = "GET"
    path = "/ws/trade"

    url = f"wss://api.valr.com{path}"
    headers = get_headers(timestamp, sign_request(timestamp, verb, path))

    wsapp = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    wsapp.run_forever(ping_interval=20)


if __name__ == "__main__":
    ws_new_trade_bucket()
