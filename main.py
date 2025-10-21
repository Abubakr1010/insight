import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from postgress_client.connection import Database



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("insight")


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