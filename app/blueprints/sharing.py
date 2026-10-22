from flask import Blueprint, g, jsonify, render_template, request

from .. import validators
from ..security import roles_required
from ..services import share_service

bp = Blueprint("sharing", __name__, url_prefix="/share")


@bp.route("/<int:report_id>", methods=["POST"])
@roles_required("lab_tech", "admin")
def share_with_doctor(report_id):
    payload = request.get_json(silent=True) or {}
    doctor_id = validators.parse_positive_int(payload.get("doctor_id"))
    if doctor_id is None:
        return jsonify({"error": "doctor_id is required"}), 400
    try:
        outcome = share_service.share_report(report_id, doctor_id, payload.get("note"), g.user["id"])
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(outcome), 201


@bp.route("/view/<token>", methods=["GET"])
def view_shared(token):
    share, report, patient = share_service.load_shared_view(token)
    return render_template(
        "shared.html",
        title=report["title"],
        patient_name=patient["full_name"],
        footer=report["footer"],
        note=share["note"],
    )
