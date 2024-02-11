import asyncio

from celery import Celery

from .updater import main

loop = asyncio.get_event_loop()


celery_app = Celery(
    'tasks',
    broker='amqp://guest:guest@localhost',
    backend='rpc://',
    include=['bg_tasks.bg_task'],
)

celery_app.conf.beat_schedule = {
    'run-task-every-15-seconds': {
        'task': 'bg_tasks.bg_task.periodic_task',
        'schedule': 15.0,
    },
}


@celery_app.task
def periodic_task() -> None:
    result = loop.run_until_complete(main())
    return result
