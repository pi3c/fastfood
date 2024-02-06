import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastfood.app import create_app
from fastfood.config import settings
from fastfood.dbase import get_async_session
from fastfood.models import Base

async_engine = create_async_engine(settings.TESTDATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def db_init(event_loop):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def client(event_loop) -> AsyncGenerator[AsyncClient, None]:
    app: FastAPI = create_app()
    app.dependency_overrides[get_async_session] = get_test_session

    async with AsyncClient(
        app=app,
        base_url='http://localhost:8000',
    ) as async_client:
        yield async_client
