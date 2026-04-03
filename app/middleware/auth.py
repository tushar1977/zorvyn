from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.utils.response import error_response


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        verify_jwt_in_request()

        user_id = get_jwt_identity()

        if not user_id:
            return error_response("invalid token payload", 401)

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return error_response("user not found", 401)

        if user.status.value != "active":
            return error_response("account is inactive", 403)

        g.current_user = user

        return f(*args, **kwargs)

    return decorated
