from fastapi import APIRouter, Request
from utils import domain_error
import os
import hmac
import hashlib
import httpx

router = APIRouter()

SHOPIFY_API_KEY = os.environ.get("SHOPIFY_API_KEY")
SHOPIFY_SECRET = os.environ.get("SHOPIFY_API_SECRET")


@router.get("/callback")
async def shopify_callback(request:Request):
    params = dict(request.query_params)


    shop = params.get("shop")
    code = params.get("code")
    hmac_recieved = params.get("hmac")
    state = params.get("state")

    if not shop or not code or not hmac_recieved:
        raise domain_error.BadRequest()
    
    sorted_params = sorted(
        (k,v) for k,v in params.items() if k != "hmac"
    )

    message = "&".join(f"{k}={v}" for k,v in sorted_params)

    computed_hmac = hmac.new(
        SHOPIFY_API_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_hmac, hmac_recieved):
        raise domain_error.BadRequest()
    

    token_url = f"https://{shop}/admin/oauth/access_token"

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, json={
            "client_id": SHOPIFY_API_KEY,
            "client_secret": SHOPIFY_SECRET,
            "code": code
        })

    data = resp.json()
    access_token = data.get("access_token")

    if not access_token:
        raise domain_error.BadRequest()
    
    return {"status": "connected", "shop":shop}







