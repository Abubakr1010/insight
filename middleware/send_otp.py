# from fastapi import Request
# from utils.error_handlers import BadRequest
# from fastapi.responses import JSONResponse
# from main import app
# import re

# EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# @app.middleware("http")
# async def email_is_present(request:Request, call_next):
#     if request.headers.get("content_type", "") == "application/json":
#         body = await request.json()
#         email = body.get("email")

#         if not email:
#             raise BadRequest(detail= "email is required")
        
#         if not re.match(EMAIL_REGEX, email):
#             raise BadRequest(detail= "Invalid email format")
        
#         response = await call_next(request)
#         return response


