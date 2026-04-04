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
    """
    Create a new user
    ---
    tags:
      - users
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - email
              - password
            properties:
              name:
                type: string
                example: Jane Doe
              email:
                type: string
                example: jane@example.com
              password:
                type: string
                example: password123
              role_id:
                type: string
                example: 550e8400-e29b-41d4-a716-446655440000
    responses:
      200:
        description: User created successfully
      400:
        description: Validation error
      401:
        description: Authentication required
      403:
        description: Admin access required
    """
    user, error = UserService.create_user(request.json)

    if error:
        return error_response(error, 400)

    return success_response(user.to_dict(), "user created")


@user_bp.route("/", methods=["GET"])
@login_required
@require_role("admin")
def get_users():
    """
    Get all users with pagination
    ---
    tags:
      - users
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Users fetched successfully
      401:
        description: Authentication required
      403:
        description: Admin access required
    """
    users = UserService.get_all_users()
    page, limit = get_pagination_params()
    data = paginate_query(users, page, limit)

    return success_response(data, "users fetched")


@user_bp.route("/<string:user_id>", methods=["GET"])
@login_required
@require_role("admin")
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        example: 550e8400-e29b-41d4-a716-446655440000
    responses:
      200:
        description: User fetched successfully
      404:
        description: User not found
    """
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    return success_response(user.to_dict(), "user fetched")


@user_bp.route("/<string:user_id>", methods=["PUT"])
@login_required
@require_role("admin")
def update_user(user_id):
    """
    Update user
    ---
    tags:
      - users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: Updated Name
              email:
                type: string
                example: updated@example.com
    responses:
      200:
        description: User updated successfully
      400:
        description: Validation error
      404:
        description: User not found
    """
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
    """
    Update user status
    ---
    tags:
      - users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - status
            properties:
              status:
                type: string
                enum: [active, inactive]
                example: active
    responses:
      200:
        description: Status updated successfully
      400:
        description: Invalid status
      404:
        description: User not found
    """
    user = UserService.get_user_by_id(user_id)

    if not user:
        return error_response("user not found", 404)

    updated_user, error = UserService.update_status(user, request.json.get("status"))

    if error:
        return error_response(error, 400)

    return success_response(updated_user.to_dict(), "status updated")
