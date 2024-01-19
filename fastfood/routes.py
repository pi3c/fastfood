from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from sqlalchemy import insert, select

from fastfood import models, schemas
from fastfood.dbase import get_async_session


router = APIRouter()


@router.get("/api/v1/menus")
async def read_menu(session: AsyncSession = Depends(get_async_session)):
    stmt = select(models.Menu)
    result = await session.execute(stmt)
    data = result.mappings().all()
    return data


@router.post("/api/v1/menus", status_code=201)
async def add_menu(menu: schemas.MenuBase, session: AsyncSession = Depends(get_async_session)):
    """
    docstring
    """
    stmt = insert(models.Menu).values(**menu.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
    
