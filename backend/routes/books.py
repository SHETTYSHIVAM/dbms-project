from flask import Blueprint, request, jsonify
from config import db
from models import Books
from flask_jwt_extended import jwt_required

from routes.users import is_admin

books = Blueprint('books', __name__, url_prefix='/books')


# Get all books
@books.route('/', methods=['GET'])
@jwt_required()
def get_books():
    all_books = Books.query.all()
    return jsonify([book.to_dict() for book in all_books])


# Get a single book

@books.route('/<string:id_>', methods=['GET'])
@jwt_required()
def get_book(id_):
    book = Books.query.get_or_404(id_, description="Book not found")
    return jsonify(book.to_dict())


# Add a new book
@books.route('/', methods=['POST'])
@jwt_required()
def add_book():
    if not is_admin():
        return jsonify({'error': 'Access Denied'}), 403
    data = request.get_json()

    required_fields = ['isbn', 'title', 'author', 'genre']
    if not data or any(field not in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Books(
        isbn=data['isbn'],
        title=data['title'],
        author=data['author'],
        published_year=data.get('published_year'),
        genre=data['genre'],
        image_url=data.get('image_url')  # Ensure consistency
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201


# Update a book
@books.route('/<string:id_>', methods=['PUT'])
@jwt_required()
def update_book(id_):
    if not is_admin():
        return jsonify({'error': 'Access Denied'}), 403
    book = Books.query.get_or_404(id_, description='Book not found')

    data = request.get_json()
    for field in ['title', 'author', 'published_year', 'genre', 'image_url']:  # Ensure consistency
        if field in data:
            setattr(book, field, data[field])

    db.session.commit()
    return jsonify(book.to_dict())


# Delete a book
@books.route('/<string:id_>', methods=['DELETE'])
@jwt_required()
def delete_book(id_):
    if not is_admin():
        return jsonify({'error': 'Access Denied'}), 403
    book = Books.query.get_or_404(id_, description='Book not found')
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200
