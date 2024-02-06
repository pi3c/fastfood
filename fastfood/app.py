import json

from fastapi import FastAPI

from fastfood.routers.dish import router as dish_router
from fastfood.routers.menu import router as menu_router
from fastfood.routers.submenu import router as submenu_router


def create_app() -> FastAPI:
    """
    Фабрика FastAPI.
    """
    app = FastAPI()
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    def custom_openapi():
        with open('openapi.json') as openapi:
            return json.load(openapi)

    app.openapi = custom_openapi

    return app
