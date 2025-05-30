import csv
from io import StringIO

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.config import db
from backend.models import Books
from backend.utils import is_admin

books = Blueprint('books', __name__, url_prefix='/books')


def get_language_code(name):
    LANGUAGE_NAMES = {
        "English": "eng",
        "French": "fr",
        "Spanish": "es",
        "German": "ger",
        "Italian": "it",
        "Portuguese": "pt",
        "Russian": "ru",
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Hindi": "hi",
        "Arabic": "ar",
        "Bengali": "bn",
        "Punjabi": "pa",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml",
        "Kannada": "kn",
        "Gujarati": "gu",
        "Urdu": "ur"
    }
    return LANGUAGE_NAMES.get(name.title(), None)

# Get all books
@books.route('/', methods=['GET'])
@jwt_required()
def get_books():
    query = Books.query

    # Grab query parameters
    author = request.args.get('author')
    subject = request.args.get('subject')
    language = request.args.get('language')
    published_year = request.args.get('published_year', type=int)
    publisher = request.args.get('publisher')
    title = request.args.get('title')

    # Dynamically build filters
    if author:
        query = query.filter(Books.author.like(f"%{author}%"))
    if language:
        language_code = get_language_code(language)
        if language_code is not None:
            query = query.filter(Books.language.like(f"%{language_code}%"))
    if subject:
        query = query.filter(Books.genre.like(f"%{subject}%"))

    if published_year:
        query = query.filter(Books.published_year == published_year)
    if publisher:
        query = query.filter(Books.publisher.like(f"%{publisher}%"))
    if title:
        query = query.filter(Books.title.like(f"%{title}%"))

    books = query.all()
    return jsonify([book.to_dict() for book in books])


# Get a single book

@books.route('/<string:id_>', methods=['GET'])
@jwt_required()
def get_book(id_):
    book = Books.query.get(id_)
    if not book:
        return jsonify({"message": "Book not found"}), 404

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


@books.route('/bulk-upload', methods=['POST'])
@jwt_required()
def bulk_upload_books():
    try:
        if not is_admin():
            return jsonify({'error': 'Access Denied'}), 403

        if 'file' not in request.files:
            return jsonify({"message": "No file provided"}), 400

        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"message": "Invalid file type"}), 400

        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        inserted = 0
        skipped = 0
        errors = []

        for row in reader:
            subject = row.get("Subject")
            title = row.get("Title")
            author = row.get("Author")
            published_year = row.get("Published Year")
            language = row.get("Language")
            image = row.get("Cover URL")
            publisher = row.get("Publisher")

            if not any([subject, title, author, published_year]):
                skipped += 1
                continue

            books = Books(title=title, author=author, genre=subject, published_year=published_year, image_url=image,
                          language=language)
            db.session.add(books)
            inserted += 1

        db.session.commit()
        return jsonify({"message": f"{inserted} books added successfully", "skipped": skipped}), 200

    except ZeroDivisionError as e:
        print(e)
        return jsonify({'error': 'Failed to upload books'}), 500

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
