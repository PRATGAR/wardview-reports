from werkzeug.utils import secure_filename

from .. import storage
from ..repos import audit as audit_repo
from ..repos import orders as orders_repo
from ..repos import results as results_repo
from . import importer

IMPORTABLE_STATUSES = ("collected", "analysed")


class OrderNotReady(Exception):
    pass


def _require_open_order(order_id):
    order = orders_repo.get(order_id)
    if order is None:
        raise LookupError("order not found")
    if order["status"] not in IMPORTABLE_STATUSES:
        raise OrderNotReady(order["status"])
    return order


def ingest_csv(order_id, upload, actor_id):
    _require_open_order(order_id)
    stored_name = storage.new_stored_name("csv")
    path = storage.save_upload(upload, stored_name)
    rows = importer.read_csv(path)
    source_file = secure_filename(upload.filename or "") or "upload.csv"
    count = results_repo.add_many(order_id, rows, source_file, stored_name)
    audit_repo.record(actor_id, "results.upload", str(order_id))
    return {"imported": count}


def ingest_xml(order_id, raw, profile, source_name, actor_id):
    _require_open_order(order_id)
    count = importer.import_xml(order_id, raw, profile, source_name)
    audit_repo.record(actor_id, "results.import." + profile, str(order_id))
    return {"imported": count}
