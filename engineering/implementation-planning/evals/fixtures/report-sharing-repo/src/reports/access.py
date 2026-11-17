"""Report access checks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Report:
    """A saved report and its owner."""

    id: str
    owner_id: str
    title: str


def can_view(report: Report, user_id: str) -> bool:
    """Return True when the user may view the report. Today only the owner may."""
    return report.owner_id == user_id
