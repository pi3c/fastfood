from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood.dbase import get_async_session
from fastfood.models import Dish
from fastfood.schemas import Dish_db


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.db = session

    async def get_dishes(self, menu_id: UUID, submenu_id: UUID) -> list[Dish]:
        query = select(Dish).where(
            Dish.parent_submenu == submenu_id,
        )
        dishes = await self.db.execute(query)
        return [x for x in dishes.scalars().all()]

    async def create_dish_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: Dish_db,
    ) -> Dish:
        new_dish = Dish(**dish_data.model_dump())
        new_dish.parent_submenu = submenu_id
        self.db.add(new_dish)
        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def get_dish_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
    ) -> Dish | None:
        query = select(Dish).where(Dish.id == dish_id)
        submenu = await self.db.execute(query)
        return submenu.scalars().one_or_none()

    async def update_dish_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_data: Dish_db,
    ) -> Dish | None:
        query = update(Dish).where(Dish.id == dish_id).values(**dish_data.model_dump())
        await self.db.execute(query)
        await self.db.commit()
        qr = select(Dish).where(Dish.id == dish_id)
        updated_submenu = await self.db.execute(qr)
        return updated_submenu.scalar_one_or_none()

    async def delete_dish_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
    ) -> None:
        query = delete(Dish).where(Dish.id == dish_id)
        await self.db.execute(query)
        await self.db.commit()
