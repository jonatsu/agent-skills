"""Copy new and changed files from a source folder to a destination folder."""

import shutil
from pathlib import Path


def sync(source: Path, destination: Path) -> list[Path]:
    """Copy each file that is missing or older in the destination; return the copied paths."""
    copied = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        target = destination / path.relative_to(source)
        if target.exists() and target.stat().st_mtime >= path.stat().st_mtime:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(target)
    return copied
