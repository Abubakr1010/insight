from datetime import datetime, timezone
from postgress_client import queries, connection



async def get_user_by_email(email:str):
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(queries.GET_OTP_BY_EMAIL,email)
        return user



async def create_user(email:str):
    pool = connection.Database.get_pool()
    async with pool.aquire() as conn:
        new_user = await conn.fetchrow(queries.CREATE_USER, 
                              email, datetime.now(timezone.utc))
        return new_user
    

