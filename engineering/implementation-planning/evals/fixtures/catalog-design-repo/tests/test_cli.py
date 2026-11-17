from catalog.cli import main


def test_stub_reports_not_implemented() -> None:
    assert main(["examples/catalog.json"]) == 3
