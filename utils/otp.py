import random
from datetime import datetime, timezone
from postgress_client import queries, connection



def generate_otp(length=4):
    
    otp_digits = []

    for _ in range(length):
        digit = random.randint(0, 9)
        otp_digits.append(str(digit))

    otp = "".join(otp_digits)
    return otp



async def save_otp(email: str, otp_code:str, expires_at: datetime):
    query = queries.SAVE_OTP
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn: 
        await conn.execute(
            query,email,otp_code,expires_at,datetime.now(timezone.utc)
        )
    


async def get_otp_by_email(email: str):
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(queries.GET_OTP_BY_EMAIL, email)
        return user


    
async def mark_otp_as_used(otp_id:int):
    pool = connection.Database.get_pool()
    async with pool.acquire() as conn:
        await conn.execute(queries.MARK_OTP_USED, otp_id)

    

async def validate_otp(email: str, otp_code: str):
    otp_record = await get_otp_by_email(email)

    if not otp_record:
        return False
    if otp_record['used']:
        return False
    if otp_record['expires_at'] < datetime.now(timezone.utc):
        return False
    if otp_record['otp_code'] != otp_code:
        return False
    
    await mark_otp_as_used(otp_record['id'])
    return True

