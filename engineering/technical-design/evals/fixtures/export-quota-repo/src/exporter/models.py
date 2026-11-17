"""Plain data types shared across the exporter."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Plan(Enum):
    FREE = "free"
    PRO = "pro"


@dataclass(frozen=True)
class Account:
    id: int
    plan: Plan


@dataclass(frozen=True)
class ExportRecord:
    id: str
    account_id: int
    requested_at: datetime
