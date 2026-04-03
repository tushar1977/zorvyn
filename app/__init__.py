from flask import Flask
from app.config import config_map

from app.extensions import db, jwt, bcrypt, migrate, limiter, register_jwt_callbacks
from app.utils.logger import setup_logging


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config_map[config_name])

    setup_logging(app)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.logger.info("Extensions initialized")

    register_jwt_callbacks(app)

    app.logger.info("JWT callbacks registered")

    from app import models

    from app.routes import register_routes

    register_routes(app)
    return app
