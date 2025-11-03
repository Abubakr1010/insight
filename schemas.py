from pydantic import BaseModel, EmailStr
from datetime import datetime

# -------------------------------
# User Models
# -------------------------------

class UserCreate(BaseModel):
    email: EmailStr

class UserRead(BaseModel):
    id: int 
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

# -------------------------------
# Store Models
# -------------------------------

class StoreCreate(BaseModel):
    user_id: int
    shop_domain: str
    access_token: str

class StoreRead(BaseModel):
    id: int
    user_id: int
    shop_domain: str 
    created_at: datetime
    updated_at: datetime

# -------------------------------
# OTP Models
# -------------------------------

class UserOTPCreate(BaseModel):
    email: EmailStr
    otp_code: str
    expires_at: datetime

class UserOTPRead(BaseModel):
    id: int
    email: EmailStr
    otp_code: str
    expires_at: datetime
    used: bool
    created_at: datetime

class UserOTPVerify(BaseModel):
    email: EmailStr
    otp_code: str
