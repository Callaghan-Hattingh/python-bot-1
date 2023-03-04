import requests
import time
from src.valr.auth import sign_request, get_headers
import os
import json


class VALRapiError(Exception):
    pass


def get_all_open_orders():
    timestamp = int(time.time() * 1000)
    verb = "GET"
    path = "/v1/orders/open"

    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = {}
    headers = get_headers(timestamp, sign_request(timestamp, verb, path))

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def post_limit_order(
    side: str,
    amount: float,
    price: int,
    customer_id: str = None,
    *,
    pair: str = "BTCZAR",
    post_type: bool = True,
):
    timestamp = int(time.time() * 1000)
    verb = "POST"
    path = "/v1/orders/limit"

    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = json.dumps(
        {
            "side": side,
            "quantity": amount,
            "price": price,
            "pair": pair,
            "postOnly": post_type,
            "customerOrderId": customer_id,
        }
    )
    signature = sign_request(timestamp, verb, path, body=payload)
    headers = get_headers(timestamp, signature)

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def del_order(*, pair: str = "BTCZAR", customer_id: str = None, order_id: str = None):
    timestamp = int(time.time() * 1000)
    verb = "DELETE"
    path = "/v1/orders/order"

    url = f"{os.getenv('ROOT_URL')}{path}"

    if customer_id is not None:
        payload = json.dumps({"customerOrderId": customer_id, "pair": pair})
    elif order_id is not None:
        payload = json.dumps({"orderId": order_id, "pair": pair})
    else:
        raise ValueError("Must provide either customer_id or order_id")

    headers = get_headers(timestamp, sign_request(timestamp, verb, path, body=payload))
    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def get_trade_hist(*, pair: str = "BTCZAR", skip: int = 0, limit: int = 1):
    timestamp = int(time.time() * 1000)
    verb = "GET"
    path = f"/v1/marketdata/{pair}/tradehistory?skip={skip}&limit={limit}"

    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = {}
    headers = get_headers(timestamp, sign_request(timestamp, verb, path))

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def get_order_status(
    *, pair: str = "BTCZAR", customer_id: str = None, order_id: str = None
):
    # call only directly after placing order
    if customer_id is not None:
        path = f"/v1/orders/{pair}/customerorderid/{customer_id}"
    elif order_id is not None:
        path = f"/v1/orders/{pair}/orderid/{order_id}"
    else:
        raise ValueError("Must provide either customer_id or order_id")
    timestamp = int(time.time() * 1000)
    verb = "GET"
    signature = sign_request(timestamp, verb, path)
    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = {}
    headers = get_headers(timestamp, signature)

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def get_order_history_summary(*, customer_id: str = None, order_id: str = None):
    # get the order history summary of the last successfully placed order
    if customer_id is not None:
        path = f"/v1/orders/history/summary/customerorderid/{customer_id}"
    elif order_id is not None:
        path = f"/v1/orders/history/summary/orderid/{order_id}"
    else:
        raise ValueError("Must provide either customer_id or order_id")
    timestamp = int(time.time() * 1000)
    verb = "GET"
    signature = sign_request(timestamp, verb, path)
    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = {}
    headers = get_headers(timestamp, signature)

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())


def get_order_history_detail(*, customer_id: str = None, order_id: str = None):
    # get the order history detail of the last successfully placed order
    if customer_id is not None:
        path = f"/v1/orders/history/detail/customerorderid/{customer_id}"
    elif order_id is not None:
        path = f"/v1/orders/history/detail/orderid/{order_id}"
    else:
        raise ValueError("Must provide either customer_id or order_id")
    timestamp = int(time.time() * 1000)
    verb = "GET"
    signature = sign_request(timestamp, verb, path)
    url = f"{os.getenv('ROOT_URL')}{path}"
    payload = {}
    headers = get_headers(timestamp, signature)

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        raise VALRapiError(response.json())
