from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas
from fastfood.crud import Crud as crud
from fastfood.dbase import get_async_session

router = APIRouter()


@router.get("/api/v1/menus")
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    result = await crud.get_menus(session=session)
    return result


@router.post("/api/v1/menus", status_code=201)
async def add_menu(
    menu: schemas.MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = insert(models.Menu).values(**menu.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
