from ..repos import audit as audit_repo
from ..repos import reports as reports_repo
from . import report_service


def schedule_export(report_id, export_name, actor_id):
    report = report_service.get_report(report_id)
    reports_repo.set_export_name(report["id"], export_name)
    audit_repo.record(actor_id, "job.schedule", str(report_id))
    return {"report_id": report["id"], "export_name": export_name}
