from flask import Blueprint, request, jsonify
from config import db
from models import Users

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users])

@users.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = Users(username=data['username'], email=data['email'], password=data['password'])
    if not new_user:
        return jsonify({'message': 'No user found'}), 400
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@users.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'No user found'}), 400
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.serialize())

@users.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'No user found'}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

