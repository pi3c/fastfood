import asyncio

from celery import Celery

from fastfood.config import settings

from .updater import main, main_gsheets

loop = asyncio.get_event_loop()


celery_app = Celery(
    'tasks',
    broker=settings.REBBITMQ_URL,
    backend='rpc://',
    include=['bg_tasks.bg_task'],
)

celery_app.conf.beat_schedule = {
    'run-task-every-15-seconds': {
        'task': 'bg_tasks.bg_task.periodic_task',
        'schedule': 30.0,
    },
}

celery_app_google = Celery(
    'tasks',
    broker=settings.REBBITMQ_URL,
    backend='rpc://',
    include=['bg_tasks.bg_task'],
)

celery_app_google.conf.beat_schedule = {
    'run-task-every-15-seconds': {
        'task': 'bg_tasks.bg_task.periodic_task_google',
        'schedule': 30.0,
    },
}


@celery_app_google.task
def periodic_task_google() -> None:
    result = loop.run_until_complete(main_gsheets())
    return result


@celery_app.task
def periodic_task() -> None:
    result = loop.run_until_complete(main())
    return result
