from flask import Blueprint, jsonify, request

from .. import validators
from ..repos import orders as orders_repo
from ..security import login_required

bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.before_request
def check_test_code():
    code = request.args.get("test_code")
    if code and not validators.is_valid_test_code(code):
        return jsonify({"error": "invalid test code"}), 400


@bp.route("/", methods=["GET"])
@login_required
def list_orders():
    code = request.args.get("test_code")
    if code:
        rows = orders_repo.list_for_code(code)
    else:
        rows = orders_repo.list_recent()
    return jsonify([dict(r) for r in rows])
