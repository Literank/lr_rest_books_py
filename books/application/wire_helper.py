from books.domain.gateway import BookManager, ReviewManager, UserManager
from books.infrastructure.cache import RedisCache, CacheHelper
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence, MongoPersistence


class WireHelper:
    def __init__(self, sqlPersistence: MySQLPersistence, noSQLPersistence: MongoPersistence, kvStore: RedisCache):
        self.sqlPersistence = sqlPersistence
        self.noSQLPersistence = noSQLPersistence
        self.kvStore = kvStore

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db, c.app.page_size)
        mdb = MongoPersistence(c.db.mongo_uri, c.db.mongo_db_name)
        kv = RedisCache(c.cache)
        return cls(db, mdb, kv)

    def book_manager(self) -> BookManager:
        return self.sqlPersistence

    def review_manager(self) -> ReviewManager:
        return self.noSQLPersistence

    def cache_helper(self) -> CacheHelper:
        return self.kvStore

    def user_manager(self) -> UserManager:
        return self.sqlPersistence
