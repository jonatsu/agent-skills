"""Plain data types shared across the dashboard."""

from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    VIEWER = "viewer"
    ADMIN = "admin"


@dataclass(frozen=True)
class Principal:
    """The signed-in caller. `tenant_id` is fixed at sign-in and never taken from a request."""

    user_id: int
    tenant_id: int
    role: Role


@dataclass(frozen=True)
class Record:
    id: int
    tenant_id: int
    status: str
    created_on: str
    name: str


@dataclass(frozen=True)
class Filters:
    status: str | None = None
    created_from: str | None = None
    created_to: str | None = None
