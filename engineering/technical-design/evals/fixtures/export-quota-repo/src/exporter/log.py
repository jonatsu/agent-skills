"""In-memory log of export requests."""

from datetime import datetime

from exporter.models import ExportRecord


class ExportLog:
    def __init__(self) -> None:
        self._records: list[ExportRecord] = []

    def add(self, record: ExportRecord) -> None:
        self._records.append(record)

    def count_in_month(self, account_id: int, moment: datetime) -> int:
        """Count the account's requests in the calendar month (UTC) that contains `moment`."""
        return sum(
            1
            for record in self._records
            if record.account_id == account_id
            and (record.requested_at.year, record.requested_at.month) == (moment.year, moment.month)
        )
