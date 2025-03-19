from config import db
from uuid import uuid4

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_year = db.Column(db.Integer)
    genre = db.Column(db.String(255))

class BookCopies(db.Model):
    __tablename__ = 'bookcopies'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    book_id = db.Column(db.String(36), db.ForeignKey('books.id'), nullable=False)
    copy_number = db.Column(db.Integer, nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.Enum("student", "faculty"), nullable=False)

class BorrowTransactions(db.Model):
    __tablename__ = 'borrowtransactions'

    id = db.Column(db.String(36), primary_key=True, index=True, default=lambda: str(uuid4()))
    copy_id = db.Column(db.String(36), db.ForeignKey('bookcopies.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    is_returned = db.Column(db.Boolean, default=False)
    fine = db.Column(db.Float, default=0.0)

class Reservations(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(36), db.ForeignKey('books.id'), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending')

class BookRenewals(db.Model):
    __tablename__ = 'bookrenewals'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey('borrowtransactions.id'), nullable=False)
    new_due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')

class Fines(db.Model):
    __tablename__ = 'fines'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('unpaid', 'paid'), default='unpaid')
