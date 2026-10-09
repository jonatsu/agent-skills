"""Planted references that the outside-reference check must reject or accept."""

from __future__ import annotations

from pathlib import Path

import pytest

from skill_checks.outside_references import check_packages


def make_package(root: Path, name: str, files: dict[str, str]) -> Path:
    package = root / "group" / name
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text(f"---\nname: {name}\n---\n", "utf-8")
    for relative, text in files.items():
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, "utf-8")
    return package


@pytest.mark.parametrize(
    ("relative", "text"),
    [
        ("references/a.md", "See [other](../../other/SKILL.md).\n"),
        ("references/a.md", "![diagram](../../../shared.png)\n"),
        ("references/a.md", "[ref]: ../../other/references/x.md\n"),
        ("references/a.md", "See [abs](/home/someone/repo/file.md).\n"),
        ("references/a.md", "See [home](~/repo/file.md).\n"),
        ("references/a.md", "See [url](file:///etc/hosts).\n"),
        ("scripts/run.py", "ROOT = Path(__file__).parent.parent.parent\n"),
        ("scripts/run.py", "ROOT = Path(__file__).resolve().parents[2]\n"),
        ("scripts/run.sh", 'source "$(dirname "$0")/../../other/lib.sh"\n'),
        ("scripts/run.py", 'LIB = HERE / "../../other/lib.py"\n'),
    ],
)
def test_a_reference_out_of_the_package_fails(tmp_path: Path, relative: str, text: str) -> None:
    make_package(tmp_path, "skill", {relative: text})

    assert len(check_packages((tmp_path,))) == 1


@pytest.mark.parametrize(
    ("relative", "text"),
    [
        ("references/a.md", "See [sibling](b.md) and [up](../SKILL.md#usage).\n"),
        ("references/a.md", "See [site](https://example.com/x) and [anchor](#top).\n"),
        ("references/a.md", "```\n[not a link](../../../x.md)\n```\n"),
        ("ATTRIBUTIONS.md", "Drew on docs/research/elsewhere/notes.md in another repository.\n"),
        ("scripts/run.py", "ROOT = Path(__file__).parent.parent\n"),
        ("scripts/run.py", 'DATA = HERE / "../references/data.md"\n'),
    ],
)
def test_a_reference_inside_the_package_or_plain_prose_passes(
    tmp_path: Path, relative: str, text: str
) -> None:
    make_package(tmp_path, "skill", {relative: text})

    assert check_packages((tmp_path,)) == ()
