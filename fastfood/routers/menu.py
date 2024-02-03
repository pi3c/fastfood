from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from fastfood.schemas import Menu, MenuBase, MenuRead
from fastfood.service.menu import MenuService

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['menu'],
)


@router.get('/', response_model=list[Menu])
async def get_menus(
    menu: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await menu.read_menus()


@router.post('/', status_code=201, response_model=Menu)
async def add_menu(
    menu: MenuBase,
    responce: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await responce.create_menu(menu)


@router.get('/{menu_id}', response_model=MenuRead)
async def get_menu(
    menu_id: UUID,
    responce: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await responce.read_menu(menu_id=menu_id)

    if not result:
        raise HTTPException(status_code=404, detail='menu not found')
    return result


@router.patch('/{menu_id}', response_model=MenuRead)
async def update_menu(
    menu_id: UUID,
    menu: MenuBase,
    responce: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await responce.update_menu(
        menu_id=menu_id,
        menu_data=menu,
    )
    return result.scalars().one()


@router.delete('/{menu_id}')
async def delete_menu(
    menu_id: UUID,
    menu: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    await menu.del_menu(menu_id)
