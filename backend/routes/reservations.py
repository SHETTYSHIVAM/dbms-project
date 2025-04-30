from datetime import date, datetime, timedelta
from uuid import uuid4

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.config import db
from backend.models import Reservations, Users, BookCopies, BorrowTransactions
from backend.utils import is_admin

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/<string:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    reservation = Reservations.query.get(reservation_id)
    user_id = get_jwt_identity()
    if not reservation or not user_id == reservation.user_id:
        return jsonify({'message': 'Reservation not found'}), 404

    return jsonify(reservation.to_dict())


@reservations.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    user_id = get_jwt_identity()
    reservation = Reservations(
        id=str(uuid4()),
        user_id=user_id,
        book_id=data.get('book_id'),
        reservation_date=date.today(),
        status='pending'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation created successfully', 'reservation': reservation.to_dict()}), 201


@reservations.route('/', methods=['GET'])
@jwt_required()
def get_all_reservations():
    if not is_admin():
        return jsonify({'message': 'You are not authorized to access this endpoint'}), 401
    reservations = Reservations.query.all()
    return jsonify([r.to_dict() for r in reservations])


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
    return jsonify({'message': 'Reservation updated successfully', 'reservation': reservation.to_dict()})


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

    borrow_count = BorrowTransactions.query.filter_by(user_id=reservation.user_id).count()
    borrow_limit = 3 if user.user_type == "student" else 5
    if borrow_count > borrow_limit:
        return jsonify({'message': 'User has reached borrowing limit'}), 400

    due_days = 14 if user.user_type == "student" else 30
    due_date = datetime.now() + timedelta(days=due_days)

    reservation.status = 'completed'

    transaction = BorrowTransactions(
        user_id=user.user_id,
        copy_id=copy.id,
        issue_date=due_date,
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
