"""Fail before a commit records any identity other than the published noreply address.

The repository is public, and its history carries only the GitHub noreply address. A clone whose Git config
falls back to another address would publish it in the next commit; this check runs as a pre-commit hook and
reads the identity Git is about to record.
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
