"""Tests for the duplicate-name and commit-identity checks."""

import os
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from skill_checks.catalog import discover_skill_sources
from skill_checks.cli import main
from skill_checks.identity import (
    NOREPLY_ADDRESS,
    IdentityError,
    wrong_identities,
    wrong_pushed_identities,
)
from skill_checks.names import duplicate_names


def test_two_packages_with_one_name_are_reported(
    tmp_path: Path, write_skill: Callable[[str], Path]
) -> None:
    first = write_skill("engineering/shared-name")
    second = write_skill("review/nested/shared-name")
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


def commit(message: str, email: str) -> str:
    environment = {"GIT_AUTHOR_EMAIL": email, "GIT_COMMITTER_EMAIL": email}
    subprocess.run(
        ["git", "commit", "-q", "--allow-empty", "--no-verify", "-m", message],
        check=True,
        env={**os.environ, **environment},
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, check=True, text=True
    ).stdout.strip()


def test_a_push_of_noreply_commits_passes(repository: Path) -> None:
    base = commit("base", NOREPLY_ADDRESS)
    tip = commit("next", NOREPLY_ADDRESS)

    assert wrong_pushed_identities(base, tip) == ()


def test_a_pushed_commit_under_another_address_fails(repository: Path) -> None:
    base = commit("base", NOREPLY_ADDRESS)
    commit("leak", "someone@example.com")
    tip = commit("next", NOREPLY_ADDRESS)

    problems = wrong_pushed_identities(base, tip)

    assert len(problems) == 1
    assert "another address" in problems[0]


def test_a_new_branch_push_checks_every_commit_no_remote_holds(repository: Path) -> None:
    commit("leak", "someone@example.com")
    tip = commit("next", NOREPLY_ADDRESS)

    assert len(wrong_pushed_identities("", tip)) == 1


def test_a_new_branch_push_skips_commits_that_remote_already_holds(repository: Path) -> None:
    commit("leak", "someone@example.com")
    subprocess.run(["git", "update-ref", "refs/remotes/probe/main", "HEAD"], check=True)
    tip = commit("next", NOREPLY_ADDRESS)

    assert wrong_pushed_identities("", tip, "probe") == ()
    assert len(wrong_pushed_identities("", tip, "other")) == 1


@pytest.mark.parametrize(("email", "status"), [(NOREPLY_ADDRESS, 0), ("someone@example.com", 1)])
def test_a_push_carrying_the_root_commit_is_checked_from_the_local_ref(
    repository: Path, monkeypatch: pytest.MonkeyPatch, email: str, status: int
) -> None:
    commit("root", email)
    # What pre-commit sets for a push that includes the root commit: no range, only the refs.
    for name in ("PRE_COMMIT_FROM_REF", "PRE_COMMIT_TO_REF"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PRE_COMMIT_LOCAL_BRANCH", "HEAD")
    monkeypatch.setenv("PRE_COMMIT_REMOTE_NAME", "origin")

    assert main(["pushed-identity"]) == status


def test_a_second_branch_in_the_same_push_is_checked(repository: Path) -> None:
    base = commit("base", NOREPLY_ADDRESS)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", base], check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "feature"], check=True)
    commit("leak", "someone@example.com")
    subprocess.run(["git", "checkout", "-q", "-"], check=True)
    tip = commit("next", NOREPLY_ADDRESS)

    # pre-commit names only the first ref, here main; the leak sits on feature.
    assert len(wrong_pushed_identities(base, tip, "origin")) == 1


def test_a_merged_commit_the_remote_already_holds_is_not_rechecked(repository: Path) -> None:
    base = commit("base", NOREPLY_ADDRESS)
    bot = commit("update", "bot@example.com")
    subprocess.run(["git", "update-ref", "refs/remotes/origin/update", bot], check=True)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", base], check=True)
    tip = commit("next", NOREPLY_ADDRESS)

    assert wrong_pushed_identities(base, tip, "origin") == ()
