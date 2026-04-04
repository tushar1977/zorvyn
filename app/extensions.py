from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


def register_jwt_callbacks(app):

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return {"success": False, "message": "Missing or invalid token"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return {"success": False, "message": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"success": False, "message": "Token has expired"}, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {"success": False, "message": "Token has been revoked"}, 401
