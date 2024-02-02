from uuid import UUID

import redis.asyncio as redis
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.dish import DishRepository
from fastfood.repository.redis import RedisRepository
from fastfood.schemas import DishBase


class DishService:
    def __init__(
        self,
        dish_repo: DishRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ):
        self.dish_repo = dish_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_dishes(self, menu_id: UUID, submenu_id: UUID):
        data = await self.dish_repo.get_dishes(menu_id, submenu_id)
        return data

    async def create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: DishBase,
    ):
        data = await self.dish_repo.create_dish_item(
            menu_id,
            submenu_id,
            dish_data,
        )
        return data

    async def read_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        data = await self.dish_repo.get_dish_item(menu_id, submenu_id, dish_id)
        return data

    async def update_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id, dish_data: DishBase
    ):
        data = await self.dish_repo.update_dish_item(
            menu_id, submenu_id, dish_id, dish_data
        )
        return data

    async def del_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        data = await self.dish_repo.delete_dish_item(
            menu_id,
            submenu_id,
            dish_id,
        )
        return data
