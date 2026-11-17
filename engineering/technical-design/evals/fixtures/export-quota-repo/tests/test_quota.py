from datetime import UTC, datetime

import pytest

from exporter.log import ExportLog
from exporter.models import Account, Plan
from exporter.quota import FREE_MONTHLY_EXPORT_LIMIT, QuotaExceeded
from exporter.service import ExportService

MARCH = datetime(2026, 3, 10, 9, 0, tzinfo=UTC)
APRIL = datetime(2026, 4, 1, 0, 0, tzinfo=UTC)


def test_free_account_is_blocked_after_the_limit():
    service = ExportService(ExportLog())
    account = Account(id=1, plan=Plan.FREE)
    for _ in range(FREE_MONTHLY_EXPORT_LIMIT):
        service.request_export(account, MARCH)
    with pytest.raises(QuotaExceeded):
        service.request_export(account, MARCH)


def test_limit_resets_in_a_new_calendar_month():
    service = ExportService(ExportLog())
    account = Account(id=1, plan=Plan.FREE)
    for _ in range(FREE_MONTHLY_EXPORT_LIMIT):
        service.request_export(account, MARCH)
    assert service.request_export(account, APRIL)


def test_pro_account_is_not_limited():
    service = ExportService(ExportLog())
    account = Account(id=2, plan=Plan.PRO)
    for _ in range(FREE_MONTHLY_EXPORT_LIMIT + 1):
        service.request_export(account, MARCH)
