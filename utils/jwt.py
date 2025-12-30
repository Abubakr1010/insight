import os
from datetime import datetime,timedelta, timezone
from jose import jwt


ACCESS_SECRET = os.getenv("ACCESS_SECRET")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
ALGO = os.getenv("ALGO")


def create_access_token(data:dict, expires_minutes = 10):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(to_encode, ACCESS_SECRET, algorithm=ALGO)



def create_refresh_secret(data:dict, expires_days = 30):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(days=expires_days)
    return jwt.encode(to_encode, REFRESH_SECRET, algorithm=ALGO)



def generate_tokens(user_id: int):
    data = {"sub": str(user_id)}
    access_token = create_access_token(data)
    refresh_token = create_refresh_secret(data)
    return access_token, refresh_token
