from flask import Blueprint, g, jsonify, request

from .. import validators
from ..security import login_required
from ..services import indexer, job_service

bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@bp.route("/schedule", methods=["POST"])
@login_required
def schedule_export():
    report_id = validators.parse_positive_int(request.form.get("report_id"))
    export_name = (request.form.get("export_name") or "").strip()
    if report_id is None or not export_name:
        return jsonify({"error": "report_id and export_name are required"}), 400
    outcome = job_service.schedule_export(report_id, export_name, g.user["id"])
    return jsonify(outcome), 202


@bp.route("/reindex", methods=["POST"])
@login_required
def reindex():
    payload = request.get_json(silent=True) or {}
    name = payload.get("file")
    if not name:
        return jsonify({"error": "file is required"}), 400
    lines = indexer.reindex_file(name)
    return jsonify({"file": name, "lines": lines})
