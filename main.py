import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from postgress_client.connection import Database



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("insight")

API_KEY = "e9e107d7d54b66f50e20b3412e3d22c5"
SCOPES = "read analytics"
REDIRECT_URI = "https://localhost:8000/auth/callback"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 App startup — attempting DB connection")
    try:
        await Database.connect()
        logger.info("✅ Database connected")
    except Exception:
        logger.exception("❌ Database connection failed")
    logger.info("🚀 App startup — attempting Redis connection")
    yield
    await Database.disconnect()
    logger.info("🛑 Database disconnected")

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