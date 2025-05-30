from flask_jwt_extended import get_jwt_identity

from backend.models import Users


def is_admin():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    return user and user.user_type == 'admin'