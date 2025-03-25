from models import Books, BookCopies
from random import randint
from config import db, app

with app.app_context():
    books = Books.query.all()
    copies = []
    for book in books:
        num_copies = randint(1,5)
        for i in range(num_copies):
            book_copy = BookCopies(book_id=book.isbn, copy_number=i+1)
            copies.append(book_copy)
            print(book.isbn, book_copy.copy_number)

    db.session.bulk_save_objects(copies)
    db.session.commit()


