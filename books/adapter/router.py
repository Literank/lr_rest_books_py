import logging
from flask import Flask, request, jsonify

from ..application.executor import BookOperator
from ..application import WireHelper
from ..domain.model import Book
from .util import dataclass_from_dict


class RestHandler:
    def __init__(self, logger: logging.Logger, book_operator: BookOperator):
        self._logger = logger
        self.book_operator = book_operator

    def get_books(self):
        try:
            books = self.book_operator.get_books()
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


def health():
    return jsonify({"status": "ok"})


def make_router(app: Flask, wire_helper: WireHelper):
    rest_handler = RestHandler(
        app.logger, BookOperator(wire_helper.book_manager()))
    app.add_url_rule('/', view_func=health)
    app.add_url_rule('/books', view_func=rest_handler.get_books)
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.get_book)
    app.add_url_rule('/books', view_func=rest_handler.create_book,
                     methods=['POST'])
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.update_book,
                     methods=['PUT'])
    app.add_url_rule('/books/<int:id>', view_func=rest_handler.delete_book,
                     methods=['DELETE'])
