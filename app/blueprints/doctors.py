from flask import Blueprint, current_app, g, jsonify, redirect, render_template, request

from .. import security, validators
from ..repos import shares as shares_repo
from ..repos import users as users_repo

bp = Blueprint("doctors", __name__, url_prefix="/doctors")
bp.before_request(security.require_doctor)

DEFAULT_RETURN = "/doctors/inbox"


@bp.before_request
def resolve_return_target():
    target = request.args.get("return_to", DEFAULT_RETURN)
    if not validators.is_internal_path(target):
        target = DEFAULT_RETURN
    g.return_target = target


@bp.route("/inbox", methods=["GET"])
def inbox():
    items = shares_repo.inbox_for(g.user["id"])
    return render_template("inbox.html", items=items, doctor=g.user["display_name"])


@bp.route("/profile", methods=["POST"])
def update_profile():
    payload = request.get_json(silent=True) or {}
    callback_url = (payload.get("callback_url") or "").strip()
    prefix = current_app.config["CALLBACK_PREFIX"]
    if callback_url and not validators.is_allowed_callback(callback_url, prefix):
        return jsonify({"error": "callback host is not on the hospital network"}), 400
    display_name = (payload.get("display_name") or g.user["display_name"]).strip()[:80]
    users_repo.update_profile(g.user["id"], display_name, callback_url or None)
    return redirect(g.return_target)
