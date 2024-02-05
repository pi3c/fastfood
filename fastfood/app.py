import json

from fastapi import FastAPI

from fastfood.routers.dish import router as dish_router
from fastfood.routers.menu import router as menu_router
from fastfood.routers.submenu import router as submenu_router

tags_metadata = [
    {
        'name': 'menu',
        'description': 'Операции с меню.',
    },
    {
        'name': 'submenu',
        'description': 'Подменю и работа с ним',
    },
    {'name': 'dish', 'description': 'Блюда и работа с ними'},
]


def create_app(redis=None) -> FastAPI:
    """
    Фабрика FastAPI.
    """
    with open('openapi.json') as f:
        js = json.load(f)

    app = FastAPI(
        title=js['info']['title'],
        description=js['info']['description'],
        version=js['info']['version'],
        contact={
            'name': 'Sergey Vanyushkin',
            'url': 'http://pi3c.ru',
            'email': 'pi3c@yandex.ru',
        },
        license_info={
            'name': 'MIT license',
            'url': 'https://mit-license.org/',
        },
        openapi_tags=tags_metadata,
    )
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    return app
