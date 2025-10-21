import os
import asyncpg
from typing import Optional


db_pool = None

# Load database credentials from environment
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "mydb")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(DB_URL)
        return cls._pool

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError("Database pool is not initialized.")
        return cls._pool

    @classmethod
    async def disconnect(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None


async def get_db():
    pool = Database.get_pool()
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


