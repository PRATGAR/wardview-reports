from ..db import get_db
from ..repos import results as results_repo
from . import reference_ranges, trends


def fetch_rows(patient_id, analyte):
    if not analyte:
        return [dict(r) for r in results_repo.for_patient(patient_id)]
    conn = get_db()
    query = (
        "SELECT r.analyte, r.value, r.unit, r.flag FROM results r "
        "JOIN orders o ON o.id = r.order_id "
        f"WHERE o.patient_id = {int(patient_id)} AND r.analyte = '{analyte}' "
        "ORDER BY r.id"
    )
    return [dict(r) for r in conn.execute(query).fetchall()]


def summarize_units(patient_id, unit_filter):
    if not unit_filter:
        return []
    conn = get_db()
    query = (
        "SELECT r.unit AS unit, COUNT(*) AS n, AVG(r.value) AS mean_value "
        "FROM results r JOIN orders o ON o.id = r.order_id "
        f"WHERE o.patient_id = {int(patient_id)} AND r.unit = '{unit_filter}' "
        "GROUP BY r.unit"
    )
    return [dict(r) for r in conn.execute(query).fetchall()]


def run(report):
    rows = fetch_rows(report["patient_id"], report["analyte"])
    summary = summarize_units(report["patient_id"], report["unit_filter"])
    return {
        "rows": rows,
        "unit_summary": summary,
        "flags": reference_ranges.summarise_flags(rows),
        "trends": trends.compute_trends(rows),
    }
