from abc import ABC, abstractmethod
from typing import List, Optional

from ..model import Book


class BookManager(ABC):
    @abstractmethod
    def create_book(self, b: Book) -> int:
        pass

    @abstractmethod
    def update_book(self, id: int, b: Book) -> None:
        pass

    @abstractmethod
    def delete_book(self, id: int) -> None:
        pass

    @abstractmethod
    def get_book(self, id: int) -> Optional[Book]:
        pass

    @abstractmethod
    def get_books(self) -> List[Book]:
        pass
