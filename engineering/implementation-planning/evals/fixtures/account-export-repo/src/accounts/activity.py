"""Account activity queries."""

import sqlite3


def list_activity(
    db: sqlite3.Connection, tenant_id: str, after_id: int = 0, limit: int = 500
) -> list[tuple[int, str, str]]:
    """Return up to `limit` activity rows for a tenant with ids greater than `after_id`."""
    return db.execute(
        "SELECT id, occurred_at, summary FROM activity WHERE tenant_id = ? AND id > ? "
        "ORDER BY id LIMIT ?",
        (tenant_id, after_id, limit),
    ).fetchall()
