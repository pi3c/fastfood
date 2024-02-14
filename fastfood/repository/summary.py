from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastfood.dbase import get_async_session
from fastfood.models import Menu, SubMenu


class SummaryRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.db = session

    async def get_data(self) -> list[Any]:
        query = select(Menu).options(
            selectinload(Menu.submenus).selectinload(SubMenu.dishes)
        )
        data = await self.db.execute(query)
        return [x for x in data.scalars().all()]
