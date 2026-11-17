from pathlib import Path

import pytest

from auditlog.cli import main


def test_prints_events(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    log = tmp_path / "audit.jsonl"
    log.write_text(
        '{"timestamp": "2026-03-01T10:00:00Z", "actor": "ops-1", "action": "login"}\n',
        encoding="utf-8",
    )
    assert main([str(log)]) == 0
    assert capsys.readouterr().out == "2026-03-01T10:00:00Z ops-1 login\n"
