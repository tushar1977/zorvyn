import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from time import time
import traceback
import uuid
from flask import request, g
from app.utils.response import error_response

logger = logging.getLogger(__name__)


def setup_logging(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(log_level)
    app.logger.addHandler(stdout_handler)

    try:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
        app.logger.info("File logging enabled at logs/app.log")
    except OSError:
        app.logger.warning(
            "Read-only filesystem detected — file logging disabled, using stdout only"
        )

    app.logger.setLevel(log_level)
    app.logger.info("Logging is set up.")


def setup_http_logging(app):
    @app.before_request
    def before_request():
        g.start_time = time()
        g.request_id = str(uuid.uuid4())[:8]
        app.logger.info(
            "[REQUEST] %s %s %s %s",
            request.method,
            request.path,
            request.remote_addr,
            g.request_id,
        )

    @app.after_request
    def after_request(response):
        if hasattr(g, "start_time"):
            duration = time() - g.start_time
            app.logger.info(
                "[RESPONSE] %s %s %s - %s (%.3fs)",
                request.method,
                request.path,
                response.status_code,
                getattr(g, "request_id", "unknown"),
                duration,
            )
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        tb = traceback.format_exc()
        app.logger.error(
            "[ERROR] %s %s - 500 ERROR\n%s", request.method, request.path, tb
        )
        return error_response("Internal server error", 500)
