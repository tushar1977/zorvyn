from functools import wraps
from flask import g
from app.utils.response import error_response


def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = g.get("current_user")
            if not user:
                return error_response("unauthorized", 401)
            if user.role.name not in allowed_roles:
                return error_response(
                    f"access denied: requires one of {list(allowed_roles)}", 403
                )
            return f(*args, **kwargs)

        return decorated

    return decorator
