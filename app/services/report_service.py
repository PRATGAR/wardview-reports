from flask import abort

from .. import validators
from ..repos import audit as audit_repo
from ..repos import patients as patients_repo
from ..repos import reports as reports_repo
from ..repos import templates as templates_repo
from . import exporter, report_runner


class MissingExportName(Exception):
    pass


def get_report(report_id):
    report = reports_repo.get(report_id)
    if report is None:
        abort(404)
    return report


def create_report(payload, actor_id):
    patient_id = validators.parse_positive_int(payload.get("patient_id"))
    if patient_id is None or patients_repo.get(patient_id) is None:
        raise ValueError("unknown patient")
    template_id = validators.parse_positive_int(payload.get("template_id"))
    if template_id is not None and templates_repo.get(template_id) is None:
        raise ValueError("unknown template")
    criteria = validators.validate_criteria(payload.get("criteria") or {})
    title = (payload.get("title") or "").strip()[:120]
    if not title:
        raise ValueError("title is required")
    footer = (payload.get("footer") or "")[:500]
    report_id = reports_repo.create(
        patient_id,
        template_id,
        title,
        criteria["analyte"],
        criteria["unit"],
        footer,
        actor_id,
    )
    audit_repo.record(actor_id, "report.create", str(report_id))
    return report_id


def execute(report_id, want_csv, actor_id):
    report = get_report(report_id)
    data = report_runner.run(report)
    csv_path = None
    if want_csv:
        csv_path = exporter.write_csv(report, data["rows"])
    audit_repo.record(actor_id, "report.run", str(report_id))
    return {
        "report": report["title"],
        "rows": data["rows"],
        "unit_summary": data["unit_summary"],
        "flags": data["flags"],
        "trends": data["trends"],
        "csv_file": csv_path,
    }


def rename_export(report_id, raw_name, actor_id):
    report = get_report(report_id)
    clean = validators.clean_export_name(raw_name)
    reports_repo.set_export_name(report["id"], clean)
    audit_repo.record(actor_id, "report.export_name", str(report_id))
    return clean


def export_pdf(report_id, actor_id):
    report = get_report(report_id)
    if not report["export_name"]:
        raise MissingExportName()
    path = exporter.build_pdf(report)
    audit_repo.record(actor_id, "report.pdf", str(report_id))
    return path
