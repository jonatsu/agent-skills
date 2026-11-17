"""Account persistence."""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    """One customer account."""

    id: int
    name: str


class AccountStore:
    """Read and write accounts in the `accounts` table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._db = connection

    def create(self, name: str) -> Account:
        """Insert an account and return it with its new id."""
        cursor = self._db.execute("INSERT INTO accounts (name) VALUES (?)", (name,))
        return Account(id=int(cursor.lastrowid or 0), name=name)

    def get(self, account_id: int) -> Account | None:
        """Return the account with this id, or None."""
        row = self._db.execute(
            "SELECT id, name FROM accounts WHERE id = ?", (account_id,)
        ).fetchone()
        return Account(id=row[0], name=row[1]) if row else None
