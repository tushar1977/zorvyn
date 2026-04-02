import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s"
    )
    file_handler.setFormatter(formatter)

    file_handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)

    app.logger.info("Logging is set up.")
