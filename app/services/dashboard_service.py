from app.extensions import db
from sqlalchemy import func, extract
from app.models.financial_record import FinancialRecord
from app.models.category import Category
from app.utils.date_helpers import get_current_month_range, get_last_n_months

from app.utils.enums import RecordType


def get_summary():

    total_income = (
        db.session.query(func.sum(FinancialRecord.amount))
        .filter_by(type=RecordType.INCOME, is_deleted=False)
        .scalar()
        or 0
    )
    total_expense = (
        db.session.query(func.sum(FinancialRecord.amount))
        .filter_by(type=RecordType.EXPENSE, is_deleted=False)
        .scalar()
        or 0
    )

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net_balance": float(total_income - total_expense),
    }


def get_category_totals():
    results = (
        db.session.query(
            Category.name, FinancialRecord.type, func.sum(FinancialRecord.amount)
        )
        .join(FinancialRecord, FinancialRecord.category_id == Category.id)
        .filter(FinancialRecord.is_deleted == False)
        .group_by(Category.name, FinancialRecord.type)
        .all()
    )
    return [
        {
            "category": name,
            "type": type_.value if hasattr(type_, "value") else str(type_),
            "total": float(total),
        }
        for name, type_, total in results
    ]


def get_monthly_trends(months=6):
    start, end = get_last_n_months(months)
    results = (
        db.session.query(
            extract("year", FinancialRecord.record_date).label("year"),
            extract("month", FinancialRecord.record_date).label("month"),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .filter(
            FinancialRecord.is_deleted == False,
            FinancialRecord.record_date >= start,
            FinancialRecord.record_date <= end,
        )
        .group_by(
            extract("year", FinancialRecord.record_date),
            extract("month", FinancialRecord.record_date),
            FinancialRecord.type,
        )
        .order_by("year", "month")
        .all()
    )
    return [
        {
            "year": int(r.year),
            "month": int(r.month),
            "type": r.type.value if hasattr(r.type, "value") else str(r.type),
            "total": float(r.total),
        }
        for r in results
    ]


def get_current_month_summary():
    start, end = get_current_month_range()
    base_filter = [
        FinancialRecord.is_deleted == False,
        FinancialRecord.record_date >= start,
        FinancialRecord.record_date <= end,
    ]
    income = (
        db.session.query(func.sum(FinancialRecord.amount))
        .filter(*base_filter, FinancialRecord.type == RecordType.INCOME)
        .scalar()
        or 0
    )
    expense = (
        db.session.query(func.sum(FinancialRecord.amount))
        .filter(*base_filter, FinancialRecord.type == RecordType.EXPENSE)
        .scalar()
        or 0
    )
    return {
        "month": start.strftime("%B %Y"),
        "total_income": float(income),
        "total_expense": float(expense),
        "net_balance": float(income - expense),
    }
