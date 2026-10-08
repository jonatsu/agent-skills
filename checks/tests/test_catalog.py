"""Tests for skill discovery from the repository root."""

from collections.abc import Callable
from pathlib import Path

import pytest

from skill_checks.catalog import (
    InvalidSkillDirectories,
    SkillCatalogError,
    discover_skill_sources,
    find_skill_source,
)


def directories(root: Path) -> list[Path]:
    return [source.directory for source in discover_skill_sources(root)]


def test_discovery_covers_every_deployable_group(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    domain = write_skill("engineering/technical-design")
    nested = write_skill("lazy/development/python/python-style")
    claude = write_skill("claude/session-reflect")

    assert directories(tmp_path) == [claude, domain, nested]


@pytest.mark.parametrize(
    "excluded",
    [
        "archived/retired",
        "tests/fixture",
        "checks/tests/fixture",
        "review/example/evals/fixtures/x",
    ],
)
def test_discovery_skips_non_deployable_trees(
    tmp_path: Path, write_skill: Callable[[str], Path], excluded: str
) -> None:
    active = write_skill("engineering/active")
    write_skill(excluded)

    assert directories(tmp_path) == [active]


def test_explicit_names_bypass_the_exclusions(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    archived = write_skill("archived/retired")

    sources = discover_skill_sources(
        tmp_path, (Path("archived/retired"),), working_directory=tmp_path
    )

    assert [source.directory for source in sources] == [archived]


def test_explicit_names_report_every_invalid_entry(tmp_path: Path) -> None:
    with pytest.raises(InvalidSkillDirectories) as raised:
        discover_skill_sources(tmp_path, (Path("one"), Path("two")), working_directory=tmp_path)

    assert raised.value.missing_skill_files == (
        tmp_path / "one/SKILL.md",
        tmp_path / "two/SKILL.md",
    )


def test_an_empty_catalog_fails(tmp_path: Path) -> None:
    with pytest.raises(SkillCatalogError):
        discover_skill_sources(tmp_path)


def test_a_symlinked_skill_file_is_not_a_skill(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    active = write_skill("engineering/active")
    linked = tmp_path / "engineering/linked"
    linked.mkdir()
    (linked / "SKILL.md").symlink_to(active / "SKILL.md")

    assert directories(tmp_path) == [active]


def test_find_skill_source_returns_the_unique_match(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    example = write_skill("engineering/example")
    write_skill("review/sibling")

    assert find_skill_source(tmp_path, "example").directory == example


@pytest.mark.parametrize(("name", "message"), [("missing", "no skill named"), ("dup", "ambiguous")])
def test_find_skill_source_fails_on_a_missing_or_shared_name(
    tmp_path: Path, write_skill: Callable[[str], Path], name: str, message: str
) -> None:
    write_skill("engineering/dup")
    write_skill("lazy/review/dup")

    with pytest.raises(SkillCatalogError, match=message):
        find_skill_source(tmp_path, name)
