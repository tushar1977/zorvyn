from datetime import datetime

from app.models.financial_record import RecordType
from app.models.category import CategoryType

VALID_TYPES = {"income", "expense"}
VALID_ROLES = {"admin", "analyst", "viewer"}
VALID_STATUSES = {"active", "inactive"}


def validate_amount(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError("amount must be a valid number")
    if value <= 0:
        raise ValueError("amount must be greater than zero")
    return value


def validate_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("date must be in YYYY-MM-DD format")


def validate_role(value):
    if value not in VALID_ROLES:
        raise ValueError(f"role must be one of {VALID_ROLES}")


def validate_status(value):
    if value not in VALID_STATUSES:
        raise ValueError(f"status must be one of {VALID_STATUSES}")


def validate_email(value):
    if not value or "@" not in value:
        raise ValueError("invalid email address")


def validate_required_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")


def validate_category_type(value):

    try:
        return CategoryType(value.lower())
    except Exception:
        allowed = [e.value for e in CategoryType]
        raise ValueError(f"type must be one of {allowed}")


def validate_record_type(value):

    try:
        return RecordType(value.lower())
    except Exception:
        allowed = [e.value for e in RecordType]
        raise ValueError(f"type must be one of {allowed}")
