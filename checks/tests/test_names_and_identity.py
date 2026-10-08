"""Tests for the duplicate-name and commit-identity checks."""

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from skill_checks.catalog import discover_skill_sources
from skill_checks.identity import NOREPLY_ADDRESS, IdentityError, wrong_identities
from skill_checks.names import duplicate_names


def test_two_packages_with_one_name_are_reported(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    first = write_skill("engineering/shared-name")
    second = write_skill("lazy/review/shared-name")
    write_skill("review/unique")

    assert duplicate_names(discover_skill_sources(tmp_path)) == {"shared-name": (first, second)}


@pytest.fixture
def repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    monkeypatch.chdir(tmp_path)
    for variable in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL", "EMAIL"):
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "no-global-config"))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    subprocess.run(["git", "config", "user.name", "Fixture"], check=True)
    return tmp_path


def test_the_noreply_identity_passes(repository: Path) -> None:
    subprocess.run(["git", "config", "user.email", NOREPLY_ADDRESS], check=True)

    assert wrong_identities() == ()


def test_another_address_fails_for_each_role(repository: Path) -> None:
    subprocess.run(["git", "config", "user.email", "someone@example.com"], check=True)

    assert len(wrong_identities()) == 2


def test_an_author_override_alone_is_caught(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    subprocess.run(["git", "config", "user.email", NOREPLY_ADDRESS], check=True)
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "someone@example.com")

    assert wrong_identities() == (f"GIT_AUTHOR_IDENT uses another address than {NOREPLY_ADDRESS}",)


def test_no_configured_identity_is_an_error(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    subprocess.run(["git", "config", "--unset", "user.name"], check=True)
    monkeypatch.setenv("GIT_AUTHOR_NAME", "")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "")

    with pytest.raises(IdentityError):
        wrong_identities()
