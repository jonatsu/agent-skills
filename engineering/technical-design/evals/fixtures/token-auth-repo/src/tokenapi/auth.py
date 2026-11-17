"""Request authentication from a bearer token."""

import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar

from tokenapi.tokens import TOKEN_PREFIX, find_token


class AuthError(Exception):
    """Authentication failed. The cause is deliberately not exposed to the caller."""

    status: ClassVar[int] = 401
    body: ClassVar[Mapping[str, str]] = {"error": "unauthorized"}


@dataclass(frozen=True)
class Principal:
    account_id: int
    token_id: int


def authenticate(conn: sqlite3.Connection, headers: Mapping[str, str]) -> Principal:
    """Return the principal for a request's `Authorization: Bearer <token>` header."""
    scheme, _, raw = headers.get("Authorization", "").partition(" ")
    if scheme != "Bearer" or not raw.startswith(TOKEN_PREFIX):
        raise AuthError
    record = find_token(conn, raw)
    if record is None or record.revoked_at is not None:
        raise AuthError
    return Principal(account_id=record.account_id, token_id=record.id)
