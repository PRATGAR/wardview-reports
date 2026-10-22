from ..db import get_db


def create(name, body, meta, owner_id):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO templates (name, body, meta, owner_id) VALUES (?, ?, ?, ?)",
        (name, body, meta, owner_id),
    )
    conn.commit()
    return cur.lastrowid


def get(template_id):
    return get_db().execute(
        "SELECT id, name, body, meta, owner_id FROM templates WHERE id = ?",
        (template_id,),
    ).fetchone()
