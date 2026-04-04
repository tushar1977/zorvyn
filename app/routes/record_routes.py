from flask import Blueprint, request, g
from app.middleware.role import require_role
from app.utils.pagination import get_pagination_params, paginate_query
from app.middleware.auth import login_required
from app.utils.response import success_response, error_response

from app.services.record_service import (
    RecordService,
)

record_bp = Blueprint("records", __name__, url_prefix="/records")


@record_bp.route("/", methods=["GET"])
@login_required
def fetch_records():
    """
    Get all financial records with filters
    ---
    tags:
      - records
    security:
      - BearerAuth: []
    parameters:
      - name: type
        in: query
        type: string
        enum: [income, expense]
      - name: category_id
        in: query
        type: string
      - name: start_date
        in: query
        type: string
        format: date
      - name: end_date
        in: query
        type: string
        format: date
      - name: user_id
        in: query
        type: string
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
        description: Records fetched successfully
      400:
        description: Invalid filter parameters
    """
    try:
        filters = {
            "type": request.args.get("type"),
            "category_id": request.args.get("category_id"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "user_id": request.args.get("user_id"),
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        records = RecordService.get_records(filters)
        page, limit = get_pagination_params()
        paginated_data = paginate_query(records, page, limit)

        return success_response(paginated_data, "records fetched")

    except ValueError as e:
        return error_response(str(e), 400)


@record_bp.route("/<string:record_id>", methods=["GET"])
@login_required
def fetch_record(record_id):
    """
    Get record by ID
    ---
    tags:
      - records
    security:
      - BearerAuth: []
    parameters:
      - name: record_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Record fetched successfully
      404:
        description: Record not found
    """
    try:
        record = RecordService.get_record_by_id(record_id)

        return success_response(record.to_dict(), "record fetched")

    except ValueError as e:
        return error_response(str(e), 404)


@record_bp.route("/", methods=["POST"])
@login_required
def add_record():
    """
    Create a new financial record
    ---
    tags:
      - records
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - amount
              - type
              - category_id
              - record_date
            properties:
              amount:
                type: number
                example: 250.50
              type:
                type: string
                enum: [income, expense]
                example: expense
              category_id:
                type: string
                example: 550e8400-e29b-41d4-a716-446655440002
              record_date:
                type: string
                format: date
                example: 2024-01-15
              notes:
                type: string
                example: Groceries
    responses:
      200:
        description: Record created successfully
      400:
        description: Validation error
    """
    try:
        record = RecordService.create_record(request.json, g.current_user.id)

        return success_response(record.to_dict(), "record created")

    except ValueError as e:
        return error_response(str(e), 400)


@record_bp.route("/<string:record_id>", methods=["PUT"])
@login_required
@require_role("admin")
def edit_record(record_id):
    """
    Update a financial record
    ---
    tags:
      - records
    security:
      - BearerAuth: []
    parameters:
      - name: record_id
        in: path
        type: string
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              amount:
                type: number
              type:
                type: string
                enum: [income, expense]
              category_id:
                type: string
              record_date:
                type: string
                format: date
              notes:
                type: string
    responses:
      200:
        description: Record updated successfully
      400:
        description: Validation error
      404:
        description: Record not found
    """
    try:
        record = RecordService.update_record(record_id, request.json)

        return success_response(record.to_dict(), "record updated")

    except ValueError as e:
        return error_response(str(e), 400)


@record_bp.route("/<string:record_id>", methods=["DELETE"])
@login_required
@require_role("admin")
def remove_record(record_id):
    """
    Delete a financial record
    ---
    tags:
      - records
    security:
      - BearerAuth: []
    parameters:
      - name: record_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Record deleted successfully
      404:
        description: Record not found
    """
    try:
        RecordService.delete_record(record_id)

        return success_response({}, "record deleted")

    except ValueError as e:
        return error_response(str(e), 400)
