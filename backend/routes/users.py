from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models import Users
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    return jsonify([user.to_dict() for user in all_users])


@users.route('/', methods=['POST'])
def add_user():
    data = request.get_json()

    # Validate required fields
    if not all(key in data for key in ['username', 'email', 'password', 'user_type']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Hash password before storing
    hashed_password = generate_password_hash(data['password'])

    new_user = Users(name=data['username'], email=data['email'], user_type=data['user_type'], password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201  # 201 Created


@users.route('/<string:id_>', methods=['PUT'])
def update_user(id_):
    user = Users.query.get_or_404(id_, description='User not found')
    data = request.get_json()
    if 'email' in data and data['email'] != user.email:
        existing_user = Users.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already in use'}), 400
        user.email = data['email']

    # Securely update password if provided
    if 'password' in data:
        setattr(user, 'password', generate_password_hash(data['password']))
    for field in ['username', 'email', 'user_type']:
        if  field in data:
            setattr(user, field, data[field])


    db.session.commit()
    return jsonify(user.to_dict())


@users.route('/<string:id_>', methods=['DELETE'])
def delete_user(id_):
    user = Users.query.get(id_)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
