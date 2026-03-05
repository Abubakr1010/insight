import os
from typing import Dict
from fastapi import APIRouter
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

router = APIRouter(tags=["email"])

@router.post("/mail")
async def send_mail() -> Dict:
    params: resend.Emails.SendParams = {
        "from": "Insight <abubakriqbal1997@gmail.co>",
        "to": ["delivered@resend.dev"],
        "subject": "hello world",
        "html": "<strong>it works!</strong>",
    }
    email = await resend.Emails.send_async(params)
    return email