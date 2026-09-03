#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Check Skill Forge policies outside the Agent Skills specification.

Run ``skills-ref validate`` separately for specification compliance. This script does
not duplicate that external schema and must not be reported as an equivalent check.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(?:\n|$)", re.DOTALL)
PLACEHOLDERS = ("[TODO", "FIXME", "<skill-name>", "<upstream-")


def validate_skill(skill_path: str | Path) -> tuple[list[str], list[str]]:
    """Return local-policy errors and warnings for a skill directory."""
    errors: list[str] = []
    warnings: list[str] = []
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.is_file():
        return ["SKILL.md not found"], warnings

    content = skill_md.read_text()
    match = FRONTMATTER_RE.match(content)
    if not match:
        return [
            "cannot inspect local policy because YAML frontmatter is invalid"
        ], warnings

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return [f"cannot inspect local policy: {error}"], warnings
    if not isinstance(frontmatter, dict):
        return [
            "cannot inspect local policy because frontmatter is not a mapping"
        ], warnings

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata must contain the current author")
        metadata = {}
    elif not str(metadata.get("author", "")).strip():
        errors.append("metadata.author must name the current author")

    if not str(frontmatter.get("license", "")).strip():
        errors.append("top-level license must identify the applicable license")
    if "license" in metadata:
        errors.append(
            "move metadata.license to the Agent Skills top-level license field"
        )

    scope = metadata.get("scope")
    if scope not in (None, "repo-local"):
        errors.append(
            "metadata.scope must be absent for portable skills or 'repo-local'"
        )
    if scope == "repo-local":
        body = content[match.end() :]
        if "repository" not in "\n".join(body.splitlines()[:12]).lower():
            errors.append("repo-local skill must name its repository near the start")

    attribution = skill_path / "ATTRIBUTIONS.md"
    upstream_license = skill_path / "LICENSE.upstream"
    if upstream_license.exists() and not attribution.exists():
        errors.append("LICENSE.upstream requires a corresponding ATTRIBUTIONS.md")
    if attribution.exists():
        attribution_text = attribution.read_text()
        for placeholder in PLACEHOLDERS:
            if placeholder in attribution_text:
                errors.append(
                    f"ATTRIBUTIONS.md contains scaffold placeholder {placeholder!r}"
                )

    for placeholder in PLACEHOLDERS:
        if placeholder in content:
            errors.append(f"SKILL.md contains scaffold placeholder {placeholder!r}")

    if not attribution.exists():
        warnings.append(
            "source influence cannot be inferred; confirm whether external ideas or "
            "expression require ATTRIBUTIONS.md"
        )

    return errors, warnings


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Exit status: 0 valid, 1 policy failures, 2 invalid invocation.",
    )
    parser.add_argument("skill_directory", type=Path, help="Agent Skill directory")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    errors, warnings = validate_skill(args.skill_directory)
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    if errors:
        sys.exit(1)
    print("Skill Forge local policy is valid.")


if __name__ == "__main__":
    main()
