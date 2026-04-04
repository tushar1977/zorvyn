from flask import Blueprint
from sqlalchemy.sql.expression import text
from app.extensions import db

health_bp = Blueprint("health", __name__, url_prefix="/")


@health_bp.route("/ping", methods=["GET"])
def ping():
    """
    Health check endpoint
    ---
    tags:
      - health
    responses:
      200:
        description: Server is running
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                data:
                  type: object
                  properties:
                    server:
                      type: string
                    database:
                      type: string
    """
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    return {"success": True, "data": {"server": "running", "database": db_status}}, 200
