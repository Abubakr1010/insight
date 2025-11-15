from fastapi import Request
from main import app

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@app.middleware("http")
async def email_is_present(request:Request, call_next):
    if request.headers.get("content_type") == "application/json":
        body = await request.json()
        email = body.get("email")

        if not email:
            return
        
        if not re.match(EMAIL_REGEX, email):
            return 
        
        response = await call_next(request)
        return response



