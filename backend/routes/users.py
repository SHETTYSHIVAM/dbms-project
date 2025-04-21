from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db, bcrypt
from models import Users
from utils  import is_admin

users = Blueprint('users', __name__, url_prefix='/users')

# Get all users (Admin only)
@users.route('/', methods=['GET'])
@jwt_required()
def get_users():
    if not is_admin():
        return jsonify({'message': 'Access denied'}), 403
    all_users = Users.query.all()
    return jsonify([user.to_dict() for user in all_users])


# Add a new user (Admin only)
@users.route('/', methods=['POST'])
@jwt_required()
def add_user():
    if not is_admin():
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    if not all(key in data for key in ['username', 'email', 'password', 'user_type']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Use bcrypt to hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = Users(name=data['username'], email=data['email'], user_type=data['user_type'],
                     password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# Update user (Users can update their own details, Admins can update any user)
@users.route('/<string:id_>', methods=['PUT'])
@jwt_required()
def update_user(id_):
    current_user_id = get_jwt_identity()
    user = Users.query.get_or_404(id_, description='User not found')

    # Users can only update their own details unless they are admin
    if str(user.id) != str(current_user_id) and not is_admin():
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()

    if 'email' in data and data['email'] != user.email:
        existing_user = Users.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already in use'}), 400
        user.email = data['email']

    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    for field in ['username', 'user_type']:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()
    return jsonify(user.to_dict())


# Delete user (Admin only)
@users.route('/', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    if not is_admin() or not user_id:
        return jsonify({'message': 'Access denied'}), 403

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
