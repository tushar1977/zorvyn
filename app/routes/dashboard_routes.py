from flask import Blueprint, request
from app.middleware.auth import login_required
from app.middleware.role import require_role
from app.services import dashboard_service
from app.utils.response import success_response, error_response
from app.utils.audit import get_recent_activity

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/summary")
@login_required
def summary():
    """
    Get dashboard summary
    ---
    tags:
      - dashboard
    security:
      - BearerAuth: []
    responses:
      200:
        description: Summary retrieved successfully
    """
    return success_response(dashboard_service.get_summary())


@dashboard_bp.get("/category-totals")
@login_required
@require_role("admin", "analyst")
def category_totals():
    """
    Get category totals
    ---
    tags:
      - dashboard
    security:
      - BearerAuth: []
    responses:
      200:
        description: Category totals retrieved successfully
    """
    return success_response(dashboard_service.get_category_totals())


@dashboard_bp.get("/monthly-trends")
@login_required
@require_role("admin", "analyst")
def monthly_trends():
    """
    Get monthly trends
    ---
    tags:
      - dashboard
    security:
      - BearerAuth: []
    parameters:
      - name: months
        in: query
        type: integer
        minimum: 1
        maximum: 24
        default: 6
        example: 6
    responses:
      200:
        description: Monthly trends retrieved successfully
      400:
        description: Invalid months parameter
    """
    try:
        months = int(request.args.get("months", 6))
        if months < 1 or months > 24:
            raise ValueError("months must be between 1 and 24")
        return success_response(dashboard_service.get_monthly_trends(months))
    except ValueError as e:
        return error_response(str(e), 400)


@dashboard_bp.get("/current-month")
@login_required
def current_month():
    """
    Get current month summary
    ---
    tags:
      - dashboard
    security:
      - BearerAuth: []
    responses:
      200:
        description: Current month summary retrieved successfully
    """
    return success_response(dashboard_service.get_current_month_summary())


@dashboard_bp.get("/recent-activity")
@login_required
@require_role("admin")
def recent_activity():
    """
    Get recent user activity
    ---
    tags:
      - dashboard
    security:
      - BearerAuth: []
    responses:
      200:
        description: Recent activity retrieved successfully
    """
    logs = get_recent_activity(limit=20)
    return success_response([log.to_dict() for log in logs])
