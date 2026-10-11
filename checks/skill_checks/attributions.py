"""Structural checks for a skill's ATTRIBUTIONS.md against the scheme in skill-forge's provenance reference.

The scheme keeps the file a list of sources: a header naming the author and license, first-party and
third-party source sections whose entries each carry Source, License, and Version bullets, and an optional
upstream license notice. The checks catch the shapes a work ledger takes, such as extra sections and file
checksums; whether the prose narrates past work stays a review judgment."""

import re
from pathlib import Path

import attrs

from skill_checks.catalog import SkillSource

ATTRIBUTIONS_FILE = "ATTRIBUTIONS.md"
FIRST_PARTY = "First-party Sources"
THIRD_PARTY = "Third-party Sources"
NOTICE = "Upstream License Notice"
SECTION_ORDER = (FIRST_PARTY, THIRD_PARTY, NOTICE)
SOURCE_SECTIONS = frozenset({FIRST_PARTY, THIRD_PARTY})
ENTRY_FIELDS = ("Source", "License", "Version")

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*$")
FIELD_RE = re.compile(r"^- (Author|Source|License|Version):[ \t]*(.*)$")
LICENSE_VALUE_RE = re.compile(r"^`([^`]+)`$")
LICENSE_TOKEN_RE = re.compile(r"\(|\)|[A-Za-z0-9][A-Za-z0-9.+-]*")
LICENSE_OPERATORS = frozenset({"AND", "OR", "WITH"})
SHA256_RE = re.compile(r"\b[0-9a-fA-F]{64}\b")
FENCE_RE = re.compile(r"^(```|~~~)")


@attrs.frozen
class AttributionFinding:
    """One way an ATTRIBUTIONS.md departs from the scheme."""

    path: Path
    line: int
    message: str


@attrs.frozen
class AttributionReport:
    """Complete deterministic attributions-check result."""

    checked: int
    findings: tuple[AttributionFinding, ...]


@attrs.define
class _Entry:
    heading_line: int
    fields: dict[str, tuple[int, str]] = attrs.field(factory=dict)


def check_attributions(sources: tuple[SkillSource, ...]) -> AttributionReport:
    """Check every skill that ships an ATTRIBUTIONS.md; a skill without one is not checked."""
    findings: list[AttributionFinding] = []
    checked = 0
    for source in sources:
        path = source.directory / ATTRIBUTIONS_FILE
        if not path.is_file():
            continue
        checked += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(AttributionFinding(path, 0, f"cannot read: {error}"))
            continue
        findings.extend(check_attribution_text(path, text))
    return AttributionReport(checked, tuple(findings))


def check_attribution_text(path: Path, text: str) -> list[AttributionFinding]:
    """Return every departure from the scheme in one file's text."""
    findings: list[AttributionFinding] = []

    def fail(line: int, message: str) -> None:
        findings.append(AttributionFinding(path, line, message))

    lines = _unfenced_lines(text)
    if not lines or lines[0] != (1, "# Attributions"):
        fail(1, "the first line must be '# Attributions'")

    header: dict[str, tuple[int, str]] = {}
    section: str | None = None
    seen_sections: list[str] = []
    entries: list[_Entry] = []
    entry: _Entry | None = None

    for number, line in lines[1:]:
        if SHA256_RE.search(line):
            fail(number, "a SHA-256 checksum; file hashes do not belong in attributions")
        heading = HEADING_RE.match(line)
        if heading is not None:
            level, title = len(heading.group(1)), heading.group(2)
            if level == 1:
                fail(number, "a second level-one heading")
            elif level == 2:
                entry = None
                section = title
                if title not in SECTION_ORDER:
                    fail(number, f"section '{title}' is not one of: {', '.join(SECTION_ORDER)}")
                elif title in seen_sections:
                    fail(number, f"section '{title}' appears twice")
                else:
                    if seen_sections and SECTION_ORDER.index(title) < SECTION_ORDER.index(
                        seen_sections[-1]
                    ):
                        fail(
                            number,
                            f"section '{title}' is out of order; use {', '.join(SECTION_ORDER)}",
                        )
                    seen_sections.append(title)
            elif level == 3 and section in SOURCE_SECTIONS:
                entry = _Entry(number)
                entries.append(entry)
            elif section in SOURCE_SECTIONS:
                fail(number, "a heading below the source-entry level")
            else:
                fail(number, f"a level-{level} heading outside a source section")
            continue
        field = FIELD_RE.match(line)
        if field is None:
            continue
        name, value = field.group(1), field.group(2)
        target = header if section is None else entry.fields if entry is not None else None
        if target is not None and name not in target:
            target[name] = (number, value)

    for name in ("Author", "License"):
        if name not in header:
            fail(1, f"the header lacks '- {name}:'")
    if "License" in header:
        findings.extend(_license_findings(path, *header["License"]))

    for item in entries:
        for name in ENTRY_FIELDS:
            if name not in item.fields:
                fail(item.heading_line, f"the entry lacks '- {name}:'")
        if "License" in item.fields:
            findings.extend(_license_findings(path, *item.fields["License"]))

    if not any(title in SOURCE_SECTIONS for title in seen_sections):
        fail(1, f"no '{FIRST_PARTY}' or '{THIRD_PARTY}' section")
    return findings


def _license_findings(path: Path, line: int, value: str) -> list[AttributionFinding]:
    match = LICENSE_VALUE_RE.match(value.strip())
    if match is None:
        return [
            AttributionFinding(path, line, "a license must be one SPDX expression in backticks")
        ]
    expression = match.group(1)
    leftover = LICENSE_TOKEN_RE.sub("", expression).strip()
    tokens = LICENSE_TOKEN_RE.findall(expression)
    identifiers = [
        token for token in tokens if token not in LICENSE_OPERATORS and token not in "()"
    ]
    if leftover or not identifiers:
        return [AttributionFinding(path, line, f"'{expression}' is not an SPDX license expression")]
    return []


def _unfenced_lines(text: str) -> list[tuple[int, str]]:
    """Number the lines outside fenced code blocks, so example Markdown cannot fake a heading."""
    kept: list[tuple[int, str]] = []
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            kept.append((number, line))
    return kept


def format_attribution_report(report: AttributionReport, repo_root: Path) -> str:
    """Render one line per finding, then the totals."""
    lines = [
        f"FAIL  {_display_path(finding.path, repo_root)}:{finding.line}: {finding.message}"
        for finding in report.findings
    ]
    failed = len({finding.path for finding in report.findings})
    lines.append("")
    lines.append(f"{report.checked} checked, {failed} failed")
    return "\n".join(lines) + "\n"


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
