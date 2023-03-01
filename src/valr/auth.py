import os
import hashlib
import hmac
from dotenv import load_dotenv

load_dotenv()


def sign_request(
    timestamp: int,
    verb: str,
    path: str,
    *,
    api_key_secret: str = os.getenv("API_SECRET"),
    body: str = "",
) -> str:
    """Signs the request payload using the api key secret
    api - the api key secret
    t - the unix t of this request e.g. int(time.time()*1000)
    v - Http v - GET, POST, PUT or DELETE
    p - p excluding host name, e.g. '/v1/withdraw
    body - http request body as a string, optional
    """
    payload = "{}{}{}{}".format(timestamp, verb.upper(), path, body)
    print(f"'{payload}'")
    message = bytearray(payload, "utf-8")
    print(message)
    print(api_key_secret)
    signature = hmac.new(
        bytearray(api_key_secret, "utf-8"), message, digestmod=hashlib.sha512
    ).hexdigest()
    print(signature)
    # print(signature.digest())
    return signature


def get_headers(timestamp: int, signature: str) -> dict:
    header = {
        "X-VALR-API-KEY": os.getenv("API_KEY"),
        "X-VALR-SIGNATURE": f"{signature}",
        "X-VALR-TIMESTAMP": f"{timestamp}",
        "Content-Type": "application/json",
    }
    return header
