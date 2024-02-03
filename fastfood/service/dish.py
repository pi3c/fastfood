from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.dish import DishRepository
from fastfood.repository.redis import RedisRepository
from fastfood.schemas import Dish, Dish_db, DishBase


class DishService:
    def __init__(
        self,
        dish_repo: DishRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:
        self.dish_repo = dish_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_dishes(self, menu_id: UUID, submenu_id: UUID) -> list[Dish]:
        data = await self.dish_repo.get_dishes(menu_id, submenu_id)
        response = []
        for row in data:
            dish = row.__dict__
            dish['price'] = str(dish['price'])
            response.append(Dish(**dish))
        return response

    async def create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: DishBase,
    ) -> Dish:
        dish = Dish_db(**dish_data.model_dump())
        data = await self.dish_repo.create_dish_item(
            menu_id,
            submenu_id,
            dish,
        )
        response = data.__dict__
        response['price'] = str(response['price'])
        return Dish(**response)

    async def read_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish | None:
        data = await self.dish_repo.get_dish_item(menu_id, submenu_id, dish_id)
        if data is None:
            return None
        response = data.__dict__
        response['price'] = str(response['price'])
        return Dish(**response)

    async def update_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id, dish_data: DishBase
    ) -> Dish:
        dish = Dish_db(**dish_data.model_dump())
        data = await self.dish_repo.update_dish_item(menu_id, submenu_id, dish_id, dish)
        response = data.__dict__
        response['price'] = str(response['price'])
        return Dish(**response)

    async def del_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> int:
        response = await self.dish_repo.delete_dish_item(
            menu_id,
            submenu_id,
            dish_id,
        )
        return response
