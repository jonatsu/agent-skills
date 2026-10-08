"""Disposable skill-tree fixtures for the checks' tests."""

from collections.abc import Callable
from pathlib import Path

import pytest

SKILL_TEXT = "---\nname: fixture\ndescription: Fixture.\nlicense: MIT\n---\n"


@pytest.fixture
def write_skill(tmp_path: Path) -> Callable[[str], Path]:
    """Return a factory that creates a minimal skill directory under the fixture root."""

    def factory(relative: str) -> Path:
        directory = tmp_path / relative
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(SKILL_TEXT, encoding="utf-8")
        return directory

    return factory
