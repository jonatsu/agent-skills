"""Fail before any identity other than the published noreply address is committed or pushed.

The repository is public, and its history carries only the GitHub noreply address. A clone whose Git config
falls back to another address would publish it. `wrong_identities` runs as a pre-commit hook and reads the
identity Git is about to record. `wrong_pushed_identities` runs as a pre-push hook and reads every commit being
pushed, which also covers commits made where the pre-commit hook does not run: a rebase, a cherry-pick, an
amend with `--no-verify`, or a clone that never installed the hooks.
"""

from __future__ import annotations

import re
import subprocess
from typing import Final

NOREPLY_ADDRESS: Final = "284267409+jonatsu@users.noreply.github.com"
IDENTITY_ROLES: Final = ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT")
ADDRESS = re.compile(r"<([^>]*)>")


class IdentityError(Exception):
    """Git cannot report the identity it would record."""


def wrong_identities() -> tuple[str, ...]:
    """Return a message for each commit role whose address is not the noreply address.

    Raises:
        IdentityError: If Git cannot report an identity, for example because none is configured.
    """
    problems: list[str] = []
    for role in IDENTITY_ROLES:
        result = subprocess.run(["git", "var", role], capture_output=True, text=True, check=False)
        match = ADDRESS.search(result.stdout)
        if result.returncode != 0 or match is None:
            raise IdentityError(f"git var {role} failed: {result.stderr.strip()}")
        if match.group(1) != NOREPLY_ADDRESS:
            problems.append(f"{role} uses another address than {NOREPLY_ADDRESS}")
    return tuple(problems)


def wrong_pushed_identities(from_ref: str, to_ref: str) -> tuple[str, ...]:
    """Return a message for each commit in a push whose author or committer is not the noreply address.

    `from_ref` is the remote's current commit, or empty when the push creates the branch; then every commit
    reachable from `to_ref` that no remote-tracking ref already holds is checked.

    Raises:
        IdentityError: If Git cannot list the pushed commits.
    """
    revisions = [f"{from_ref}..{to_ref}"] if from_ref else [to_ref, "--not", "--remotes"]
    result = subprocess.run(
        ["git", "log", "--format=%h %ae %ce", *revisions],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise IdentityError(f"cannot list the pushed commits: {result.stderr.strip()}")
    problems: list[str] = []
    for line in result.stdout.splitlines():
        commit, author, committer = line.split(" ", 2)
        if author != NOREPLY_ADDRESS or committer != NOREPLY_ADDRESS:
            problems.append(f"commit {commit} carries another address than {NOREPLY_ADDRESS}")
    return tuple(problems)
