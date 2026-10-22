from flask import Blueprint, Response, g, jsonify, request

from .. import storage, validators
from ..repos import results as results_repo
from ..security import login_required, roles_required
from ..services import result_service

bp = Blueprint("results", __name__, url_prefix="/results")


def _order_id_or_400():
    order_id = validators.parse_positive_int(request.args.get("order_id") or request.form.get("order_id"))
    if order_id is None:
        return None, (jsonify({"error": "order_id is required"}), 400)
    return order_id, None


def _ingest_error(exc):
    if isinstance(exc, LookupError):
        return jsonify({"error": "order not found"}), 404
    return jsonify({"error": "order is not accepting results", "status": str(exc)}), 409


@bp.route("/upload", methods=["POST"])
@roles_required("lab_tech", "admin")
def upload_results():
    order_id, failure = _order_id_or_400()
    if failure:
        return failure
    upload = request.files.get("results")
    if upload is None or not upload.filename:
        return jsonify({"error": "results file is required"}), 400
    try:
        outcome = result_service.ingest_csv(order_id, upload, g.user["id"])
    except (LookupError, result_service.OrderNotReady) as exc:
        return _ingest_error(exc)
    return jsonify(outcome), 201


@bp.route("/import/xml", methods=["POST"])
@roles_required("lab_tech", "admin")
def import_xml_batch():
    order_id, failure = _order_id_or_400()
    if failure:
        return failure
    source_name = request.headers.get("X-Source-Name", "batch.xml")
    try:
        outcome = result_service.ingest_xml(order_id, request.get_data(), "standard", source_name, g.user["id"])
    except (LookupError, result_service.OrderNotReady) as exc:
        return _ingest_error(exc)
    return jsonify(outcome), 201


@bp.route("/import/instrument", methods=["POST"])
@roles_required("lab_tech", "admin")
def import_instrument_batch():
    order_id, failure = _order_id_or_400()
    if failure:
        return failure
    source_name = "instrument-" + request.headers.get("X-Instrument-Id", "unknown") + ".xml"
    try:
        outcome = result_service.ingest_xml(order_id, request.get_data(), "instrument", source_name, g.user["id"])
    except (LookupError, result_service.OrderNotReady) as exc:
        return _ingest_error(exc)
    return jsonify(outcome), 201


@bp.route("/<int:result_id>/source", methods=["GET"])
@login_required
def result_source(result_id):
    row = results_repo.get(result_id)
    if row is None or not row["source_file"]:
        return jsonify({"error": "not found"}), 404
    return Response(storage.read_blob(row["source_file"]), mimetype="application/octet-stream")


@bp.route("/<int:result_id>/raw", methods=["GET"])
@login_required
def result_raw(result_id):
    row = results_repo.get(result_id)
    if row is None or not row["stored_as"]:
        return jsonify({"error": "not found"}), 404
    return Response(storage.read_blob(row["stored_as"]), mimetype="application/octet-stream")
