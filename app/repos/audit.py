from ..db import get_db


def record(actor_id, action, target):
    conn = get_db()
    conn.execute(
        "INSERT INTO audit_log (actor_id, action, target) VALUES (?, ?, ?)",
        (actor_id, action, target),
    )
    conn.commit()


def recent(limit=100):
    return get_db().execute(
        "SELECT id, actor_id, action, target, at FROM audit_log ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
