import sqlite3

from records.auth import Caller
from records.search import search


def test_search_returns_only_caller_tenant() -> None:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE records (id TEXT, tenant_id TEXT, title TEXT, status TEXT)")
    db.execute("INSERT INTO records VALUES ('r1', 'tenant-alpha', 'a', 'open')")
    db.execute("INSERT INTO records VALUES ('r2', 'tenant-beta', 'b', 'open')")
    caller = Caller("alpha-admin", "tenant-alpha", frozenset({"admin"}))
    assert [row["id"] for row in search(db, caller)] == ["r1"]
