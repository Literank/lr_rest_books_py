import mysql.connector
from typing import Any, List, Optional

from books.infrastructure.config import DBConfig

from ...domain.gateway import BookManager
from ...domain.model import Book


class MySQLPersistence(BookManager):
    def __init__(self, c: DBConfig):
        self.conn = mysql.connector.connect(
            host=c.host,
            port=c.port,
            user=c.user,
            password=c.password,
            database=c.database,
            autocommit=True
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            published_at DATE NOT NULL,
            description TEXT NOT NULL,
            isbn VARCHAR(15) NOT NULL,
            total_pages INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        ''')

    def create_book(self, b: Book) -> int:
        self.cursor.execute('''
            INSERT INTO books (title, author, published_at, description, isbn, total_pages) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (b.title, b.author, b.published_at, b.description, b.isbn, b.total_pages))
        return self.cursor.lastrowid or 0

    def update_book(self, id: int, b: Book) -> None:
        self.cursor.execute('''
            UPDATE books SET title=%s, author=%s, published_at=%s, description=%s, isbn=%s, total_pages=%s WHERE id=%s
        ''', (b.title, b.author, b.published_at, b.description, b.isbn, b.total_pages, id))

    def delete_book(self, id: int) -> None:
        self.cursor.execute('''
            DELETE FROM books WHERE id=%s
        ''', (id,))

    def get_book(self, id: int) -> Optional[Book]:
        self.cursor.execute('''
            SELECT * FROM books WHERE id=%s
        ''', (id,))
        result: Any = self.cursor.fetchone()
        if result is None:
            return None
        return Book(**result)

    def get_books(self) -> List[Book]:
        self.cursor.execute('''
            SELECT * FROM books
        ''')
        results: List[Any] = self.cursor.fetchall()
        return [Book(**result) for result in results]
