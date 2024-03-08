import logging
from flask import Flask, request, jsonify

from ..application.executor import BookOperator, ReviewOperator
from ..application import WireHelper
from ..domain.model import Book, Review
from .util import dataclass_from_dict


class RestHandler:
    def __init__(self, logger: logging.Logger, book_operator: BookOperator, review_operator: ReviewOperator):
        self._logger = logger
        self.book_operator = book_operator
        self.review_operator = review_operator

    def get_books(self):
        try:
            offset = request.args.get("o", type=int, default=0)
            query = request.args.get("q", type=str, default="")
            books = self.book_operator.get_books(offset, query)
            return jsonify(books), 200
        except Exception as e:
            self._logger.error(f"Failed to get books: {e}")
            return jsonify({"error": "Failed to get books"}), 404

    def get_book(self, id):
        try:
            book = self.book_operator.get_book(id)
            if not book:
                return jsonify({"error": f"The book with id {id} does not exist"}), 404
            return jsonify(book), 200
        except Exception as e:
            self._logger.error(f"Failed to get the book with {id}: {e}")
            return jsonify({"error": "Failed to get the book"}), 404

    def create_book(self):
        try:
            b = dataclass_from_dict(Book, request.json)
            book = self.book_operator.create_book(b)
            return jsonify(book), 201
        except Exception as e:
            self._logger.error(f"Failed to create: {e}")
            return jsonify({"error": "Failed to create"}), 400

    def update_book(self, id):
        try:
            b = dataclass_from_dict(Book, request.json)
            book = self.book_operator.update_book(id, b)
            return jsonify(book), 200
        except Exception as e:
            self._logger.error(f"Failed to update: {e}")
            return jsonify({"error": "Failed to update"}), 404

    def delete_book(self, id):
        try:
            self.book_operator.delete_book(id)
            return "", 204
        except Exception as e:
            self._logger.error(f"Failed to delete: {e}")
            return jsonify({"error": "Failed to delete"}), 404

    def get_reviews_of_book(self, book_id: int):
        try:
            query = request.args.get("q", type=str, default="")
            reviews = self.review_operator.get_reviews_of_book(book_id, query)
            return jsonify(reviews), 200
        except Exception as e:
            self._logger.error(f"Failed to get reviews of book: {e}")
            return jsonify({"error": "Failed to get reviews of book"}), 404

    def get_review(self, id: str):
        try:
            review = self.review_operator.get_review(id)
            if not review:
                return jsonify({"error": f"The review with id {id} does not exist"}), 404
            return jsonify(review), 200
        except Exception as e:
            self._logger.error(f"Failed to get the review with {id}: {e}")
            return jsonify({"error": "Failed to get the review"}), 404

    def create_review(self):
        try:
            b = dataclass_from_dict(Review, request.json)
            review = self.review_operator.create_review(b)
            return jsonify(review), 201
        except Exception as e:
            self._logger.error(f"Failed to create: {e}")
            return jsonify({"error": "Failed to create"}), 400

    def update_review(self, id: str):
        try:
            b = dataclass_from_dict(Review, request.json)
            review = self.review_operator.update_review(id, b)
            return jsonify(review), 200
        except Exception as e:
            self._logger.error(f"Failed to update: {e}")
            return jsonify({"error": "Failed to update"}), 404

    def delete_review(self, id: str):
        try:
            self.review_operator.delete_review(id)
            return "", 204
        except Exception as e:
            self._logger.error(f"Failed to delete: {e}")
            return jsonify({"error": "Failed to delete"}), 404


def health():
    return jsonify({"status": "ok"})


def make_router(app: Flask, wire_helper: WireHelper):
    rest_handler = RestHandler(
        app.logger,
        BookOperator(
            wire_helper.book_manager(),
            wire_helper.cache_helper()),
        ReviewOperator(wire_helper.review_manager()))
    app.add_url_rule('/', view_func=health)
    app.add_url_rule('/books', view_func=rest_handler.get_books)
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.get_book)
    app.add_url_rule('/books', view_func=rest_handler.create_book,
                     methods=['POST'])
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.update_book,
                     methods=['PUT'])
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.delete_book,
                     methods=['DELETE'])
    app.add_url_rule('/books/<int:book_id>/reviews',
                     view_func=rest_handler.get_reviews_of_book)
    app.add_url_rule('/reviews/<id>', view_func=rest_handler.get_review)
    app.add_url_rule('/reviews', view_func=rest_handler.create_review,
                     methods=['POST'])
    app.add_url_rule('/reviews/<id>', view_func=rest_handler.update_review,
                     methods=['PUT'])
    app.add_url_rule('/reviews/<id>', view_func=rest_handler.delete_review,
                     methods=['DELETE'])
