from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from fastfood.schemas import Dish, DishBase
from fastfood.service.dish import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dish'],
)


@router.get(
    '/',
    response_model=list[Dish],
    summary='Получить список блюд',
    description='Этот метод позволяет получить список всех блюда по UUID'
    ' родительских меню и подменю',
)
async def get_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> list[Dish]:
    result = await dish.read_dishes(menu_id, submenu_id)
    return result


@router.post(
    '/',
    status_code=201,
    response_model=Dish,
    summary='Создать блюдо',
    description='Этот метод позволяет создать блюдо по UUID'
    'его родительских меню и подменю',
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_data: DishBase,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> Dish:
    return await dish.create_dish(
        menu_id,
        submenu_id,
        dish_data,
    )


@router.get(
    '/{dish_id}',
    response_model=Dish,
    summary='Получить блюдо',
    description='Этот метод позволяет получить блюдо по его UUID'
    ' и UUID его родительских меню',
    responses={
        404: {
            'description': 'Dish not found',
            'content': {'application/json': {'example': {'detail': 'string'}}},
        },
    },
)
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> Dish:
    result = await dish.read_dish(
        menu_id,
        submenu_id,
        dish_id,
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'Блюдо c UUID={dish_id} не существует, доступ невозможен',
        )
    return result


@router.patch(
    '/{dish_id}',
    response_model=Dish,
    summary='Обновить блюдо',
    description='Этот метод позволяет обновить блюдо по его UUID'
    ' и UUID родительских меню',
    responses={
        404: {
            'description': 'Dish not found',
            'content': {'application/json': {'example': {'detail': 'string'}}},
        },
    },
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_data: DishBase,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> Dish:
    result = await dish.update_dish(
        menu_id,
        submenu_id,
        dish_id,
        dish_data,
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'Блюдо c UUID={dish_id} не существует, обновление невозможно',
        )
    return result


@router.delete(
    '/{dish_id}',
    summary='Удалить блюдо',
    description='Этот метод позволяет удалить блюдо по его UUID'
    ' и UUID родительских меню',
)
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> None:
    await dish.del_dish(menu_id, submenu_id, dish_id)
