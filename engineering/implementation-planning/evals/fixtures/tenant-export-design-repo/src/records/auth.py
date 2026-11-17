"""Caller identity and role checks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Caller:
    """The authenticated user making a request."""

    user_id: str
    tenant_id: str
    roles: frozenset[str]


def is_admin(caller: Caller) -> bool:
    """Return True when the caller administers their own tenant."""
    return "admin" in caller.roles
