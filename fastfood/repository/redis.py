import pickle
from typing import Any

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_redis_pool


def get_key(level: str, **kwargs) -> str:
    match level:
        case 'menus':
            return 'MENUS'
        case 'menu':
            return f"{kwargs.get('menu_id')}"
        case 'submenus':
            return f"{kwargs.get('menu_id')}:SUBMENUS"
        case 'submenu':
            return f"{kwargs.get('menu_id')}:{kwargs.get('submenu_id')}"
        case 'dishes':
            return f"{kwargs.get('menu_id')}:{kwargs.get('submenu_id')}:DISHES"
        case 'dish':
            return f"{kwargs.get('menu_id')}:{kwargs.get('submenu_id')}:{kwargs.get('dish_id')}"

    return 'abracadabra'


class RedisRepository:
    def __init__(
        self,
        pool: redis.Redis = Depends(get_redis_pool),
    ) -> None:
        self.pool = pool
        self.ttl = 2

    async def get(self, key: str) -> Any | None:
        data = await self.pool.get(key)
        if data is not None:
            return pickle.loads(data)
        return None

    async def set(self, key: str, value: Any, bg_task: BackgroundTasks) -> None:
        data = pickle.dumps(value)
        bg_task.add_task(self._set_cache, key, data)

    async def _set_cache(self, key: str, data: Any) -> None:
        await self.pool.setex(key, self.ttl, data)

    async def delete(self, key: str, bg_task: BackgroundTasks) -> None:
        bg_task.add_task(self._delete_cache, key)

    async def _delete_cache(self, key: str) -> None:
        await self.pool.delete(key)

    async def clear_cache(self, pattern: str, bg_task: BackgroundTasks) -> None:
        keys = [key async for key in self.pool.scan_iter(pattern)]
        if keys:
            bg_task.add_task(self._clear_keys, keys)

    async def _clear_keys(self, keys: list[str]) -> None:
        await self.pool.delete(*keys)

    async def invalidate(self, key: str, bg_task: BackgroundTasks) -> None:
        await self.clear_cache(f'{key}*', bg_task)
        await self.clear_cache(f'{get_key("menus")}*', bg_task)
