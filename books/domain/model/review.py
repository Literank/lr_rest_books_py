from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    id: str
    book_id: int
    author: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
