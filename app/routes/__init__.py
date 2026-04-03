from app.routes.role_routes import role_bp
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.health_routes import health_bp
from app.routes.record_routes import record_bp
from app.routes.category_routes import category_bp


def register_routes(app):
    app.register_blueprint(role_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(record_bp)
    app.register_blueprint(category_bp)
