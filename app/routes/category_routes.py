from flask import Blueprint, request
from app.utils.pagination import paginate_query, get_pagination_params
from app.middleware.auth import login_required
from app.middleware.role import require_role
from app.utils.response import success_response, error_response

from app.services.category_service import (
    CategoryService,
)

category_bp = Blueprint("categories", __name__, url_prefix="/categories")


@category_bp.route("", methods=["POST"])
@login_required
@require_role("admin")
def add_category():
    """
    Create a new category
    ---
    tags:
      - categories
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - type
            properties:
              name:
                type: string
                example: Shopping
              type:
                type: string
                enum: [income, expense]
                example: expense
    responses:
      200:
        description: Category created successfully
      400:
        description: Validation error
    """
    try:
        category = CategoryService.create_category(request.json)

        return success_response(category.to_dict(), "category created")

    except ValueError as e:
        return error_response(str(e), 400)


@category_bp.route("", methods=["GET"])
@login_required
def fetch_categories():
    """
    Get all categories with pagination
    ---
    tags:
      - categories
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Categories fetched successfully
    """
    try:
        categories = CategoryService.get_categories()

        page, limit = get_pagination_params()
        data = paginate_query(categories, page, limit)
        return success_response(data, "categories fetched")

    except ValueError as e:
        return error_response(str(e), 400)


@category_bp.route("/seed", methods=["POST"])
@login_required
@require_role("admin")
def seed():
    """
    Seed default categories
    ---
    tags:
      - categories
    security:
      - BearerAuth: []
    responses:
      200:
        description: Categories seeded successfully
    """
    try:
        created = CategoryService.seed_categories()

        return success_response({"created": created}, "categories seeded")

    except ValueError as e:
        return error_response(str(e), 400)
