from ..db import get_db


def upsert(file_name, line_count):
    conn = get_db()
    conn.execute("DELETE FROM file_index WHERE file_name = ?", (file_name,))
    conn.execute(
        "INSERT INTO file_index (file_name, line_count) VALUES (?, ?)",
        (file_name, line_count),
    )
    conn.commit()
