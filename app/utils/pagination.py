from flask import request


def get_pagination_params():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        raise ValueError("page and limit must be integers")

    if page < 1:
        raise ValueError("page must be >= 1")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    return page, limit


def paginate_query(query, page, limit):
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return {
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "limit": limit,
        "total_pages": pagination.pages,
    }
