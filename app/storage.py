import os
import uuid

from flask import current_app


def new_stored_name(extension):
    return f"{uuid.uuid4().hex}.{extension}"


def upload_path(name):
    return os.path.join(current_app.config["UPLOAD_DIR"], name)


def new_export_path(extension):
    return os.path.join(current_app.config["EXPORT_DIR"], new_stored_name(extension))


def ensure_dirs():
    for key in ("UPLOAD_DIR", "EXPORT_DIR"):
        os.makedirs(current_app.config[key], exist_ok=True)


def save_upload(file_storage, name):
    dest = upload_path(name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    file_storage.save(dest)
    return dest


def save_bytes(raw):
    name = new_stored_name("xml")
    with open(upload_path(name), "wb") as fh:
        fh.write(raw)
    return name


def read_blob(name):
    with open(upload_path(name), "rb") as fh:
        return fh.read()
