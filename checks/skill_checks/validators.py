"""Adapters for the two authoritative skill validators.

The specification validator is `skills-ref` from PyPI, pinned in this project's lockfile, whose command is
`agentskills validate`. The policy validator is skill-forge's own `scripts/quick_validate.py`. Running a script
from inside a sibling package is allowed here because both ship at the same commit of this repository.
"""

from __future__ import annotations

import enum
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final, Protocol

import attrs

from skill_checks.catalog import SkillCatalogError, SkillSource, find_skill_source

SPECIFICATION_COMMAND: Final = "agentskills"
POLICY_SKILL: Final = "skill-forge"
POLICY_SCRIPT: Final = Path("scripts") / "quick_validate.py"


class ValidatorKind(enum.Enum):
    """The independent validation authorities exposed by the tool."""

    SPECIFICATION = "spec"
    POLICY = "policy"


@attrs.frozen
class CommandResult:
    """Captured output from one validator process."""

    returncode: int
    output: str


class ValidatorRunner(Protocol):
    """Subprocess boundary used by validator orchestration."""

    def run(self, arguments: Sequence[str], *, cwd: Path) -> CommandResult: ...


class SubprocessValidatorRunner:
    """Run validators without a shell and merge their diagnostic streams."""

    def run(self, arguments: Sequence[str], *, cwd: Path) -> CommandResult:
        completed = subprocess.run(
            list(arguments),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return CommandResult(completed.returncode, completed.stdout)


@attrs.frozen
class ValidationRecord:
    """One skill's parsed validator outcome."""

    source: SkillSource
    returncode: int
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    raw_failure: str | None = None

    @property
    def has_failed(self) -> bool:
        return self.returncode != 0 or bool(self.errors)


@attrs.frozen
class ValidationReport:
    """Complete result from one validation authority."""

    kind: ValidatorKind
    records: tuple[ValidationRecord, ...]
    fatal_error: str | None = None

    @property
    def checked(self) -> int:
        return len(self.records)

    @property
    def failures(self) -> int:
        return sum(record.has_failed for record in self.records)

    @property
    def warnings(self) -> int:
        return sum(len(record.warnings) for record in self.records)


def run_validator(
    kind: ValidatorKind,
    sources: tuple[SkillSource, ...],
    repo_root: Path,
    *,
    runner: ValidatorRunner | None = None,
) -> ValidationReport:
    """Run one authority over every source in deterministic order."""
    command_runner = runner or SubprocessValidatorRunner()
    try:
        prefix = _command_prefix(kind, repo_root)
    except (SkillCatalogError, FileNotFoundError) as error:
        return ValidationReport(kind, (), str(error))
    records: list[ValidationRecord] = []
    for source in sources:
        try:
            result = command_runner.run((*prefix, str(source.directory)), cwd=repo_root)
        except OSError as error:
            return ValidationReport(kind, tuple(records), f"cannot run validator: {error}")
        records.append(_parse_result(kind, source, result))
    return ValidationReport(kind, tuple(records))


def _command_prefix(kind: ValidatorKind, repo_root: Path) -> tuple[str, ...]:
    """Return the command that validates one skill directory appended to it.

    Raises:
        SkillCatalogError: If skill-forge cannot be located.
        FileNotFoundError: If a validator is not installed or not where it belongs.
    """
    if kind is ValidatorKind.POLICY:
        script = find_skill_source(repo_root, POLICY_SKILL).directory / POLICY_SCRIPT
        if not script.is_file():
            raise FileNotFoundError(f"policy validator not found; looked for: {script}")
        return (sys.executable, str(script))
    # The command sits beside the running interpreter in the project environment.
    command = shutil.which(SPECIFICATION_COMMAND, path=str(Path(sys.executable).parent))
    if command is None:
        raise FileNotFoundError(
            f"specification validator {SPECIFICATION_COMMAND!r} not found beside {sys.executable}; "
            "run uv sync"
        )
    return (command, "validate")


def _parse_result(
    kind: ValidatorKind, source: SkillSource, result: CommandResult
) -> ValidationRecord:
    if kind is ValidatorKind.SPECIFICATION:
        return ValidationRecord(
            source,
            result.returncode,
            raw_failure=result.output.strip() if result.returncode else None,
        )
    errors: list[str] = []
    warnings: list[str] = []
    for line in result.output.splitlines():
        if line.startswith("error:"):
            errors.append(line.removeprefix("error:").strip())
        elif line.startswith("warning:"):
            warnings.append(line.removeprefix("warning:").strip())
    raw_failure = result.output.strip() if result.returncode and not errors else None
    return ValidationRecord(
        source,
        result.returncode,
        errors=tuple(errors),
        warnings=tuple(warnings),
        raw_failure=raw_failure,
    )


def format_validation_report(report: ValidationReport, repo_root: Path) -> tuple[str, str]:
    """Return the stdout and stderr payloads for one validator report."""
    if report.fatal_error is not None:
        label = "skill-forge policy" if report.kind is ValidatorKind.POLICY else "specification"
        return "", f"FAIL  {label} validator unavailable\n      {report.fatal_error}\n"
    heading = (
        "Skill Forge local policy (quick_validate)"
        if report.kind is ValidatorKind.POLICY
        else "Agent Skills specification (skills-ref)"
    )
    lines = [heading]
    for record in report.records:
        relative = _display_path(record.source.directory, repo_root)
        for warning in record.warnings:
            lines.extend((f"warn  {relative}", f"      {warning}"))
        for error in record.errors:
            lines.extend((f"FAIL  {relative}", f"      {error}"))
        if record.raw_failure is not None:
            lines.extend((f"FAIL  {relative}", f"      {record.raw_failure}"))
    lines.append("")
    if report.kind is ValidatorKind.POLICY:
        lines.append(
            f"{report.checked} checked, {report.failures} failed, {report.warnings} with warnings"
        )
    else:
        lines.append(f"{report.checked} checked, {report.failures} failed")
    return "\n".join(lines) + "\n", ""


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
