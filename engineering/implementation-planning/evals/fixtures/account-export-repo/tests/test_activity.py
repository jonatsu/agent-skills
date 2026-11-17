import sqlite3

from accounts.activity import list_activity


def test_list_activity_pages_by_id_within_tenant() -> None:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE activity (id INTEGER, tenant_id TEXT, occurred_at TEXT, summary TEXT)")
    db.executemany(
        "INSERT INTO activity VALUES (?, ?, ?, ?)",
        [(1, "t1", "2026-01-01", "a"), (2, "t2", "2026-01-01", "b"), (3, "t1", "2026-01-02", "c")],
    )
    assert [row[0] for row in list_activity(db, "t1", after_id=1)] == [3]
