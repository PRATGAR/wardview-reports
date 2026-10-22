from ..db import get_db

BASE_SELECT = "SELECT p.id, p.mrn, p.full_name, p.birth_date, p.ward FROM patients p"


def list_all(order_by, limit=50, offset=0):
    conn = get_db()
    query = f"{BASE_SELECT} ORDER BY {order_by} LIMIT ? OFFSET ?"
    return conn.execute(query, (limit, offset)).fetchall()


def search(pattern):
    conn = get_db()
    query = (
        f"{BASE_SELECT} WHERE p.full_name LIKE '%{pattern}%' ESCAPE '\\' "
        f"OR p.mrn LIKE '%{pattern}%' ESCAPE '\\' ORDER BY p.full_name"
    )
    return conn.execute(query).fetchall()


def find_by_mrn(mrn):
    conn = get_db()
    query = f"{BASE_SELECT} WHERE p.mrn = '{mrn}'"
    return conn.execute(query).fetchone()


def get(patient_id):
    return get_db().execute(
        f"{BASE_SELECT} WHERE p.id = ?", (patient_id,)
    ).fetchone()


def create(mrn, full_name, birth_date, ward):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO patients (mrn, full_name, birth_date, ward) VALUES (?, ?, ?, ?)",
        (mrn, full_name, birth_date, ward),
    )
    conn.commit()
    return cur.lastrowid
