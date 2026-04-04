from flask import Blueprint, request, g
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response
from app.middleware.auth import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: tushar2@example.com
            password:
              type: string
              example: StrongPass@123
    responses:
      200:
        description: User registered successfully
      400:
        description: Registration failed
    """
    result, error = AuthService.register(request.json)
    if error:
        return error_response(error, 400)
    return success_response(result, "user registered")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: tushar2@example.com
            password:
              type: string
              example: StrongPass@123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.json
    result, error = AuthService.login(data.get("email"), data.get("password"))
    if error:
        return error_response(error, 401)
    return success_response(result, "login successful")


@auth_bp.route("/refresh", methods=["POST"])
@login_required
def refresh():
    """
    Refresh access token
    ---
    tags:
      - auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Session refreshed successfully
    """
    return success_response(AuthService.refresh(g.current_user), "session refreshed")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Logout user
    ---
    tags:
      - auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Logged out successfully
    """
    AuthService.logout(g.current_user)
    return success_response({}, "logged out")
