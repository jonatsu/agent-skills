"""Tests for the specification and policy validator adapters."""

import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from skill_checks.catalog import discover_skill_sources
from skill_checks.validators import (
    CommandResult,
    ValidatorKind,
    format_validation_report,
    run_validator,
)


class RecordingRunner:
    def __init__(self, result: CommandResult) -> None:
        self.result = result
        self.calls: list[tuple[str, ...]] = []

    def run(self, arguments: Sequence[str], *, cwd: Path) -> CommandResult:
        self.calls.append(tuple(arguments))
        return self.result


@pytest.fixture
def tree(tmp_path: Path, write_skill: Callable[[str], Path]) -> Path:
    write_skill("engineering/example")
    forge = write_skill("skills-for-skills/skill-forge")
    (forge / "scripts").mkdir()
    (forge / "scripts/quick_validate.py").write_text("print('ok')\n", encoding="utf-8")
    return tmp_path


def test_policy_runs_skill_forges_validator_and_parses_its_findings(tree: Path) -> None:
    runner = RecordingRunner(CommandResult(1, "warning: long body\nerror: bad name\n"))
    sources = discover_skill_sources(tree)

    report = run_validator(ValidatorKind.POLICY, sources, tree, runner=runner)
    stdout, _ = format_validation_report(report, tree)

    assert runner.calls[0][:2] == (
        sys.executable,
        str(tree / "skills-for-skills/skill-forge/scripts/quick_validate.py"),
    )
    assert report.failures == 2
    assert report.warnings == 2
    assert "FAIL  engineering/example\n      bad name" in stdout


def test_specification_runs_agentskills_validate_and_keeps_its_output(tree: Path) -> None:
    runner = RecordingRunner(CommandResult(1, "Validation failed: name mismatch"))

    report = run_validator(
        ValidatorKind.SPECIFICATION, discover_skill_sources(tree), tree, runner=runner
    )

    assert Path(runner.calls[0][0]).name == "agentskills"
    assert runner.calls[0][1] == "validate"
    assert report.records[0].raw_failure == "Validation failed: name mismatch"


def test_a_missing_policy_validator_is_a_fatal_error(tree: Path) -> None:
    (tree / "skills-for-skills/skill-forge/scripts/quick_validate.py").unlink()

    report = run_validator(ValidatorKind.POLICY, discover_skill_sources(tree), tree)

    assert report.fatal_error is not None
    assert "quick_validate.py" in report.fatal_error


def test_a_runner_os_error_is_a_fatal_error(tree: Path) -> None:
    class FailingRunner:
        def run(self, arguments: Sequence[str], *, cwd: Path) -> CommandResult:
            raise OSError("boom")

    report = run_validator(
        ValidatorKind.POLICY, discover_skill_sources(tree), tree, runner=FailingRunner()
    )

    assert report.fatal_error == "cannot run validator: boom"
