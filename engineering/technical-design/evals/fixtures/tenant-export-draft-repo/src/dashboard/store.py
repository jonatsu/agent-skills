"""Tenant-scoped access to records."""

from dashboard.models import Filters, Principal, Record


class RecordStore:
    """Holds records for all tenants and returns only those of the caller's tenant."""

    def __init__(self, records: list[Record]) -> None:
        self._records = records

    def query(self, principal: Principal, filters: Filters) -> list[Record]:
        """Return the principal's tenant records that match the filters, ordered by id."""
        matches = [r for r in self._records if r.tenant_id == principal.tenant_id]
        if filters.status is not None:
            matches = [r for r in matches if r.status == filters.status]
        if filters.created_from is not None:
            matches = [r for r in matches if r.created_on >= filters.created_from]
        if filters.created_to is not None:
            matches = [r for r in matches if r.created_on <= filters.created_to]
        return sorted(matches, key=lambda r: r.id)
