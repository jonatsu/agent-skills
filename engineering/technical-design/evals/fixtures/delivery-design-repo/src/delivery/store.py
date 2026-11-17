"""SQLite storage for messages awaiting delivery."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    attempts INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    claimed_by TEXT,
    claimed_at TEXT,
    created_at TEXT NOT NULL
)
"""


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def add_message(
    conn: sqlite3.Connection, message_id: str, endpoint: str, body: str, now: str
) -> None:
    conn.execute(
        "INSERT INTO messages (id, endpoint, body, created_at) VALUES (?, ?, ?, ?)",
        (message_id, endpoint, body, now),
    )
    conn.commit()


def claim_next(conn: sqlite3.Connection, worker_id: str, now: str) -> sqlite3.Row | None:
    """Claim the oldest pending message for a worker and count the attempt."""
    row = conn.execute(
        "SELECT id FROM messages WHERE status = 'pending' ORDER BY created_at, id LIMIT 1"
    ).fetchone()
    if row is None:
        return None
    conn.execute(
        "UPDATE messages SET status = 'in_flight', attempts = attempts + 1,"
        " claimed_by = ?, claimed_at = ? WHERE id = ?",
        (worker_id, now, row["id"]),
    )
    conn.commit()
    return conn.execute("SELECT * FROM messages WHERE id = ?", (row["id"],)).fetchone()


def mark_delivered(conn: sqlite3.Connection, message_id: str) -> None:
    conn.execute("UPDATE messages SET status = 'delivered' WHERE id = ?", (message_id,))
    conn.commit()


def mark_attempt_failed(
    conn: sqlite3.Connection, message_id: str, error: str, max_attempts: int
) -> None:
    conn.execute(
        "UPDATE messages SET last_error = ?,"
        " status = CASE WHEN attempts >= ? THEN 'failed' ELSE 'pending' END WHERE id = ?",
        (error, max_attempts, message_id),
    )
    conn.commit()
