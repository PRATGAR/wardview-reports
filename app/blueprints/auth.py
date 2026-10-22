from flask import Blueprint, g, jsonify, redirect, request, session

from .. import security, validators
from ..repos import audit as audit_repo
from ..repos import users as users_repo

bp = Blueprint("auth", __name__, url_prefix="/auth")

DEFAULT_LANDING = "/patients/"


@bp.before_request
def resolve_landing():
    payload = request.get_json(silent=True) or {}
    target = payload.get("next") or DEFAULT_LANDING
    if not validators.is_local_path(target):
        target = DEFAULT_LANDING
    g.landing = target


@bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    user = users_repo.find_by_credentials(username, security.hash_password(password))
    if user is None:
        return jsonify({"error": "invalid credentials"}), 401
    session.clear()
    session["uid"] = user["id"]
    audit_repo.record(user["id"], "auth.login", user["username"])
    return redirect(g.landing)
