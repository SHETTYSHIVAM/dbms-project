from flask import Blueprint, request, jsonify
from models import TokenBlocklist, Users
from config import db
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if Users.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already registered"}), 400

    user = Users(
        email=data.get("email"),
        name=data.get("username"),
        user_type=data.get("user_type"),
    )
    user.set_password(data.get("password"))

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=True)
    return jsonify({"access_token": access_token}), 200


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]

    if TokenBlocklist.query.filter_by(jti=jti).first():
        return jsonify({"message": "Already logged out"}), 400

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    return jsonify({"message": "Successfully logged out"}), 200
