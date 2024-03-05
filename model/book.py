from dataclasses import dataclass
from datetime import datetime

@dataclass
class Book:
    id: int
    title: str
    author: str
    published_at: str
    description: str
    isbn: str
    total_pages: int
    created_at: datetime
    updated_at: datetime