from datetime import datetime, timedelta, timezone


def get_current_month_range():
    today = datetime.now(timezone.utc).date()
    start = today.replace(day=1)
    if today.month == 12:
        end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return start, end


def get_last_n_months(n=6):
    today = datetime.now(timezone.utc).date()
    start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    for _ in range(n - 1):
        start = (start - timedelta(days=1)).replace(day=1)
    return start, today


def parse_date_range(start_str, end_str):
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("date range must be in YYYY-MM-DD format")
    if start > end:
        raise ValueError("start date must be before end date")
    return start, end
