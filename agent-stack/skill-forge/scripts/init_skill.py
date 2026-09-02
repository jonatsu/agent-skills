#!/usr/bin/env python3
"""Create a minimal, provenance-aware Agent Skill scaffold."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def discover_author():
    """Return the Git-configured author without inventing a fallback identity."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def render_skill(skill_name, author, license_id, scope, repository):
    """Return a minimal scaffold for the selected portability scope."""
    metadata = f"  author: {author}\n"
    opening = "[TODO: State the skill's purpose and essential instructions.]"
    if scope == "repo-local":
        metadata += "  scope: repo-local\n"
        opening = (
            f"This skill serves the {repository} repository.\n\n"
            "[TODO: State its purpose and essential instructions.]"
        )

    title = " ".join(word.capitalize() for word in skill_name.split("-"))
    return f"""---
name: {skill_name}
description: "[TODO: State what the skill does and when to use it.]"
license: {license_id}
metadata:
{metadata}---

# {title}

{opening}

## Before Delivery

- [ ] Replace every scaffold placeholder.
- [ ] Run `skills-ref validate` and the target repository's applicable checks.
"""


def init_skill(skill_name, path, author, license_id, scope, repository=None):
    """Create the skill directory and SKILL.md, returning its path on success."""
    if not NAME_RE.fullmatch(skill_name) or len(skill_name) > 64:
        print(
            "Error: skill name must be 1-64 lowercase letters, digits, and single "
            "hyphens, with no leading or trailing hyphen.",
            file=sys.stderr,
        )
        return None
    if scope == "repo-local" and not repository:
        print(
            "Error: --repository is required with --scope repo-local.", file=sys.stderr
        )
        return None

    skill_dir = Path(path).resolve() / skill_name
    if skill_dir.exists():
        print(f"Error: skill directory already exists: {skill_dir}", file=sys.stderr)
        return None

    skill_dir.mkdir(parents=True)
    content = render_skill(skill_name, author, license_id, scope, repository)
    (skill_dir / "SKILL.md").write_text(content)
    print(f"Skill '{skill_name}' initialized at {skill_dir}")
    return skill_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name")
    parser.add_argument("--path", required=True)
    parser.add_argument("--author")
    parser.add_argument("--license", dest="license_id", required=True)
    parser.add_argument(
        "--scope", choices=("portable", "repo-local"), default="portable"
    )
    parser.add_argument(
        "--repository", help="repository name; required for repo-local skills"
    )
    args = parser.parse_args()

    author = args.author or discover_author()
    if not author:
        print(
            "Error: no author. Pass --author or set git config user.name.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = init_skill(
        args.skill_name,
        args.path,
        author,
        args.license_id,
        args.scope,
        args.repository,
    )
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
