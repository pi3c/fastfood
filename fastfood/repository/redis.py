from typing import Any

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_redis_pool


class RedisRepository:
    def __init__(
        self,
        redis_pool: redis.Redis = Depends(get_redis_pool),
    ) -> None:
        self.redis_pool = redis_pool
        self.ttl = 1800

    async def get(self, key: str) -> Any | None:

        return None

    async def set(
        self, key: str, value: Any, background_tasks: BackgroundTasks
    ) -> None:
        pass
