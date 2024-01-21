from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import schemas
from fastfood.utils import price_converter
from fastfood.cruds import crud
from fastfood.dbase import get_async_session


router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dish"],
)


@router.get("/")
async def get_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    result = await crud.get_dishes(submenu_id=submenu_id, session=session)
    return result


@router.post("/", status_code=201)
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
    return price_converter(result)


@router.get("/{dish_id}")
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
    return price_converter(result)


@router.patch(
    "/{dish_id}"
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: schemas.DishBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_dish_item(
        dish_id=dish_id, dish=dish, session=session,
    )
    return price_converter(result)


@router.delete("/{dish_id}")
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)):
    await crud.delete_dish_item(dish_id=dish_id, session=session)
