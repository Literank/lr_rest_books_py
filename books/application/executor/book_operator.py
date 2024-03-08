from dataclasses import asdict
import json
from typing import Any, Dict, List, Optional

from books.infrastructure.cache.helper import CacheHelper
from ...domain.model import Book
from ...domain.gateway import BookManager

BOOKS_KEY = "lr-books"


class BookOperator():

    def __init__(self, book_manager: BookManager, cache_helper: CacheHelper):
        self.book_manager = book_manager
        self.cache_helper = cache_helper

    def create_book(self, b: Book) -> Book:
        id = self.book_manager.create_book(b)
        b.id = id
        return b

    def get_book(self, id: int) -> Optional[Book]:
        return self.book_manager.get_book(id)

    def get_books(self) -> List[Book]:
        v = self.cache_helper.load(BOOKS_KEY)
        if v:
            return json.loads(v)
        books = self.book_manager.get_books()
        self.cache_helper.save(
            BOOKS_KEY, json.dumps([_convert(b) for b in books]))
        return books

    def update_book(self, id: int, b: Book) -> Book:
        self.book_manager.update_book(id, b)
        return b

    def delete_book(self, id: int) -> None:
        return self.book_manager.delete_book(id)


def _convert(b: Book) -> Dict[str, Any]:
    new_b = asdict(b)
    new_b['created_at'] = b.created_at.isoformat()
    new_b['updated_at'] = b.updated_at.isoformat()
    return new_b
