"""Resolve a skill's source directory by name through the skill-checks catalog.

Tests key skills by name so moving a skill between domains never breaks them. The catalog
owns the lookup and fails when a name is missing or ambiguous.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


REPOSITORY_ROOT = _repository_root()
LOCATE_SCRIPT = REPOSITORY_ROOT / "src" / "tools" / "skill-checks" / "skill_checks.py"


def skill_directory(name: str) -> Path:
    """Return the source directory of the skill named `name`, or fail naming the skill."""
    result = subprocess.run(
        [sys.executable, str(LOCATE_SCRIPT), "locate", name],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise LookupError(f"cannot locate skill {name!r}: {result.stderr.strip()}")
    return Path(result.stdout.strip())
