from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

from pyazo_api.config import settings


pool: AsyncConnectionPool | None = None


def get_pool() -> AsyncConnectionPool:
    if pool is None:
        raise RuntimeError("Database pool not initialized")
    return pool


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global pool
    pool = AsyncConnectionPool(settings.database_url, open=False)
    await pool.open()
    try:
        yield
    finally:
        await pool.close()
        pool = None
