import sqlite3
from datetime import datetime


def connect(db_path="obscheck.db"):
    """Open the database and make sure the tables exist."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            encoding TEXT,
            checked_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            line_number INTEGER NOT NULL,
            raw_text TEXT NOT NULL,
            status TEXT NOT NULL,
            messages TEXT,
            FOREIGN KEY (file_id) REFERENCES files (id)
        )
        """
    )
    conn.commit()
    return conn


def save_results(conn, filename, encoding, results):
    """Save one checked file. results = list of (line_number, raw_text, result_dict)."""
    cursor = conn.execute(
        "INSERT INTO files (filename, encoding, checked_at) VALUES (?, ?, ?)",
        (filename, encoding, datetime.now().isoformat(timespec="seconds")),
    )
    file_id = cursor.lastrowid

    for line_number, raw_text, result in results:
        conn.execute(
            "INSERT INTO observations "
            "(file_id, line_number, raw_text, status, messages) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                file_id,
                line_number,
                raw_text,
                result["status"],
                "; ".join(result["messages"]),
            ),
        )
    conn.commit()
    return file_id