"""Kasetto-compatible source-text checks for skill descriptions.

Kasetto records a folded or literal block scalar as its marker character rather than the text, so a
description must stay one inline scalar."""

import re
from pathlib import Path

import attrs

from skill_checks.catalog import SkillSource

SPEC_MAX = 1024
WARN_OVER = 512
DESCRIPTION_RE = re.compile(r"^description:[ \t]*(.*)$")


@attrs.frozen
class DescriptionFinding:
    """One failing or warning description finding."""

    source: SkillSource
    message: str
    is_warning: bool = False


@attrs.frozen
class DescriptionReport:
    """Complete deterministic description-check result."""

    checked: int
    findings: tuple[DescriptionFinding, ...]

    @property
    def failures(self) -> int:
        return sum(not finding.is_warning for finding in self.findings)

    @property
    def warnings(self) -> int:
        return sum(finding.is_warning for finding in self.findings)


def check_descriptions(sources: tuple[SkillSource, ...]) -> DescriptionReport:
    """Check description source form and length without decoding YAML scalar escapes."""
    findings: list[DescriptionFinding] = []
    for source in sources:
        finding = _check_description(source)
        if finding is not None:
            findings.append(finding)
    return DescriptionReport(len(sources), tuple(findings))


def _check_description(source: SkillSource) -> DescriptionFinding | None:
    try:
        text = source.skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return DescriptionFinding(source, f"cannot read description: {error}")
    raw_value = _description_source_value(text)
    if raw_value is None:
        return DescriptionFinding(source, "no description in frontmatter")
    if raw_value.startswith(("|", ">")):
        return DescriptionFinding(
            source,
            "description uses a block scalar; Kasetto records the marker, not the text",
        )
    if len(raw_value) > 1 and raw_value[0] == raw_value[-1] and raw_value[0] in {'"', "'"}:
        raw_value = raw_value[1:-1]
    length = len(raw_value)
    if length == 0:
        return DescriptionFinding(source, "description is present but empty")
    if length > SPEC_MAX:
        return DescriptionFinding(
            source,
            f"description is {length} characters, over the {SPEC_MAX} specification cap",
        )
    if length > WARN_OVER:
        return DescriptionFinding(
            source,
            f"description is {length} characters, over the {WARN_OVER} repository budget",
            is_warning=True,
        )
    return None


def _description_source_value(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    for line in lines[1:]:
        if line == "---":
            return None
        match = DESCRIPTION_RE.match(line)
        if match is not None:
            return match.group(1)
    return None


def format_description_report(report: DescriptionReport, repo_root: Path) -> str:
    """Render the legacy human-readable description report."""
    lines: list[str] = []
    for finding in report.findings:
        label = "warn" if finding.is_warning else "FAIL"
        lines.append(f"{label}  {_display_path(finding.source.skill_md, repo_root)}")
        lines.append(f"      {finding.message}")
    lines.append("")
    lines.append(
        f"{report.checked} checked, {report.failures} failed, {report.warnings} over budget"
    )
    return "\n".join(lines) + "\n"


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
