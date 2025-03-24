from flask import Blueprint, request, jsonify
from uuid import uuid4
from config import db
from models import Books

books = Blueprint('books', __name__, url_prefix='/books')


# Get all books
@books.route('/', methods=['GET'])
def get_books():
    all_books = Books.query.all()
    return jsonify([book.to_dict() for book in all_books])


@books.route('/<string:id_>', methods=['GET'])
def get_book(id_):
    book = Books.query.get_or_404(id_, description="Book not found")
    return jsonify(book.to_dict())


# Add a new book
@books.route('/', methods=['POST'])
def add_book():
    data = request.get_json()

    required_fields = ['isbn', 'title', 'author', 'genre']
    if not data or any(field not in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Books(
        isbn= data['isbn'],
        title=data['title'],
        author=data['author'],
        published_year=data.get('published_year'),
        genre=data['genre'],
        image_url=data.get('image_path')
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201


# Update a book
@books.route('/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    book = Books.query.get_or_404(isbn, description='Book not found')

    data = request.get_json()
    for field in ['title', 'author', 'published_year', 'genre', 'image_path']:
        if field in data:
            setattr(book, field, data[field])

    db.session.commit()
    return jsonify(book.to_dict())


# Delete a book
@books.route('/<string:id_>', methods=['DELETE'])
def delete_book(id_):
    book = Books.query.get_or_404(id_, description='Book not found')

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200
