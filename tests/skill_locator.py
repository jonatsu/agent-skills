"""Resolve a skill's source directory by name through the repository's skill catalog.

Tests key skills by name so moving a skill between domains never breaks them. The catalog owns the lookup and
fails when a name is missing or ambiguous.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from skill_checks.catalog import SkillCatalogError, find_skill_source


def _repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


REPOSITORY_ROOT = _repository_root()


def skill_directory(name: str) -> Path:
    """Return the source directory of the skill named `name`, or fail naming the skill."""
    try:
        return find_skill_source(REPOSITORY_ROOT, name).directory
    except SkillCatalogError as error:
        raise LookupError(f"cannot locate skill {name!r}: {error}") from error
