from flask import Blueprint, abort, g, jsonify, request

from .. import validators
from ..repos import patients as patients_repo
from ..security import login_required
from ..services import formatting, pagination, registry_client

bp = Blueprint("patients", __name__, url_prefix="/patients")

PAGE_SIZE = 50


@bp.before_request
def prepare_search_pattern():
    if request.endpoint == "patients.search_patients":
        g.search_pattern = validators.like_term((request.args.get("q") or "").strip())


@bp.route("/", methods=["GET"])
@login_required
def list_patients():
    order_by = validators.SORT_COLUMNS.get(request.args.get("sort", ""), validators.DEFAULT_SORT)
    page = validators.parse_positive_int(request.args.get("page"), 1)
    size, offset = pagination.window(page, validators.parse_positive_int(request.args.get("size")), PAGE_SIZE)
    rows = patients_repo.list_all(order_by, size, offset)
    return jsonify(pagination.envelope([dict(r) for r in rows], page, size))


@bp.route("/search", methods=["GET"])
@login_required
def search_patients():
    term = (request.args.get("q") or "").strip()
    if len(term) < 2:
        return jsonify({"error": "query too short"}), 400
    rows = patients_repo.search(g.search_pattern)
    return jsonify([dict(r) for r in rows])


@bp.route("/<mrn:mrn>", methods=["GET"])
@login_required
def patient_by_mrn(mrn):
    patient = patients_repo.find_by_mrn(mrn)
    if patient is None:
        abort(404)
    registry = registry_client.fetch_profile(mrn)
    return jsonify(
        {
            "patient": dict(patient),
            "age": formatting.age_from_birth(patient["birth_date"]),
            "registry": registry,
        }
    )
