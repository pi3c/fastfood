from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import schemas
from fastfood.cruds import crud
from fastfood.dbase import get_async_session

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenu"],
)


@router.get("/")
async def get_submenus(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    result = await crud.get_submenus(menu_id=menu_id, session=session)
    return result.scalars().all()


@router.post("/", status_code=201)
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


@router.get("/{submenu_id}", response_model=schemas.SubMenuRead)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.get_submenu_item(
        menu_id=menu_id,
        submenu_id=submenu_id,
        session=session,
    )
    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")
    return result


@router.patch(
    "/{submenu_id}",
    response_model=schemas.MenuBase,
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.update_submenu_item(
        submenu_id=submenu_id,
        submenu=submenu,
        session=session,
    )
    return result.scalars().one()


@router.delete("/{submenu_id}")
async def delete_submenu(
    menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    await crud.delete_submenu_item(submenu_id=submenu_id, session=session)
