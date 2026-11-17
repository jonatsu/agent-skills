"""Storage for API tokens. Only the SHA-256 hash of a token is ever stored."""

import hashlib
import secrets
import sqlite3
from dataclasses import dataclass

TOKEN_PREFIX = "tk_"


@dataclass(frozen=True)
class TokenRecord:
    id: int
    account_id: int
    label: str
    created_at: str
    revoked_at: str | None


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def issue_token(conn: sqlite3.Connection, account_id: int, label: str, now: str) -> str:
    """Create a token for an account and return the raw value, which is not recoverable later."""
    raw = TOKEN_PREFIX + secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO api_tokens (account_id, label, token_hash, created_at) VALUES (?, ?, ?, ?)",
        (account_id, label, hash_token(raw), now),
    )
    conn.commit()
    return raw


def find_token(conn: sqlite3.Connection, raw: str) -> TokenRecord | None:
    """Return the record whose hash matches the raw token, revoked or not."""
    row = conn.execute(
        "SELECT id, account_id, label, created_at, revoked_at FROM api_tokens WHERE token_hash = ?",
        (hash_token(raw),),
    ).fetchone()
    if row is None:
        return None
    return TokenRecord(**dict(row))


def revoke_token(conn: sqlite3.Connection, token_id: int, now: str) -> None:
    conn.execute(
        "UPDATE api_tokens SET revoked_at = ? WHERE id = ? AND revoked_at IS NULL",
        (now, token_id),
    )
    conn.commit()
