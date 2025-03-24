from flask import Blueprint, request, jsonify
import jwt
import datetime
from config import db, SECRET_KEY
from models import Users

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = Users.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "user_type": user.user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token, "user_type": user.user_type})

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = Users.query.filter_by(email=data.get("email")).first()
    if user:
        return jsonify({"message": "Email already registered"}), 400

    new_user = Users(
        name=data.get("name"),
        email=data.get("email"),
        user_type=data.get("user_type")
    )
    new_user.set_password(data.get("password"))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})
