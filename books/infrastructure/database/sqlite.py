import sqlite3
from typing import List, Optional

from ...domain.gateway import BookManager
from ...domain.model import Book


class SQLitePersistence(BookManager):

    def __init__(self, file_name: str):
        self._file_name = file_name
        self._create_table()

    def _create_table(self):
        conn, cursor = self._connect()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_at TEXT NOT NULL,
            description TEXT NOT NULL,
            isbn TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
       ''')
        conn.commit()

    def _connect(self):
        # You cannot use a SQLite connection object across multiple threads in Flask.
        # Flask is designed to be multithreaded for handling multiple requests simultaneously.
        conn = sqlite3.connect(self._file_name)
        return conn, conn.cursor()

    def create_book(self, b: Book) -> int:
        conn, cursor = self._connect()
        cursor.execute('''
            INSERT INTO books (title, author, published_at, description, isbn, total_pages) VALUES (?, ?, ?, ?, ?, ?)
        ''', (b.title, b.author, b.published_at, b.description, b.isbn, b.total_pages))
        conn.commit()
        return cursor.lastrowid or 0

    def update_book(self, id: int, b: Book) -> None:
        conn, cursor = self._connect()
        cursor.execute('''
            UPDATE books SET title=?, author=?, published_at=?, description=?, isbn=?, total_pages=?,updated_at=DATETIME('now') WHERE id=?
        ''', (b.title, b.author, b.published_at, b.description, b.isbn, b.total_pages, id))
        conn.commit()

    def delete_book(self, id: int) -> None:
        conn, cursor = self._connect()
        cursor.execute('''
            DELETE FROM books WHERE id=?
        ''', (id,))
        conn.commit()

    def get_book(self, id: int) -> Optional[Book]:
        _, cursor = self._connect()
        cursor.execute('''
            SELECT * FROM books WHERE id=?
        ''', (id,))
        result = cursor.fetchone()
        if result:
            return Book(*result)
        return None

    def get_books(self) -> List[Book]:
        _, cursor = self._connect()
        cursor.execute('''
            SELECT * FROM books
        ''')
        results = cursor.fetchall()
        return [Book(*result) for result in results]
