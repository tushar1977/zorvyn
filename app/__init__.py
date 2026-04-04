from flasgger import Swagger
from flask import Flask
from app.config import config_map

from app.extensions import (
    db,
    jwt,
    bcrypt,
    migrate,
    limiter,
    register_jwt_callbacks,
)
from app.utils.logger import setup_http_logging, setup_logging
from app.utils.response import error_response


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config_map[config_name])
    swagger_config = {
        "title": "Zorvyn Financial API",
        "version": "2.0.0",
        "description": "Financial Management System API",
        "contact": {"name": "API Support", "email": "support@zorvyn.com"},
        "tags": [
            {"name": "auth", "description": "Authentication operations"},
            {"name": "users", "description": "User management"},
            {"name": "records", "description": "Financial records"},
            {"name": "categories", "description": "Category management"},
            {"name": "dashboard", "description": "Dashboard analytics"},
            {"name": "roles", "description": "Role management"},
            {"name": "health", "description": "Health check endpoints"},
        ],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Paste your token as: Bearer {your_token_here}",
            }
        },
        "security": [{"BearerAuth": []}],
    }

    flasgger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "swagger_ui_config": {
            "persistAuthorization": True,
        },
    }

    s = Swagger(app, template=swagger_config, config=flasgger_config)

    setup_logging(app)
    setup_http_logging(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return error_response(f"Rate limit exceeded. {e.description}", 429)

    app.logger.info("Extensions initialized")

    register_jwt_callbacks(app)

    app.logger.info("JWT callbacks registered")

    from app import models

    from app.routes import register_routes

    register_routes(app)
    return app
