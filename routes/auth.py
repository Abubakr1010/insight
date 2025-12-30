import httpx
from main import app, API_KEY, SECRET 
from utils.domain_error import PermissionDenied, DatabaseError
from fastapi.responses import RedirectResponse
from postgress_client import queries
from postgress_client.connection import Database
from fastapi import Request



@app.get("/auth/callback")
async def shopify_callback(request:Request, code: str, shop:str, state:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{shop}/admin/oauth/access_token",
                data={
                    "client_id": API_KEY,
                    "client_secret": SECRET,
                    "code": code
                }
            )
        if response.status_code != 200:
            return PermissionDenied(detail=f"Shopify toke exchange failed: {response.text}")
        
        data = response.json()
        access_token = data["access_token"]

        pool = await Database.connect()
        async with pool.acquire() as conn:
            user_id = request.state
            if not user_id:
                raise PermissionDenied(detail="User not authoraused")
            
        existing_store = await conn.fetchrow(queries.FETCH_STORE,shop)

        if existing_store:
            await conn.execute(queries.UPDATE_STORE, access_token,shop)
        else:
            await conn.execute(queries.INSERT_STORE, user_id, shop, access_token)

    except DatabaseError as e:
        raise e
    
    return RedirectResponse(url="myapp://shopify-connected?success=true")

