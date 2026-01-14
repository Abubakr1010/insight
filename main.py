import logging, os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.otp import router as otp_router
from routes.shopify import router as shopify_router
from postgress_client.connection import Database
from utils.domain_error import (PermissionDenied, 
                                NotFoundError, 
                                DatabaseError, 
                                BadRequest,
                                NotAuthenticatedUser)
from utils.error_handlers import (permission_denied_handler, 
                                  not_found_handler, 
                                  database_error_handler, 
                                  bad_request, 
                                  not_authenticated_user)
from starlette.middleware.sessions import SessionMiddleware





#why we need shopify env variable in docker compose


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("insight")

load_dotenv()

API_KEY = os.environ.get("API_KEY")
SCOPES = os.environ.get("SCOPES")
SECRET = os.environ.get("SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 App startup — attempting DB connection")
    try:
        await Database.connect()
        logger.info("✅ Database connected")
    except Exception:
        logger.exception("❌ Database connection failed")
        raise  # <-- fail startup if DB cannot connect
    logger.info("🚀 App startup — attempting Redis connection")
    
    yield 

    # Shutdown
    try:
        await Database.disconnect()
        logger.info("🛑 Database disconnected")
    except Exception:
        logger.exception("❌ Error during DB disconnect")

# -----------------------
# App instance
# -----------------------

app = FastAPI(lifespan=lifespan)

# -----------------------
# Register global error handlers
# -----------------------

app.include_router(otp_router)
app.include_router(shopify_router)

app.add_middleware(SessionMiddleware, secret_key=SECRET)

app.add_exception_handler(PermissionDenied, permission_denied_handler)
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(BadRequest, bad_request)
app.add_exception_handler(NotAuthenticatedUser, not_authenticated_user)
  

