import os
from app import create_app

env = os.environ.get("FLASK_ENV")

app = create_app(env)


if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 3000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    if env == "prod":
        print("Running in production mode")
        app.run(
            host=host,
            port=port,
            debug=False,
        )
    else:
        print("Running in Dev mode")

        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=debug,
        )
