from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(user_id, action, table_name, record_id=None):
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()


def get_recent_activity(limit=10):
    return AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()
