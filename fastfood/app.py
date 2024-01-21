from fastapi import FastAPI

from fastfood.routers.menu import router as menu_router
from fastfood.routers.submenu import router as submenu_router
from fastfood.routers.dish import router as dish_router


description = """
# 🔥🔥🔥Fastfood-API поможет тебе подкрепиться 🔥🔥🔥

### У нас есть Menu. Ты можеш выбрать блюда из кухни, которая тебе нравится

## Menu

Ты можешь **add menu**.

Ты можешь **read menu**.

Ты можешь **patch menu**.

Ты можешь **delete menu**.

### У нас есть в SubMenu, где ты сможешь найти
десерты/напитки/супчики/прочие вкусности

# SubMenu

Ты можешь **add submenu into menu**.

Ты можешь **read submenu**.

Ты можешь **patch submenu**.

Ты можешь **delete menu**.

### У нас есть в Dish, где ты сможешь найти блюдо по вкусу

# Dish

Ты можешь **add dish into submenu**.

Ты можешь **read dish**.

Ты можешь **patch dish**.

Ты можешь **delete dish**.

## Приятного аппетита
"""


tags_metadata = [
    {
        "name": "menu",
        "description": "Операции с меню.",
    },
    {
        "name": "submenu",
        "description": "Подменю и работа с ним",
    },
    {
        "name": "dish",
        "description": "Блюда и работа с ними"
    },
]


def create_app():
    """
    Фабрика FastAPI.
    """
    app = FastAPI(
        title="Fastfood-API",
        description=description,
        version="0.0.1",
        contact={
            "name": "Sergey Vanyushkin",
            "url": "http://pi3c.ru",
            "email": "pi3c@yandex.ru",
        },
        license_info={
            "name": "MIT license",
            "url": "https://mit-license.org/",
        },
        openapi_tags=tags_metadata,
    )
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    return app
