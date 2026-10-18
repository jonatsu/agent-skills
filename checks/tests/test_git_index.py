"""Tree-wide discovery inside a Git work tree sees only the files Git tracks or has staged."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

from skill_checks.catalog import discover_skill_sources
from skill_checks.skill_tree import package_files, skill_packages


def git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)


def init_repository(root: Path) -> None:
    git(root, "init", "--quiet")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")


def test_discovery_skips_untracked_skills_and_keeps_staged_ones(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    init_repository(tmp_path)
    tracked = write_skill("engineering/tracked")
    staged = write_skill("engineering/staged")
    write_skill("engineering/untracked")
    git(tmp_path, "add", "engineering/tracked")
    git(tmp_path, "commit", "--quiet", "-m", "tracked")
    git(tmp_path, "add", "engineering/staged")

    found = [source.directory for source in discover_skill_sources(tmp_path)]

    assert found == [staged.resolve(), tracked.resolve()]
    assert skill_packages((tmp_path,)) == (
        tmp_path / "engineering/staged",
        tmp_path / "engineering/tracked",
    )


def test_package_files_skip_an_untracked_file_inside_a_tracked_package(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    init_repository(tmp_path)
    package = write_skill("engineering/skill")
    git(tmp_path, "add", ".")
    (package / "draft.md").write_text("Work in progress.\n", encoding="utf-8")

    assert list(package_files(package)) == [package / "SKILL.md"]
