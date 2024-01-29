import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
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


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.dependency_overrides[get_async_session] = get_test_session
    yield app


@pytest_asyncio.fixture(scope="function")
async def client(app):
    async with AsyncClient(
        app=app, base_url="http://localhost:8000/api/v1/menus",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function")
async def asession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
