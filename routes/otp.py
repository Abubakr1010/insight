from fastapi import APIRouter, status
from utils.domain_error import BadRequest
from utils.jwt import generate_tokens
from utils.user import get_user_by_email, create_user
from schemas import OTPResponse, OTPRequest, TokenResponse, OTPVerify
from utils.otp import generate_otp, save_otp, validate_otp
from datetime import datetime, timezone, timedelta


router = APIRouter(prefix="/otp", tags=["otp"])

@router.post("/send", status_code=status.HTTP_201_CREATED, response_model=OTPResponse)
async def otp_request(data: OTPRequest):
    email = data.email
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    await save_otp(email=email, otp_code=otp, expires_at=expires_at)
    return OTPResponse(email=email, otp_code=otp, expires_at=expires_at)



@router.post("/verify", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def verify_otp(data: OTPVerify):
    valid = await validate_otp(data.email, data.otp_code)
    if not valid:
        raise BadRequest(detail="Invalid OTP")
    
    user = await get_user_by_email(data.email)
    if not user:
        user = await create_user(email=data.email)

    access,refresh = generate_tokens(user['id'])

    return TokenResponse(access_token=access, refresh_token=refresh)

