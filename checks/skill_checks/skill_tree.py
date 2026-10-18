"""Find skill packages and their files under a skills tree."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from pathlib import Path

from skill_checks.git_index import candidate_files

SKILL_FILE_NAME = "SKILL.md"
# Directories never holding packages to check: version control and tool caches.
IGNORED_DIRECTORY_NAMES = frozenset(
    {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
)
# Top-level directories that hold this tooling and its tests rather than skill packages, and `.scratch`, where
# sessions keep untracked working copies such as third-party skills under evaluation.
NON_SKILL_TOP_LEVEL = frozenset({"checks", "tests", ".github", ".scratch"})


def skill_packages(roots: Sequence[Path]) -> tuple[Path, ...]:
    """Return every directory under `roots` that holds a `SKILL.md`, outermost first.

    A package nested inside another package is not a separate package: its files belong to the outer one.
    """
    found: list[Path] = []
    for root in roots:
        for skill_file in candidate_files(root, SKILL_FILE_NAME):
            package = skill_file.parent
            relative = package.relative_to(root).parts
            if _is_ignored(package, root) or relative[:1] and relative[0] in NON_SKILL_TOP_LEVEL:
                continue
            if any(package.is_relative_to(outer) for outer in found):
                continue
            found.append(package)
    return tuple(found)


def package_files(package: Path) -> Iterator[Path]:
    """Yield every regular file inside one package that Git tracks or has staged, in a stable order."""
    for path in candidate_files(package, "*"):
        if path.is_file() and not path.is_symlink() and not _is_ignored(path, package):
            yield path


def _is_ignored(path: Path, root: Path) -> bool:
    return any(part in IGNORED_DIRECTORY_NAMES for part in path.relative_to(root).parts)
