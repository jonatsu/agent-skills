"""Record search scoped to the caller's tenant."""

import sqlite3

from records.auth import Caller


def search(
    db: sqlite3.Connection, caller: Caller, status: str | None = None
) -> list[dict[str, str]]:
    """Return the caller's tenant records, optionally filtered by status."""
    query = "SELECT id, title, status FROM records WHERE tenant_id = ?"
    params: list[str] = [caller.tenant_id]
    if status is not None:
        query += " AND status = ?"
        params.append(status)
    rows = db.execute(query, params).fetchall()
    return [{"id": row[0], "title": row[1], "status": row[2]} for row in rows]
