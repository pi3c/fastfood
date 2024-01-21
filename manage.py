import asyncio
import sys

import uvicorn

from fastfood.cruds import create_db_and_tables


def run_app():
    """
    Запуск FastAPI
    """
    uvicorn.run(
        app="fastfood.app:create_app",
        reload=True,
        factory=True,
    )


async def recreate():
    """Удаление и создание таблиц в базе данных для тестирования"""
    await create_db_and_tables()


if __name__ == "__main__":
    if "--run-server" in sys.argv:
        run_app()

    if "--run-test-server" in sys.argv:
        asyncio.run(recreate())
        run_app()
