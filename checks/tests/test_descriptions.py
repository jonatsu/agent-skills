"""Tests for source-text description policy."""

from pathlib import Path

import pytest

from skill_checks.catalog import SkillSource
from skill_checks.descriptions import check_descriptions, format_description_report


def source(tmp_path: Path, value: str | None, *, raw: bytes | None = None) -> SkillSource:
    directory = tmp_path / "domain/example"
    directory.mkdir(parents=True)
    skill_md = directory / "SKILL.md"
    if raw is not None:
        skill_md.write_bytes(raw)
    else:
        description = "" if value is None else f"description: {value}\n"
        skill_md.write_text(f"---\nname: example\n{description}---\n", encoding="utf-8")
    return SkillSource(directory, skill_md)


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (None, "no description"),
        ("", "present but empty"),
        (">-\n  folded", "block scalar"),
        ("|\n  literal", "block scalar"),
        ("x" * 1025, "1025 characters"),
    ],
)
def test_failing_description_forms(tmp_path: Path, value: str | None, message: str) -> None:
    report = check_descriptions((source(tmp_path, value),))

    assert report.failures == 1
    assert message in report.findings[0].message


def test_escaped_value_counts_source_characters(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, '"' + "x" * 511 + '\\n"'),))

    assert report.failures == 0
    assert report.warnings == 1
    assert "513 characters" in report.findings[0].message
    assert "repository budget" in report.findings[0].message


def test_multiline_quote_counts_only_the_physical_description_line(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, '"' + "x" * 512 + '\ncontinued"'),))

    assert report.warnings == 1
    assert "513 characters" in report.findings[0].message


def test_unicode_counts_characters_not_utf8_bytes(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, '"' + "ä" * 513 + '"'),))

    assert "513 characters" in report.findings[0].message


def test_description_on_the_first_frontmatter_line_is_found(tmp_path: Path) -> None:
    skill = source(
        tmp_path, None, raw=b"---\ndescription: " + b"x" * 513 + b"\nname: example\n---\n"
    )

    report = check_descriptions((skill,))

    assert report.failures == 0
    assert "513 characters" in report.findings[0].message


def test_unreadable_utf8_is_a_failure(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, None, raw=b"\xff"),))

    assert report.failures == 1
    assert "cannot read description" in report.findings[0].message


def test_report_preserves_legacy_labels_and_summary(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, "x" * 513),))

    text = format_description_report(report, tmp_path)

    assert text.startswith("warn  domain/example/SKILL.md\n")
    assert text.endswith("1 checked, 0 failed, 1 over budget\n")


def test_report_labels_a_failure_as_fail(tmp_path: Path) -> None:
    report = check_descriptions((source(tmp_path, None),))

    text = format_description_report(report, tmp_path)

    assert text.startswith("FAIL  domain/example/SKILL.md\n")
