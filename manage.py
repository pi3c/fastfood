import asyncio
import json
import sys

import uvicorn
from fastapi.openapi.utils import get_openapi

from fastfood.app import create_app
from fastfood.repository import create_db_and_tables


def create_openapi():
    app = create_app()

    with open('openapi.json', 'w') as f:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
                contact=app.contact,
                license_info=app.license_info,
                tags=app.openapi_tags,
            ),
            f,
        )


def run_app():
    """
    Запуск FastAPI
    """
    uvicorn.run(
        app='fastfood.app:create_app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        factory=True,
        workers=1,
    )


async def recreate():
    """Удаление и создание таблиц в базе данных для тестирования"""
    await create_db_and_tables()


if __name__ == '__main__':
    if '--run-server' in sys.argv:
        run_app()

    if '--run-test-server' in sys.argv:
        asyncio.run(recreate())
        run_app()

    if 'dump' in sys.argv:
        create_openapi()
