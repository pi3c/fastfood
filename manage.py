import asyncio
import sys

import uvicorn

from fastfood.crud import create_db_and_tables


def run_app():
    """
    Запуск
    """
    uvicorn.run(
        app="fastfood.app:create_app",
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    if "filldb" in sys.argv:
        """Наполнение БД демонстрационными данными"""
        pass

    if "--run-server" in sys.argv:
        async def create():
            await create_db_and_tables()
        asyncio.run(create())
        run_app()
