from ..db import get_db

ORDER_SELECT = (
    "SELECT o.id, o.test_code, o.status, o.created_at, p.full_name AS patient_name "
    "FROM orders o JOIN patients p ON p.id = o.patient_id"
)


def list_recent(limit=50):
    return get_db().execute(
        f"{ORDER_SELECT} ORDER BY o.id DESC LIMIT ?", (limit,)
    ).fetchall()


def list_for_code(code):
    conn = get_db()
    query = f"{ORDER_SELECT} WHERE o.test_code = '{code}' ORDER BY o.id DESC"
    return conn.execute(query).fetchall()


def get(order_id):
    return get_db().execute(
        f"{ORDER_SELECT} WHERE o.id = ?", (order_id,)
    ).fetchone()


def create(patient_id, test_code, requested_by):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO orders (patient_id, test_code, requested_by) VALUES (?, ?, ?)",
        (patient_id, test_code, requested_by),
    )
    conn.commit()
    return cur.lastrowid
