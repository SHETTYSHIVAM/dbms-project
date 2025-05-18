from datetime import date, datetime, timedelta
from uuid import uuid4

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.config import db
from backend.models import Reservations, Users, BookCopies, BorrowTransactions, Books
from backend.utils import is_admin

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')

@reservations.route('/<string:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    reservation = Reservations.query.get(reservation_id)
    user_id = get_jwt_identity()
    if not reservation or reservation.user_id != user_id:
        return jsonify({'message': 'Reservation not found'}), 404
    book = Books.query.get(reservation.book_id)
    return jsonify({
        'reservation': reservation.to_dict(),
        'book': book.to_dict() if book else None
    })


@reservations.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    user_id = get_jwt_identity()
    book_id = data.get('book_id')

    book = Books.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Check if reservation already exists
    existing_reservation = Reservations.query.filter_by(
        user_id=user_id,
        book_id=book_id
    ).first()

    if existing_reservation and existing_reservation.status != "cancelled":
        return jsonify({
            'message': 'You have already reserved this book.',
            'reservation': existing_reservation.to_dict()
        }), 200

    reservation = Reservations(
        id=str(uuid4()),
        user_id=user_id,
        book_id=book_id,
        reservation_date=date.today(),
        status='pending'
    )
    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        'message': 'Reservation created successfully',
        'reservation': reservation.to_dict(),
        'book': book.to_dict()
    }), 201

@reservations.route('/', methods=['GET'])
@jwt_required()
def get_all_reservations():
    if not is_admin():
        return jsonify({'message': 'You are not authorized to access this endpoint'}), 401

    status_filter = request.args.get('status')  # e.g., /reservations?status=pending

    query = Reservations.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    reservations_list = query.all()
    result = []
    for res in reservations_list:
        book = Books.query.get(res.book_id)
        user = Users.query.get(res.user_id)
        result.append({
            'reservation': res.to_dict(),
            'book': book.to_dict() if book else None,
            'user': user.to_dict() if user else None
        })
    return jsonify(result)


@reservations.route('/<string:reservation_id>', methods=['PUT'])
@jwt_required()
def update_reservation(reservation_id):
    reservation = Reservations.query.get(reservation_id)
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404

    data = request.get_json()
    if 'status' in data:
        reservation.status = data['status']
    db.session.commit()

    return jsonify({
        'message': 'Reservation updated successfully',
        'reservation': reservation.to_dict()
    })


@reservations.route('/<string:reservation_id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(reservation_id):
    reservation = Reservations.query.get(reservation_id)
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation deleted successfully'})


@reservations.route('/fulfill/<string:reservation_id>', methods=['POST'])
@jwt_required()
def fulfill_reservation(reservation_id):
    if not is_admin():
        return jsonify({'message': 'You are not authorized to access this endpoint'}), 401

    reservation = Reservations.query.get(reservation_id)
    if not reservation or reservation.status != 'pending':
        return jsonify({'message': 'Reservation not found'}), 404

    user = Users.query.get(reservation.user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    copy = BookCopies.query.filter_by(book_id=reservation.book_id, is_borrowed=False).first()
    if not copy:
        return jsonify({'message': 'Book copy not available'}), 404

    borrow_count = BorrowTransactions.query.filter_by(user_id=reservation.user_id, is_returned=False).count()
    borrow_limit = 3 if user.user_type == "student" else 5
    if borrow_count >= borrow_limit:
        return jsonify({'message': 'User has reached borrowing limit'}), 400

    issue_date = datetime.now()
    due_days = 14 if user.user_type == "student" else 30
    due_date = issue_date + timedelta(days=due_days)

    reservation.status = 'completed'

    transaction = BorrowTransactions(
        user_id=user.id,
        copy_id=copy.id,
        issue_date=issue_date,
        due_date=due_date,
        is_returned=False
    )

    copy.is_borrowed = True

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'message': 'Reservation fulfilled successfully',
        'transaction': transaction.to_dict(),
        'due_date': due_date.strftime('%Y-%m-%d')
    }), 201
