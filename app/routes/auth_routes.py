from flask import Blueprint, request, g
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response
from app.middleware.auth import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    result, error = AuthService.register(request.json)

    if error:
        return error_response(error, 400)

    return success_response(result, "user registered")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    result, error = AuthService.login(data.get("email"), data.get("password"))

    if error:
        return error_response(error, 401)

    return success_response(result, "login successful")


# Currently dummy routes
@auth_bp.route("/refresh", methods=["POST"])
@login_required
def refresh():
    return success_response(AuthService.refresh(g.current_user), "session refreshed")


# Currently dummy routes
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    AuthService.logout(g.current_user)
    return success_response({}, "logged out")
