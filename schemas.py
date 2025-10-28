from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr

class UserRead(BaseModel):
    id: int 
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

class StoreCreate(BaseModel):
    user_id: int
    shop_domain: str
    access_domain: str

class StoreRead(BaseModel):
    id: int
    user_id: int
    shop_domain: str 
    created_at: datetime
    updated_at: datetime

