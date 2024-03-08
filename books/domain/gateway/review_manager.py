from abc import ABC, abstractmethod
from typing import List, Optional

from ..model import Review


class ReviewManager(ABC):
    @abstractmethod
    def create_review(self, r: Review) -> str:
        pass

    @abstractmethod
    def update_review(self, id: str, r: Review) -> None:
        pass

    @abstractmethod
    def delete_review(self, id: str) -> None:
        pass

    @abstractmethod
    def get_review(self, id: str) -> Optional[Review]:
        pass

    @abstractmethod
    def get_reviews_of_book(self, book_id: int, keyword: str) -> List[Review]:
        pass
