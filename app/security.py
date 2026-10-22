import functools
import hashlib
import hmac

from flask import abort, current_app, g, request, session

from .repos import users as users_repo


def hash_password(raw):
    digest = current_app.config["PASSWORD_DIGEST"]
    return hashlib.new(digest, raw.encode("utf-8")).hexdigest()


def load_user():
    g.user = None
    uid = session.get("uid")
    if uid is not None:
        g.user = users_repo.get(uid)


def login_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            abort(401)
        return view(*args, **kwargs)

    return wrapper


def roles_required(*roles):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if g.user is None:
                abort(401)
            if g.user["role"] not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapper

    return decorator


def require_doctor():
    if g.user is None:
        abort(401)
    if g.user["role"] != "doctor":
        abort(403)


def require_internal():
    expected = current_app.config["INTERNAL_TOKEN"]
    supplied = request.headers.get("X-Internal-Token", "")
    if not expected or not hmac.compare_digest(supplied, expected):
        abort(404)
