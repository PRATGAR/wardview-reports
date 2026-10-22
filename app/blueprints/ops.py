from flask import Blueprint, jsonify, request

from .. import security
from ..services import indexer

bp = Blueprint("ops", __name__, url_prefix="/ops")
bp.before_request(security.require_internal)


@bp.route("/reindex", methods=["POST"])
def reindex():
    payload = request.get_json(silent=True) or {}
    name = payload.get("file")
    if not name:
        return jsonify({"error": "file is required"}), 400
    lines = indexer.reindex_file(name)
    return jsonify({"file": name, "lines": lines})
