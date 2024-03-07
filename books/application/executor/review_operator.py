from datetime import datetime
from typing import List, Optional

from ...domain.model import Review
from ...domain.gateway import ReviewManager


class ReviewOperator():

    def __init__(self, review_manager: ReviewManager):
        self.review_manager = review_manager

    def create_review(self, r: Review) -> Review:
        now = datetime.now()
        r.created_at = now
        r.updated_at = now
        id = self.review_manager.create_review(r)
        r.id = id
        return r

    def get_review(self, id: str) -> Optional[Review]:
        return self.review_manager.get_review(id)

    def get_reviews_of_book(self, review_id: int) -> List[Review]:
        return self.review_manager.get_reviews_of_book(review_id)

    def update_review(self, id: str, r: Review) -> Review:
        r.updated_at = datetime.now()
        self.review_manager.update_review(id, r)
        return r

    def delete_review(self, id: str) -> None:
        return self.review_manager.delete_review(id)
