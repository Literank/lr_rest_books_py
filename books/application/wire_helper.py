from ..domain.gateway import BookManager
from ..infrastructure.config import Config
from ..infrastructure.database import SQLitePersistence


class WireHelper:
    def __init__(self, persistence: SQLitePersistence):
        self.persistence = persistence

    @classmethod
    def new(cls, c: Config):
        db = SQLitePersistence(c.db.file_name)
        return cls(db)

    def book_manager(self) -> BookManager:
        return self.persistence
