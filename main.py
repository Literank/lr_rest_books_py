from datetime import datetime
import sqlite3

from flask import Flask, request, g, jsonify

app = Flask(__name__)
DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        g._database = db
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_at TEXT NOT NULL,
            description TEXT NOT NULL,
            isbn TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )''')
        cursor.close()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def execute_query(query, values=()):
    cursor = get_db().cursor()
    cursor.execute(query, values)
    result = cursor.fetchall()
    get_db().commit()
    cursor.close()
    return result

# Define a health endpoint handler, use `/health` or `/`
@app.route('/')
def health():
    # Return a simple response indicating the server is healthy
    return {"status": "ok"}

@app.route('/books', methods=['GET'])
def get_books():
    query = "SELECT * FROM books"
    books = execute_query(query)
    return books

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    query = "SELECT * FROM books WHERE id = ?"
    books = execute_query(query, (book_id,))
    if not books:
        return {"error": "Record not found"}, 404
    return jsonify(books[0])

@app.route('/books', methods=['POST'])
def create_book():
    b = request.get_json()
    query = "INSERT INTO books (title, author, published_at, description, isbn, total_pages, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    now = datetime.now()
    values = (b['title'], b['author'], b['published_at'], b['description'], b['isbn'], b['total_pages'], now, now)
    execute_query(query, values)
    return b, 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    b = request.get_json()
    query = "UPDATE books SET title=?, author=?, published_at=?, description=?, isbn=?, total_pages=?, updated_at=? WHERE id=?"
    values = (b['title'], b['author'], b['published_at'], b['description'], b['isbn'], b['total_pages'], datetime.now(), book_id)
    execute_query(query, values)
    return b

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    query = "DELETE FROM books WHERE id=?"
    execute_query(query, (book_id,))
    return '', 204
