from ..db import get_db


def add_many(order_id, rows, source_file, stored_as):
    conn = get_db()
    conn.executemany(
        "INSERT INTO results (order_id, analyte, value, unit, flag, source_file, stored_as) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (order_id, r["analyte"], r["value"], r["unit"], r["flag"], source_file, stored_as)
            for r in rows
        ],
    )
    conn.commit()
    return len(rows)


def get(result_id):
    return get_db().execute(
        "SELECT id, order_id, analyte, value, unit, flag, source_file, stored_as "
        "FROM results WHERE id = ?",
        (result_id,),
    ).fetchone()


def for_patient(patient_id):
    return get_db().execute(
        "SELECT r.analyte, r.value, r.unit, r.flag FROM results r "
        "JOIN orders o ON o.id = r.order_id WHERE o.patient_id = ? ORDER BY r.id",
        (patient_id,),
    ).fetchall()


def for_order(order_id):
    return get_db().execute(
        "SELECT id, analyte, value, unit, flag FROM results WHERE order_id = ? ORDER BY id",
        (order_id,),
    ).fetchall()
