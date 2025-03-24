from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from config import db
import datetime

class Books(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)  # FIXED
    published_year = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,  # FIXED
            'published_year': self.published_year,
            'publisher': self.publisher,
            'image_url': self.image_url,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            isbn=data.get('isbn'),
            title=data.get('title'),
            author=data.get('author'),
            genre=data.get('genre'),  # FIXED
            published_year=data.get('published_year'),
            publisher=data.get('publisher'),
            image_url=data.get('image_url'),  # FIXED
        )


class BookCopies(db.Model):
    __tablename__ = 'bookcopies'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    book_id = db.Column(db.String(50), db.ForeignKey('books.isbn'), nullable=False)  # FIXED
    copy_number = db.Column(db.Integer, nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'copy_number': self.copy_number,
            'is_borrowed': self.is_borrowed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            book_id=data.get('book_id'),
            copy_number=data.get('copy_number'),
            is_borrowed=data.get('is_borrowed', False)
        )



class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.Enum('student', 'faculty', 'admin'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "user_type": self.user_type
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            user_type=data.get("user_type")
        )
        if "password" in data:
            user.set_password(data["password"])  # Hash password correctly
        return user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id


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

    def to_dict(self):
        return {
            'id': self.id,
            'copy_id': self.copy_id,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id,
            'is_returned': self.is_returned,
            'fine': self.fine
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            copy_id=data.get('copy_id'),
            issue_date=date.fromisoformat(data['issue_date']) if data.get('issue_date') else None,
            return_date=date.fromisoformat(data['return_date']) if data.get('return_date') else None,
            due_date=date.fromisoformat(data['due_date']) if data.get('due_date') else None,
            user_id=data.get('user_id'),
            is_returned=data.get('is_returned', False),
            fine=data.get('fine', 0.0)
        )


class Reservations(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(50), db.ForeignKey('books.isbn'), nullable=False)  # FIXED
    reservation_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled', name="reservation_status_enum"), default='pending')  # FIXED

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'reservation_date': self.reservation_date.isoformat(),
            'status': self.status
        }


class BookRenewals(db.Model):
    __tablename__ = 'bookrenewals'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey('borrowtransactions.id'), nullable=False)
    new_due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name="renewal_status_enum"), default='pending')  # FIXED

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'new_due_date': self.new_due_date.isoformat() if self.new_due_date else None,
            'status': self.status
        }


class Fines(db.Model):
    __tablename__ = 'fines'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('unpaid', 'paid'), default='unpaid')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get('user_id'),
            amount=data.get('amount'),
            status=data.get('status', 'unpaid')
        )


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)  # JWT ID
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())