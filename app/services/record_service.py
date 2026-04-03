from app.extensions import db
from app.models.financial_record import FinancialRecord
from app.models.category import Category
from app.utils.validator import (
    validate_required_fields,
    validate_amount,
    validate_record_type,
    validate_date,
)


def _check_permission(record, user):
    if record.user_id != user.id:
        raise ValueError("you do not have permission for this action")


def _validate_filters(filters):
    if not filters:
        return {}

    validated = {}

    if filters.get("type"):
        validate_record_type(filters["type"])
        validated["type"] = filters["type"]

    if filters.get("category_id"):
        validated["category_id"] = filters["category_id"]

    if filters.get("start_date"):
        validated["start_date"] = validate_date(filters["start_date"])

    if filters.get("end_date"):
        validated["end_date"] = validate_date(filters["end_date"])

    if filters.get("user_id"):
        validated["user_id"] = filters["user_id"]

    return validated


def get_records(filters=None):
    query = FinancialRecord.query.filter_by(is_deleted=False)

    filters = _validate_filters(filters)

    if filters.get("type"):
        query = query.filter_by(type=filters["type"])

    if filters.get("category_id"):
        query = query.filter_by(category_id=filters["category_id"])

    if filters.get("start_date") and filters.get("end_date"):
        query = query.filter(
            FinancialRecord.record_date >= filters["start_date"],
            FinancialRecord.record_date <= filters["end_date"],
        )

    if filters.get("user_id"):
        query = query.filter_by(user_id=filters["user_id"])

    return query.order_by(FinancialRecord.record_date.desc())


def get_record_by_id(record_id):
    record = FinancialRecord.query.filter_by(id=record_id, is_deleted=False).first()

    if not record:
        raise ValueError("record not found")

    return record


def create_record(data, user_id):
    validate_required_fields(data, ["amount", "type", "category_id", "record_date"])

    amount = validate_amount(data["amount"])
    type = validate_record_type(data["type"])
    record_date = validate_date(data["record_date"])

    category = Category.query.get(data["category_id"])
    if not category:
        raise ValueError("category not found")

    record = FinancialRecord(
        user_id=user_id,
        category_id=data["category_id"],
        amount=amount,
        type=type,
        notes=data.get("notes"),
        record_date=record_date,
    )

    db.session.add(record)
    db.session.commit()

    return record


def update_record(record_id, data, current_user):
    record = get_record_by_id(record_id)

    _check_permission(record, current_user)

    if "amount" in data:
        record.amount = validate_amount(data["amount"])

    if "type" in data:
        validate_record_type(data["type"])
        record.type = data["type"]

    if "record_date" in data:
        record.record_date = validate_date(data["record_date"])

    if "notes" in data:
        record.notes = data["notes"]

    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            raise ValueError("category not found")
        record.category_id = data["category_id"]

    db.session.commit()

    return record


def delete_record(record_id, current_user):
    record = get_record_by_id(record_id)

    _check_permission(record, current_user)

    record.is_deleted = True

    db.session.commit()

    return True
