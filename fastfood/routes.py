from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import schemas
from fastfood.crud import Crud as crud
from fastfood.dbase import get_async_session


router = APIRouter()


@router.get("/api/v1/menus", response_model=Optional[List[schemas.Menu]])
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    result = await crud.get_menus(session=session)
    return result


@router.post("/api/v1/menus", status_code=201, response_model=schemas.Menu)
async def add_menu(
    menu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.create_menu_item(
        menu=menu,
        session=session,
    )
    return result


@router.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
async def get_menu(
        menu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    result = await crud.get_menu_item(menu_id=menu_id, session=session)
    if not result:
        raise HTTPException(status_code=404, detail="menu not found")
    return result


@router.patch("/api/v1/menus/{menu_id}", response_model=schemas.MenuBase)
async def update_menu(
    menu_id: UUID,
    menu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_menu_item(
        menu_id=menu_id, menu=menu, session=session,
    )
    return result


@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(
        menu_id: UUID, session: AsyncSession = Depends(get_async_session),
):
    await crud.delete_menu_item(menu_id=menu_id, session=session)


@router.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    result = await crud.get_submenus(menu_id=menu_id, session=session)
    return result


@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def create_submenu_item(
    menu_id: UUID,
    submenu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.create_submenu_item(
        menu_id=menu_id,
        submenu=submenu,
        session=session,
    )
    return result


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.get_submenu_item(
        menu_id=menu_id, submenu_id=submenu_id, session=session,
    )
    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")
    return result


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.MenuBase,
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_submenu_item(
        submenu_id=submenu_id, submenu=submenu, session=session,
    )
    return result


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    await crud.delete_submenu_item(submenu_id=submenu_id, session=session)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    result = await crud.get_dishes(submenu_id=submenu_id, session=session)
    return result


@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: schemas.DishBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.create_dish_item(
        submenu_id=submenu_id,
        dish=dish,
        session=session,
    )
    return result


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.get_dish_item(
        dish_id=dish_id, session=session,
    )
    if not result:
        raise HTTPException(status_code=404, detail="dish not found")
    return result


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.DishBase,
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: schemas.DishBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_dish_item(
        dish_id=dish_id, dish=dish, session=session,
    )
    return result


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)):
    await crud.delete_dish_item(dish_id=dish_id, session=session)
