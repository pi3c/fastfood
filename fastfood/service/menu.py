from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.menu import MenuRepository
from fastfood.repository.redis import RedisRepository
from fastfood.schemas import MenuBase, MenuRead


class MenuService:
    def __init__(
        self,
        menu_repo: MenuRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:
        self.menu_repo = menu_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_menus(self) -> list[MenuRead]:
        data = await self.menu_repo.get_menus()
        menus = []
        for r in data:
            menu = r.__dict__
            menu = {k: v for k, v in menu.items() if not k.startswith('_')}
            dishes_conter = 0
            for sub in r.submenus:
                dishes_conter += len(sub.dishes)

            menu['submenus_count'] = len(menu.pop('submenus'))
            menu['dishes_count'] = dishes_conter
            menu = MenuRead(**menu)
            menus.append(menu)
        return menus

    async def create_menu(self, menu_data: MenuBase) -> MenuRead:
        data = await self.menu_repo.create_menu_item(menu_data)
        menu = data.__dict__
        menu = {k: v for k, v in menu.items() if not k.startswith('_')}
        dishes_conter = 0

        for sub in data.submenus:
            dishes_conter += len(sub.dishes)
        menu['submenus_count'] = len(menu.pop('submenus'))
        menu['dishes_count'] = dishes_conter

        return MenuRead(**menu)

    async def read_menu(self, menu_id: UUID) -> MenuRead | None:
        data = await self.menu_repo.get_menu_item(menu_id)
        if data is None:
            return None
        menu = data.__dict__
        menu = {k: v for k, v in menu.items() if not k.startswith('_')}
        dishes_conter = 0

        for sub in data.submenus:
            dishes_conter += len(sub.dishes)
        menu['submenus_count'] = len(menu.pop('submenus'))
        menu['dishes_count'] = dishes_conter

        return MenuRead(**menu)

    async def update_menu(self, menu_id: UUID, menu_data) -> MenuRead:
        data = await self.menu_repo.update_menu_item(menu_id, menu_data)
        menu = data.__dict__
        menu = {k: v for k, v in menu.items() if not k.startswith('_')}
        dishes_conter = 0

        for sub in data.submenus:
            dishes_conter += len(sub.dishes)
        menu['submenus_count'] = len(menu.pop('submenus'))
        menu['dishes_count'] = dishes_conter

        return MenuRead(**menu)

    async def del_menu(self, menu_id: UUID) -> int:
        data = await self.menu_repo.delete_menu_item(menu_id)
        return data
