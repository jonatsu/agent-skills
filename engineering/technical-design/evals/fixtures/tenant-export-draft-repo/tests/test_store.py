from dashboard.models import Filters, Principal, Record, Role
from dashboard.store import RecordStore

RECORDS = [
    Record(1, 10, "open", "2026-09-01", "alpha"),
    Record(2, 10, "closed", "2026-09-05", "beta"),
    Record(3, 20, "open", "2026-09-02", "gamma"),
]


def test_query_returns_only_the_callers_tenant():
    store = RecordStore(RECORDS)
    admin = Principal(user_id=1, tenant_id=10, role=Role.ADMIN)
    assert [r.id for r in store.query(admin, Filters())] == [1, 2]


def test_filters_narrow_within_the_tenant():
    store = RecordStore(RECORDS)
    admin = Principal(user_id=1, tenant_id=10, role=Role.ADMIN)
    assert [r.id for r in store.query(admin, Filters(status="open"))] == [1]


def test_other_tenant_records_never_match():
    store = RecordStore(RECORDS)
    other = Principal(user_id=2, tenant_id=20, role=Role.VIEWER)
    assert [r.id for r in store.query(other, Filters(status="closed"))] == []
