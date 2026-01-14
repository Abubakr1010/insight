from fastapi import Request, APIRouter, Depends
from utils.user import get_current_user



router = APIRouter(tags=["auth"])

@router.get("/user")
async def read_current_user(current_user = Depends(get_current_user)):
    return {
            "id":current_user["id"],
            "email": current_user["email"], 
            "is_active":current_user["is_active"]
            }



