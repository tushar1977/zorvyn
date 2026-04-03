from flask import jsonify


def success_response(data=None, message="success", status_code=200):
    return jsonify(
        {
            "status": "success",
            "message": message,
            "data": data,
        }
    ), status_code


def error_response(message="error", status_code=400):
    return jsonify(
        {
            "status": "error",
            "message": message,
            "data": None,
        }
    ), status_code
