from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.menu import MenuRepository
from fastfood.repository.redis import RedisRepository, get_key
from fastfood.schemas import MenuBase, MenuRead


class MenuService:
    def __init__(
        self,
        menu_repo: MenuRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:
        self.menu_repo = menu_repo
        self.cache = RedisRepository(redis_client)
        self.key = get_key
        self.bg_tasks = background_tasks

    async def read_menus(self) -> list[MenuRead]:
        cached_menus = await self.cache.get(self.key('menus'))
        if cached_menus is not None:
            return cached_menus

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

        await self.cache.set(self.key('menus'), menus, self.bg_tasks)
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
        await self.cache.set(
            key=get_key('menu', menu_id=str(menu.get('id'))),
            value=menu,
            bg_task=self.bg_tasks,
        )
        menu = MenuRead(**menu)
        await self.cache.set(
            self.key('menu', menu_id=str(menu.id)), menu, self.bg_tasks
        )
        await self.cache.invalidate(key=str(menu.id), bg_task=self.bg_tasks)
        return menu

    async def read_menu(self, menu_id: UUID) -> MenuRead | None:
        cached_menu = await self.cache.get(self.key('menu', menu_id=str(menu_id)))
        if cached_menu is not None:
            return cached_menu

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
        menu = MenuRead(**menu)
        await self.cache.set(
            self.key('menu', menu_id=str(menu.id)), menu, self.bg_tasks
        )
        return menu

    async def update_menu(self, menu_id: UUID, menu_data) -> MenuRead:
        data = await self.menu_repo.update_menu_item(menu_id, menu_data)
        menu = data.__dict__
        menu = {k: v for k, v in menu.items() if not k.startswith('_')}
        dishes_conter = 0

        for sub in data.submenus:
            dishes_conter += len(sub.dishes)
        menu['submenus_count'] = len(menu.pop('submenus'))
        menu['dishes_count'] = dishes_conter
        menu = MenuRead(**menu)
        await self.cache.set(
            self.key('menu', menu_id=str(menu.id)), menu, self.bg_tasks
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)
        return menu

    async def del_menu(self, menu_id: UUID) -> None:
        await self.menu_repo.delete_menu_item(menu_id)
        await self.cache.delete(key=str(menu_id), bg_task=self.bg_tasks)
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)
