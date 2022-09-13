import os
from . import create_app
from .models import Book
from flask import jsonify
from flask import request

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/book/list", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])

@app.route("/book/<int:isbn>", methods=["GET"])
def get_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    return jsonify(book.to_json())


@app.route('/book/<int:isbn>', methods=['PUT'])
def update_book(isbn):
    if not request.json:
        abort(400)
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.price = request.json.get('price', book.price)
    db.session.commit()
    return jsonify(book.to_json())