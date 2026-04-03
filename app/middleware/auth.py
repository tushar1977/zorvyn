from functools import wraps
from flask import g, request
from app.models.user import User
from app.utils.response import error_response


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user_id = request.headers.get("x-user-id")
        if not user_id:
            return error_response("missing  user id", 401)
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return error_response("user not found", 401)

        if user.status != "active":
            return error_response("account is inactive", 403)

        g.current_user = user

        return f(*args, **kwargs)

    return decorated
