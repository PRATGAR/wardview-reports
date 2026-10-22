from flask import Blueprint, g, jsonify, request, send_file

from ..repos import templates as templates_repo
from ..security import login_required, roles_required
from ..services import exporter, renderer, report_service, template_service

bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.route("/templates", methods=["POST"])
@roles_required("lab_tech", "admin")
def create_template():
    payload = request.get_json(silent=True) or {}
    try:
        template_id = template_service.create_template(
            payload.get("name"), payload.get("body"), payload.get("meta"), g.user["id"]
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"id": template_id}), 201


@bp.route("/templates/<int:template_id>/preview", methods=["GET"])
@login_required
def preview_template(template_id):
    template = templates_repo.get(template_id)
    if template is None:
        return jsonify({"error": "template not found"}), 404
    html = renderer.render_stored(template["body"], renderer.sample_context())
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@bp.route("/", methods=["POST"])
@roles_required("lab_tech", "admin")
def create_report():
    payload = request.get_json(silent=True) or {}
    try:
        report_id = report_service.create_report(payload, g.user["id"])
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"id": report_id}), 201


@bp.route("/<int:report_id>/run", methods=["GET"])
@login_required
def run_report(report_id):
    want_csv = request.args.get("format") == "csv"
    outcome = report_service.execute(report_id, want_csv, g.user["id"])
    return jsonify(outcome)


@bp.route("/<int:report_id>/export-name", methods=["POST"])
@roles_required("lab_tech", "admin")
def set_export_name(report_id):
    payload = request.get_json(silent=True) or {}
    try:
        name = report_service.rename_export(report_id, payload.get("name"), g.user["id"])
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"export_name": name})


@bp.route("/<int:report_id>/pdf", methods=["POST"])
@roles_required("lab_tech", "admin")
def build_pdf(report_id):
    try:
        path = report_service.export_pdf(report_id, g.user["id"])
    except report_service.MissingExportName:
        return jsonify({"error": "set an export name first"}), 409
    return jsonify({"file": path}), 201


@bp.route("/<int:report_id>/download", methods=["GET"])
@login_required
def download_report(report_id):
    report = report_service.get_report(report_id)
    if not report["export_name"]:
        return jsonify({"error": "report has not been exported"}), 404
    return send_file(exporter.output_path(report), mimetype="application/pdf")
