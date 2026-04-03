from flask import Blueprint
from sqlalchemy.sql.expression import text
from app.extensions import db

health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.route("/ping", methods=["GET"])
def ping():
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    return {"success": True, "data": {"server": "running", "database": db_status}}, 200
