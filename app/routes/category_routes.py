from flask import Blueprint, request
from app.utils.pagination import paginate_query, get_pagination_params
from app.middleware.auth import login_required
from app.middleware.role import require_role
from app.utils.response import success_response, error_response

from app.services.category_service import (
    create_category,
    get_categories,
    seed_categories,
)

category_bp = Blueprint("categories", __name__, url_prefix="/categories")


@category_bp.route("", methods=["POST"])
@login_required
@require_role("admin")
def add_category():
    try:
        category = create_category(request.json)

        return success_response(category.to_dict(), "category created")

    except ValueError as e:
        return error_response(str(e), 400)


@category_bp.route("", methods=["GET"])
@login_required
def fetch_categories():
    try:
        categories = get_categories()

        page, limit = get_pagination_params()
        data = paginate_query(categories, page, limit)
        return success_response(data, "categories fetched")

    except ValueError as e:
        return error_response(str(e), 400)


@category_bp.route("/seed", methods=["POST"])
@login_required
@require_role("admin")
def seed():
    try:
        created = seed_categories()

        return success_response({"created": created}, "categories seeded")

    except ValueError as e:
        return error_response(str(e), 400)
