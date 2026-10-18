"""Limit tree-wide discovery to the files Git tracks or has staged.

Sessions share one working tree, so untracked work in progress belongs to whoever is still writing it. A
commit can only contain indexed files, so the checks judge those and leave the rest alone.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def indexed_files(directory: Path) -> frozenset[Path] | None:
    """Return the resolved paths under `directory` that are in Git's index.

    Returns:
        The tracked and staged files, including tracked files deleted from disk, or `None` when `directory` is
        not inside a Git work tree, in which case callers walk the filesystem instead.
    """
    directory = directory.resolve()
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached"],
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        return None
    names = completed.stdout.decode("utf-8").split("\0")
    return frozenset(directory / name for name in names if name)


def candidate_files(directory: Path, pattern: str) -> list[Path]:
    """Return the files under `directory` whose name matches `pattern`, sorted, limited to Git's index.

    Paths keep the form `directory` was given in. Outside a Git work tree, every matching file on disk is a
    candidate.
    """
    resolved = directory.resolve()
    indexed = indexed_files(resolved)
    if indexed is None:
        return sorted(directory.rglob(pattern))
    return sorted(
        directory / path.relative_to(resolved)
        for path in indexed
        if path.match(pattern) and path.exists()
    )
