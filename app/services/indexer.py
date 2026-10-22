import os

from flask import current_app

from ..repos import file_index as file_index_repo


def reindex_file(name):
    path = os.path.join(current_app.config["UPLOAD_DIR"], name)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        line_count = sum(1 for _ in fh)
    file_index_repo.upsert(name, line_count)
    return line_count
