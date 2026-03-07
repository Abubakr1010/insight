import os
from typing import Dict
import resend
import asyncio
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


async def send_email(email: str, otp: str):
    params = {
        "from": "Insight <onboarding@resend.dev>",  # testing sender
        "to": [email],
        "subject": "Your OTP Code",
        "html": f"""
        <h2>Email Verification</h2>
        <p>Your OTP code is:</p>
        <h1>{otp}</h1>
        <p>This code expires in 5 minutes.</p>
        """,
    }
    # Resend SDK is synchronous; wrap in thread for async
    return await asyncio.to_thread(resend.Emails.send, params)