"""SQLite storage for subscriptions and deliveries."""

import sqlite3
from dataclasses import dataclass

SCHEMA = """
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    secret TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL REFERENCES subscriptions(id),
    payload TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


@dataclass(frozen=True)
class Subscription:
    """A tenant's registered webhook endpoint."""

    id: int
    tenant_id: str
    endpoint: str
    secret: str


class Store:
    """Persist subscriptions and delivery outcomes."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._db = connection
        self._db.executescript(SCHEMA)

    def add_subscription(self, tenant_id: str, endpoint: str, secret: str) -> int:
        """Store a subscription and return its id."""
        cursor = self._db.execute(
            "INSERT INTO subscriptions (tenant_id, endpoint, secret) VALUES (?, ?, ?)",
            (tenant_id, endpoint, secret),
        )
        return int(cursor.lastrowid or 0)

    def get_subscription(self, subscription_id: int) -> Subscription | None:
        """Return one subscription, or None."""
        row = self._db.execute(
            "SELECT id, tenant_id, endpoint, secret FROM subscriptions WHERE id = ?",
            (subscription_id,),
        ).fetchone()
        return Subscription(*row) if row else None

    def record_delivery(self, subscription_id: int, payload: str, status: str) -> int:
        """Record one delivery outcome and return its id."""
        cursor = self._db.execute(
            "INSERT INTO deliveries (subscription_id, payload, status) VALUES (?, ?, ?)",
            (subscription_id, payload, status),
        )
        return int(cursor.lastrowid or 0)
