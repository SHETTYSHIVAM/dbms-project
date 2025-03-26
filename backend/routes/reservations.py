from flask import Blueprint, request, jsonify
from datetime import date
from uuid import uuid4
from models import Reservations
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import is_admin

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/<string:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    reservation = Reservations.query.get(reservation_id)
    user_id = get_jwt_identity()
    if not reservation or not user_id==reservation.user_id:
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
