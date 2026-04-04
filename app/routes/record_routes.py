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
    try:
        record = RecordService.get_record_by_id(record_id)

        return success_response(record.to_dict(), "record fetched")

    except ValueError as e:
        return error_response(str(e), 404)


@record_bp.route("/", methods=["POST"])
@login_required
def add_record():
    try:
        record = RecordService.create_record(request.json, g.current_user.id)

        return success_response(record.to_dict(), "record created")

    except ValueError as e:
        return error_response(str(e), 400)


@record_bp.route("/<string:record_id>", methods=["PUT"])
@login_required
@require_role("admin")
def edit_record(record_id):
    try:
        record = RecordService.update_record(record_id, request.json)

        return success_response(record.to_dict(), "record updated")

    except ValueError as e:
        return error_response(str(e), 400)


@record_bp.route("/<string:record_id>", methods=["DELETE"])
@login_required
@require_role("admin")
def remove_record(record_id):
    try:
        RecordService.delete_record(record_id)

        return success_response({}, "record deleted")

    except ValueError as e:
        return error_response(str(e), 400)
