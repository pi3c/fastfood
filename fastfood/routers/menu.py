from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import schemas
from fastfood.cruds import crud
from fastfood.dbase import get_async_session
from fastfood.service.menu import MenuService

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["menu"],
)


@router.get("/", response_model=Optional[List[schemas.Menu]])
async def get_menus(
    menu: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await menu.read_menus()
    return result


@router.post("/", status_code=201, response_model=schemas.Menu)
async def add_menu(
    menu: schemas.MenuBase,
    responce: MenuService = Depends(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    rspn = await responce.create_menu(menu)
    return rspn


@router.get("/{menu_id}", response_model=schemas.MenuRead)
async def get_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.get_menu_item(menu_id=menu_id, session=session)

    if not result:
        raise HTTPException(status_code=404, detail="menu not found")
    return result


@router.patch("/{menu_id}", response_model=schemas.MenuBase)
async def update_menu(
    menu_id: UUID,
    menu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_menu_item(
        menu_id=menu_id,
        menu=menu,
        session=session,
    )
    return result.scalars().one()


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    await crud.delete_menu_item(menu_id=menu_id, session=session)
