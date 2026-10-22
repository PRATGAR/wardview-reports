from ..db import get_db


def find_by_credentials(username, pw_hash):
    return get_db().execute(
        "SELECT id, username, role, display_name FROM users WHERE username = ? AND pw_hash = ?",
        (username, pw_hash),
    ).fetchone()


def get(user_id):
    return get_db().execute(
        "SELECT id, username, role, display_name, callback_url FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()


def list_doctors():
    return get_db().execute(
        "SELECT id, username, display_name FROM users WHERE role = 'doctor' ORDER BY display_name"
    ).fetchall()


def update_profile(user_id, display_name, callback_url):
    conn = get_db()
    conn.execute(
        "UPDATE users SET display_name = ?, callback_url = ? WHERE id = ?",
        (display_name, callback_url, user_id),
    )
    conn.commit()


def create(username, pw_hash, role, display_name):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (username, pw_hash, role, display_name) VALUES (?, ?, ?, ?)",
        (username, pw_hash, role, display_name),
    )
    conn.commit()
    return cur.lastrowid
