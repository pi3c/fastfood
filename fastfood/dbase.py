from typing import AsyncGenerator

import redis.asyncio as redis  # type: ignore
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastfood.config import settings

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_redis_pool():
    return redis.from_url(settings.REDIS_DB, decode_responses=False)


async def get_async_redis_client(
    redis_pool: redis.Redis = Depends(get_redis_pool),
):
    return redis_pool
