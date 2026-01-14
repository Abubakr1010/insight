import os
import hmac
import hashlib
import base64

SECRET = os.environ.get("ACCESS_SECRET")

def generate_state(user_id: int, shop:str): 

    payload = f"{user_id}:{shop}"

    signature = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).digest()

    state = base64.urlsafe_b64encode(
        payload.encode() + b"." + signature
    ).decode()

    return state


