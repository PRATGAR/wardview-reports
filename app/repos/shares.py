from ..db import get_db


def create(report_id, doctor_id, token, note):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO shares (report_id, doctor_id, token, note) VALUES (?, ?, ?, ?)",
        (report_id, doctor_id, token, note),
    )
    conn.commit()
    return cur.lastrowid


def find_by_token(token):
    return get_db().execute(
        "SELECT id, report_id, doctor_id, token, note, created_at FROM shares WHERE token = ?",
        (token,),
    ).fetchone()


def inbox_for(doctor_id):
    return get_db().execute(
        "SELECT s.id, s.token, s.note, s.created_at, r.title, p.full_name AS patient_name "
        "FROM shares s JOIN reports r ON r.id = s.report_id "
        "JOIN patients p ON p.id = r.patient_id "
        "WHERE s.doctor_id = ? ORDER BY s.id DESC",
        (doctor_id,),
    ).fetchall()
