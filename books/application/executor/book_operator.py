from typing import List, Optional
from ...domain.model import Book
from ...domain.gateway import BookManager


class BookOperator():

    def __init__(self, book_manager: BookManager):
        self.book_manager = book_manager

    def create_book(self, b: Book) -> Book:
        id = self.book_manager.create_book(b)
        b.id = id
        return b

    def get_book(self, id: int) -> Optional[Book]:
        return self.book_manager.get_book(id)

    def get_books(self) -> List[Book]:
        return self.book_manager.get_books()

    def update_book(self, id: int, b: Book) -> Book:
        self.book_manager.update_book(id, b)
        return b

    def delete_book(self, id: int) -> None:
        return self.book_manager.delete_book(id)
