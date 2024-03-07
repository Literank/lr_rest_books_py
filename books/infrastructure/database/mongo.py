from bson.objectid import ObjectId
import dataclasses
from pymongo import MongoClient
from typing import Any, Dict, List, Optional

from ...domain.gateway import ReviewManager
from ...domain.model import Review

COLL_REVIEW = "reviews"


class MongoPersistence(ReviewManager):
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.coll = self.db[COLL_REVIEW]

    def create_review(self, r: Review) -> str:
        result = self.coll.insert_one(dataclasses.asdict(r))
        return str(result.inserted_id)

    def update_review(self, id: str, r: Review) -> None:
        new_data = {"title": r.title, "content": r.content,
                    "updated_at": r.updated_at}
        self.coll.update_one({"_id": ObjectId(id)}, {"$set": new_data})

    def delete_review(self, id: str) -> None:
        self.coll.delete_one({"_id": ObjectId(id)})

    def get_review(self, id: str) -> Optional[Review]:
        review_data = self.coll.find_one({"_id": ObjectId(id)})
        if review_data is None:
            return None
        return Review(**_polish(review_data))

    def get_reviews_of_book(self, book_id: int) -> List[Review]:
        reviews_data = self.coll.find({"book_id": book_id})
        return [Review(**_polish(r)) for r in reviews_data]


def _polish(r: Dict[str, Any]):
    r['id'] = str(r['_id'])
    del r['_id']
    return r
