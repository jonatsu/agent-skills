"""Tests for the ATTRIBUTIONS.md structure check."""

from pathlib import Path

import pytest

from skill_checks.attributions import check_attribution_text, check_attributions
from skill_checks.catalog import SkillSource

VALID = """\
# Attributions

- Author: Example Author
- License: `MIT`

## First-party Sources

### Example Project — Example manual

- Source: <https://example.com/manual>
- License: `GPL-2.0-or-later`
- Version: `v1.0`

The guidance is built on the manual. No prose is copied.

## Third-party Sources

### Someone — Some deck

- Source: <https://example.com/deck>
- License: `CC-BY-SA-3.0`
- Version: slides dated 2020-10-26

Formerly adapted: earlier revisions followed this deck's order.

## Upstream License Notice

Copyright Example.
"""


def messages(text: str) -> list[str]:
    return [finding.message for finding in check_attribution_text(Path("ATTRIBUTIONS.md"), text)]


def test_the_scheme_passes() -> None:
    assert messages(VALID) == []


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("# Attributions", "# Attribution notes", "first line"),
        ("- Author: Example Author\n", "", "lacks '- Author:'"),
        ("## Third-party Sources", "## Third-Party Cases Used During the Repair", "is not one of"),
        ("## Upstream License Notice", "## First-party Sources", "appears twice"),
        ("- Version: `v1.0`\n", "", "lacks '- Version:'"),
        ("- License: `CC-BY-SA-3.0`", "- License: CC BY-SA 3.0", "in backticks"),
        ("- License: `CC-BY-SA-3.0`", "- License: `CC BY-SA 3.0, see notes`", "not an SPDX"),
        ("Copyright Example.", "#### Detail", "outside a source section"),
        ("No prose is copied.", "SHA-256: " + "ab" * 32, "SHA-256"),
    ],
)
def test_departures_from_the_scheme_fail(old: str, new: str, message: str) -> None:
    assert old in VALID
    found = messages(VALID.replace(old, new, 1))

    assert any(message in text for text in found), found


def test_sections_out_of_order_fail() -> None:
    first, rest = VALID.split("## Third-party Sources", 1)
    third, notice = rest.split("## Upstream License Notice", 1)
    reordered = first.replace(
        "## First-party Sources", "## Third-party Sources" + third + "## First-party Sources"
    )

    assert any(
        "out of order" in text
        for text in messages(reordered + "## Upstream License Notice" + notice)
    )


def test_spdx_expressions_pass() -> None:
    text = VALID.replace("`GPL-2.0-or-later`", "`(MIT OR Apache-2.0) AND LicenseRef-Linux-Lab`")

    assert messages(text) == []


def test_fenced_markdown_is_not_structure() -> None:
    text = VALID.replace("Copyright Example.", "```markdown\n## Not a section\n```")

    assert messages(text) == []


def test_skills_without_attributions_are_not_checked(tmp_path: Path) -> None:
    with_file = tmp_path / "domain/with"
    without = tmp_path / "domain/without"
    for directory in (with_file, without):
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
    (with_file / "ATTRIBUTIONS.md").write_text(VALID, encoding="utf-8")

    report = check_attributions(
        (SkillSource(with_file, with_file / "SKILL.md"), SkillSource(without, without / "SKILL.md"))
    )

    assert report.checked == 1
    assert report.findings == ()
