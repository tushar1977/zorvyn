from flask import Blueprint, request
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.middleware.auth import login_required
from app.middleware.role import require_role
from app.utils.response import success_response, error_response

role_bp = Blueprint("roles", __name__, url_prefix="/roles")


@role_bp.route("/", methods=["GET"])
@login_required
@require_role("admin")
def get_roles():
    roles = RoleService.get_all_roles()

    return success_response([r.to_dict() for r in roles], "roles fetched")


@role_bp.route("/assign/<int:user_id>", methods=["PATCH"])
@login_required
@require_role("admin")
def assign_role(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    updated_user, error = RoleService.assign_role(user, request.json.get("role"))

    if error:
        return error_response(error, 400)

    return success_response(updated_user.to_dict(), "role updated")


@role_bp.route("/create", methods=["POST"])
@login_required
@require_role("admin")
def create_roles():
    result, error = RoleService.seed_roles()

    if error:
        return error_response(error, 500)

    return success_response(result, "roles processed")
