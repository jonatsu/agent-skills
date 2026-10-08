"""Fail when two deployable skills share a name.

Kasetto deploys every skill flat into an agent's skills directory, so two packages with one name collide: the
last one wins silently, or two locks prune each other's copy. Names must be unique across every deployable group.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from skill_checks.catalog import SkillSource


def duplicate_names(sources: tuple[SkillSource, ...]) -> dict[str, tuple[Path, ...]]:
    """Return each skill name used by more than one package, with every directory using it."""
    by_name: dict[str, list[Path]] = defaultdict(list)
    for source in sources:
        by_name[source.directory.name].append(source.directory)
    return {name: tuple(paths) for name, paths in sorted(by_name.items()) if len(paths) > 1}
