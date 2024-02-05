from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from fastfood.schemas import MenuBase, SubMenuRead
from fastfood.service.submenu import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['submenu'],
)


@router.get('/', response_model=list[SubMenuRead])
async def get_submenus(
    menu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await submenu.read_submenus(menu_id=menu_id)
    return result


@router.post('/', status_code=201, response_model=SubMenuRead)
async def create_submenu_item(
    menu_id: UUID,
    submenu_data: MenuBase,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await submenu.create_submenu(
        menu_id=menu_id,
        submenu_data=submenu_data,
    )
    return result


@router.get('/{submenu_id}', response_model=SubMenuRead)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await submenu.read_menu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if not result:
        raise HTTPException(status_code=404, detail='submenu not found')
    return result


@router.patch(
    '/{submenu_id}',
    response_model=SubMenuRead,
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_data: MenuBase,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await submenu.update_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        submenu_data=submenu_data,
    )
    return result


@router.delete('/{submenu_id}')
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    await submenu.del_menu(menu_id=menu_id, submenu_id=submenu_id)
