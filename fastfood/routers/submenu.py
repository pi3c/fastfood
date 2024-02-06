from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from fastfood.schemas import MenuBase, SubMenuRead
from fastfood.service.submenu import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['submenu'],
)


@router.get(
    '/',
    response_model=list[SubMenuRead],
    summary='Получить список подменю',
    description='Этот метод позволяет получить список подменю основного меню'
    ' по UUID меню',
)
async def get_submenus(
    menu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> list[SubMenuRead]:
    result = await submenu.read_submenus(menu_id=menu_id)
    return result


@router.post(
    '/',
    status_code=201,
    response_model=SubMenuRead,
    summary='Создать подменю',
    description='Этот метод позволяет создать подменю по UUID родителского меню',
)
async def create_submenu_item(
    menu_id: UUID,
    submenu_data: MenuBase,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> SubMenuRead:
    result = await submenu.create_submenu(
        menu_id=menu_id,
        submenu_data=submenu_data,
    )
    return result


@router.get(
    '/{submenu_id}',
    response_model=SubMenuRead,
    summary='Получить подменю',
    description='Этот метод позволяет получить подменю по его UUID'
    ' и UUID родительского меню',
    responses={
        404: {
            'description': 'Submenu not found',
            'content': {'application/json': {'example': {'detail': 'string'}}},
        },
    },
)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> SubMenuRead:
    result = await submenu.read_menu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'Подменю c UUID={submenu_id} не существует, доступ невозможен',
        )
    return result


@router.patch(
    '/{submenu_id}',
    response_model=SubMenuRead,
    summary='Обновить подменю',
    description='Этот метод позволяет обновить подменю по его UUID'
    ' и UUID родительского меню',
    responses={
        404: {
            'description': 'Submenu not found',
            'content': {'application/json': {'example': {'detail': 'string'}}},
        },
    },
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_data: MenuBase,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> SubMenuRead:
    result = await submenu.update_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        submenu_data=submenu_data,
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'Gjlvеню c UUID={submenu_id} не существует, обновление невозможно',
        )

    return result


@router.delete(
    '/{submenu_id}',
    summary='Удалить подменю',
    description='Этот метод позволяет удалить подменю по его UUID',
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: SubmenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> None:
    await submenu.del_menu(menu_id=menu_id, submenu_id=submenu_id)
