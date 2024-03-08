from books.domain.gateway import BookManager, ReviewManager, UserManager, PermissionManager
from books.infrastructure.cache import RedisCache, CacheHelper
from books.infrastructure.token import TokenKeeper
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence, MongoPersistence


class WireHelper:
    def __init__(self,
                 sqlPersistence: MySQLPersistence,
                 noSQLPersistence: MongoPersistence,
                 kvStore: RedisCache,
                 tokenKeeper: TokenKeeper):
        self.sqlPersistence = sqlPersistence
        self.noSQLPersistence = noSQLPersistence
        self.kvStore = kvStore
        self.tokenKeeper = tokenKeeper

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db, c.app.page_size)
        mdb = MongoPersistence(c.db.mongo_uri, c.db.mongo_db_name)
        kv = RedisCache(c.cache)
        tk = TokenKeeper(c.app.token_secret, c.app.token_hours)
        return cls(db, mdb, kv, tk)

    def book_manager(self) -> BookManager:
        return self.sqlPersistence

    def perm_manager(self) -> PermissionManager:
        return self.tokenKeeper

    def review_manager(self) -> ReviewManager:
        return self.noSQLPersistence

    def cache_helper(self) -> CacheHelper:
        return self.kvStore

    def user_manager(self) -> UserManager:
        return self.sqlPersistence
