from ..domain.gateway import BookManager
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence


class WireHelper:
    def __init__(self, persistence: MySQLPersistence):
        self.persistence = persistence

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db)
        return cls(db)

    def book_manager(self) -> BookManager:
        return self.persistence
