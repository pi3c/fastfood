from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from fastfood import schemas
from fastfood.service.dish import DishService
from fastfood.utils import price_converter

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dish'],
)


@router.get('/')
async def get_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await dish.read_dishes(menu_id, submenu_id)
    return result


@router.post('/', status_code=201)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_data: schemas.DishBase,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await dish.create_dish(
        menu_id,
        submenu_id,
        dish_data,
    )
    return price_converter(result)


@router.get('/{dish_id}')
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await dish.read_dish(
        menu_id,
        submenu_id,
        dish_id,
    )
    if not result:
        raise HTTPException(status_code=404, detail='dish not found')
    return price_converter(result)


@router.patch('/{dish_id}')
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_data: schemas.DishBase,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await dish.update_dish(
        menu_id,
        submenu_id,
        dish_id,
        dish_data,
    )
    return price_converter(result)


@router.delete('/{dish_id}')
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: DishService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    await dish.del_dish(menu_id, submenu_id, dish_id)
