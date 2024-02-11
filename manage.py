import asyncio
import multiprocessing
import sys
from subprocess import Popen

import uvicorn

from fastfood.repository import create_db_and_tables

loop = asyncio.get_event_loop()


def start_celery_worker() -> None:
    Popen(['celery', '-A', 'bg_tasks.bg_task.celery_app', 'worker', '--loglevel=info'])


def start_celery_beat() -> None:
    Popen(['celery', '-A', 'bg_tasks.bg_task.celery_app', 'beat', '--loglevel=info'])


celery_worker_process = multiprocessing.Process(target=start_celery_worker)
celery_beat_process = multiprocessing.Process(target=start_celery_beat)


async def run_app() -> None:
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


async def recreate() -> None:
    """Удаление и создание таблиц в базе данных для тестирования"""
    await create_db_and_tables()


if __name__ == '__main__':
    if '--run-celery' in sys.argv:
        celery_worker_process.start()
        celery_beat_process.start()

    if '--run-server' in sys.argv:
        pass

    if '--run-test-server' in sys.argv:
        celery_worker_process.start()
        celery_beat_process.start()

        loop.run_until_complete(recreate())
        loop.run_until_complete(run_app())

        celery_beat_process.kill()
        celery_worker_process.kill()
