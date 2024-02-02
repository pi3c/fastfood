from uuid import UUID

import redis.asyncio as redis
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.menu import MenuRepository
from fastfood.repository.redis import RedisRepository
from fastfood.schemas import MenuBase


class MenuService:
    def __init__(
        self,
        menu_repo: MenuRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ):
        self.menu_repo = menu_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_menus(self):
        data = await self.menu_repo.get_menus()
        return data

    async def create_menu(self, menu_data: MenuBase):
        data = await self.menu_repo.create_menu_item(menu_data)
        return data

    async def read_menu(self, menu_id: UUID):
        data = await self.menu_repo.get_menu_item(menu_id)
        return data

    async def update_menu(self, menu_id: UUID, menu_data):
        data = await self.menu_repo.update_menu_item(menu_id, menu_data)
        return data

    async def del_menu(self, menu_id: UUID):
        data = await self.menu_repo.delete_menu_item(menu_id)
        return data
