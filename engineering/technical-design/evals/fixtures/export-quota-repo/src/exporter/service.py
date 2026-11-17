"""Export request handling."""

import uuid
from datetime import datetime

from exporter.log import ExportLog
from exporter.models import Account, ExportRecord
from exporter.quota import check_quota


class ExportService:
    def __init__(self, log: ExportLog) -> None:
        self._log = log

    def request_export(self, account: Account, now: datetime) -> str:
        """Record an export request and return its identifier."""
        check_quota(account, self._log, now)
        record = ExportRecord(id=uuid.uuid4().hex, account_id=account.id, requested_at=now)
        self._log.add(record)
        return record.id
