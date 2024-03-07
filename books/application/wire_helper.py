from books.domain.gateway import BookManager, ReviewManager
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence, MongoPersistence


class WireHelper:
    def __init__(self, sqlPersistence: MySQLPersistence, noSQLPersistence: MongoPersistence):
        self.sqlPersistence = sqlPersistence
        self.noSQLPersistence = noSQLPersistence

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db)
        mdb = MongoPersistence(c.db.mongo_uri, c.db.mongo_db_name)
        return cls(db, mdb)

    def book_manager(self) -> BookManager:
        return self.sqlPersistence

    def review_manager(self) -> ReviewManager:
        return self.noSQLPersistence
