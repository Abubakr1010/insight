import logging, os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.otp import router
from fastapi.responses import RedirectResponse
from postgress_client.connection import Database
from utils.domain_error import (PermissionDenied, NotFoundError, DatabaseError, BadRequest)
from utils.error_handlers import (permission_denied_handler, not_found_handler, database_error_handler, bad_request)


#why we use  keys in docker compose
#how alembic is updated
#how await works/coruntine
#create a map of container and how they work basic knowledge also about images (why we need to create image and if in 
# compose do we need to run seperatly for container)


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


@app.get("/auth/install")
def install(shop:str):
    redirect_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={API_KEY}"
        f"&scope={SCOPES}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=random_string"
    )
    return RedirectResponse(url=redirect_url)

# -----------------------
# Register global error handlers
# -----------------------

app.include_router(router)

app.add_exception_handler(PermissionDenied, permission_denied_handler)
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(BadRequest, bad_request)


