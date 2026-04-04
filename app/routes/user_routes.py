from flask import Blueprint, request, g
from app.utils.pagination import paginate_query, get_pagination_params
from app.services.user_service import UserService
from app.middleware.auth import login_required
from app.middleware.role import require_role
from app.utils.response import success_response, error_response

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("/", methods=["POST"])
@login_required
@require_role("admin")
def create_user():
    user, error = UserService.create_user(request.json)

    if error:
        return error_response(error, 400)

    return success_response(user.to_dict(), "user created")


@user_bp.route("/", methods=["GET"])
@login_required
@require_role("admin")
def get_users():
    users = UserService.get_all_users()
    page, limit = get_pagination_params()
    data = paginate_query(users, page, limit)

    return success_response(data, "users fetched")


@user_bp.route("/<string:user_id>", methods=["GET"])
@login_required
@require_role("admin")
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    return success_response(user.to_dict(), "user fetched")


@user_bp.route("/<string:user_id>", methods=["PUT"])
@login_required
@require_role("admin")
def update_user(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    updated_user, error = UserService.update_user(user, request.json)

    if error:
        return error_response(error, 400)

    return success_response(updated_user.to_dict(), "user updated")


@user_bp.route("/<string:user_id>/status", methods=["PATCH"])
@login_required
@require_role("admin")
def update_status(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    updated_user, error = UserService.update_status(user, request.json.get("status"))

    if error:
        return error_response(error, 400)

    return success_response(updated_user.to_dict(), "status updated")
