import os
from fastapi import APIRouter, Body, Depends
from utils.shopify_state import generate_state
from fastapi.security import OAuth2PasswordBearer
from utils.user import get_current_user


router = APIRouter(tags=["shopify"])


SHOPIFY_API_KEY = os.environ.get("SHOPIFY_API_KEY")
SHOPIFY_SCOPES = os.environ.get("SHOPIFY_SCOPE")
SHOPIFY_SECRET = os.environ.get("SHOPIFY_API_SECRET")
SHOPIFY_REDIRECT_URI = os.environ.get("SHOPIFY_REDIRECT_URI")



@router.post("/connect")
async def connect_shopify(
    shop: str = Body(embed=True),
    user = Depends(get_current_user)
):
    
    state = generate_state(
        user_id = user["id"],
        shop = shop
    )

    oauth_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={SHOPIFY_API_KEY}"
        f"&scope={SHOPIFY_SCOPES}"
        f"&redirect_uri={SHOPIFY_REDIRECT_URI}"
        f"&state={state}"
    )

    return {
        "oauth_url":oauth_url
    }


