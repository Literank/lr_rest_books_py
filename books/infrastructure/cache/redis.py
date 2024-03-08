from typing import Any, Optional

from redis import Redis

from .helper import CacheHelper
from ..config import CacheConfig

DEFAULT_TTL = 3600


class RedisCache(CacheHelper):
    def __init__(self, c: CacheConfig):
        self.client = Redis(
            host=c.host,
            port=c.port,
            password=c.password,
            db=c.db,
        )

    def save(self, key: str, value: str) -> None:
        self.client.set(key, value, ex=DEFAULT_TTL)

    def load(self, key: str) -> Optional[str]:
        value: Any = self.client.get(key)
        if value is None:
            return None
        return value.decode("utf-8")
