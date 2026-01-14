import os
from datetime import datetime, timezone
from fastapi import Depends
from utils import domain_error
from postgress_client import queries, connection
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer



SECRET = os.environ.get("ACCESS_SECRET")
if not SECRET:
    raise RuntimeError("SECRET environment variable not set!")
print("SECRET =", SECRET, type(SECRET))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/verify")

async def get_user_by_email(email:str):
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(queries.GET_USER_BY_EMAIL,email)
        return user



async def get_user_by_id(user_id:str):
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(queries.GET_USER_BY_ID,user_id)
        return user



async def create_user(email: str):
    pool = connection.Database.get_pool()
    print("Pool:", pool)
    async with pool.acquire() as conn:
        print("Connection acquired:", conn)
        new_user = await conn.fetchrow(
            queries.CREATE_USER,
            email,
            datetime.now(),
            ""
        )
        print("Inserted user:", new_user)
        return new_user

    


async def get_current_user(token = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        print("Secret used:", payload)
        user_id= payload.get("sub")
        print("Email token:", user_id)

        if not user_id:
            raise domain_error.NotAuthenticatedUser()
    
        user = await get_user_by_id(int(user_id))
        print("User from DB:", user)

        if not user:
            raise domain_error.NotAuthenticatedUser()

       
        return user 
    except JWTError as exc:
        print("JWT Error:", exc)   
        raise domain_error.NotAuthenticatedUser() from exc

    
    
    


