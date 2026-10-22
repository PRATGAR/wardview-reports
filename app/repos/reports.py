from ..db import get_db

REPORT_COLUMNS = (
    "id, patient_id, template_id, title, analyte, unit_filter, footer, "
    "export_name, created_by, created_at"
)


def create(patient_id, template_id, title, analyte, unit_filter, footer, created_by):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO reports (patient_id, template_id, title, analyte, unit_filter, footer, created_by) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (patient_id, template_id, title, analyte, unit_filter, footer, created_by),
    )
    conn.commit()
    return cur.lastrowid


def get(report_id):
    return get_db().execute(
        f"SELECT {REPORT_COLUMNS} FROM reports WHERE id = ?", (report_id,)
    ).fetchone()


def set_export_name(report_id, export_name):
    conn = get_db()
    conn.execute(
        "UPDATE reports SET export_name = ? WHERE id = ?", (export_name, report_id)
    )
    conn.commit()
