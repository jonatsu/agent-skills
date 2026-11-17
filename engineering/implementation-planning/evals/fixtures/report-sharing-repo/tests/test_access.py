from reports.access import Report, can_view


def test_only_owner_can_view() -> None:
    report = Report("r1", "u1", "Weekly")
    assert can_view(report, "u1")
    assert not can_view(report, "u2")
