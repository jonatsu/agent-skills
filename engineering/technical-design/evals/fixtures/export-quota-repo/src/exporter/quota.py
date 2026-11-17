"""Monthly export limit by plan."""

from datetime import datetime

from exporter.log import ExportLog
from exporter.models import Account, Plan

FREE_MONTHLY_EXPORT_LIMIT = 100


class QuotaExceeded(Exception):
    def __init__(self, limit: int) -> None:
        super().__init__(f"monthly export limit of {limit} reached")
        self.limit = limit


def check_quota(account: Account, log: ExportLog, now: datetime) -> None:
    """Raise `QuotaExceeded` when a free account has used its exports for the current month."""
    if account.plan is not Plan.FREE:
        return
    if log.count_in_month(account.id, now) >= FREE_MONTHLY_EXPORT_LIMIT:
        raise QuotaExceeded(FREE_MONTHLY_EXPORT_LIMIT)
