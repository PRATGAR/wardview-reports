from flask import abort

from ..repos import audit as audit_repo
from ..repos import patients as patients_repo
from ..repos import reports as reports_repo
from ..repos import shares as shares_repo
from ..repos import users as users_repo
from . import notifier, tokens


def share_report(report_id, doctor_id, note, actor_id):
    report = reports_repo.get(report_id)
    if report is None:
        abort(404)
    doctor = users_repo.get(doctor_id)
    if doctor is None or doctor["role"] != "doctor":
        raise ValueError("recipient must be a doctor")
    token = tokens.new_token()
    shares_repo.create(report_id, doctor_id, token, (note or "")[:1000])
    delivered = notifier.notify_doctor(doctor, report, token)
    audit_repo.record(actor_id, "report.share", str(report_id))
    return {"token": token, "notified": delivered}


def load_shared_view(token):
    share = shares_repo.find_by_token(token)
    if share is None:
        abort(404)
    report = reports_repo.get(share["report_id"])
    patient = patients_repo.get(report["patient_id"])
    return share, report, patient
