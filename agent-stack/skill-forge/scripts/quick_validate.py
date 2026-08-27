#!/usr/bin/env python3
"""Quick validation script for skills.

Fails only on structural defects — things that are wrong regardless of which agent
loads the skill. Unrecognised frontmatter keys are reported as warnings, NEVER as
failures: skills here deploy to Claude Code, OpenCode and Copilot CLI, whose
frontmatter schemas are owned by those vendors and move independently. An allowlist
that fails closed would be a transcribed schema, which SKILL.md forbids, and it would
reject a valid skill every time a harness ships a new field.
"""

import re
import sys
from pathlib import Path

import yaml

# Advisory only. Union of the surfaces this repo deploys to, verified 2026-08-27
# against https://code.claude.com/docs/en/skills. Being absent from this set is a
# prompt to check, NEVER evidence of a defect.
KNOWN_KEYS = {
    # Claude Code skill frontmatter
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    # Accepted additionally by claude.ai uploads and the Skills API
    "license",
    "compatibility",
    "metadata",
}


def validate_skill(skill_path):
    """Return (valid, message, warnings). Only structural defects set valid=False."""
    warnings = []
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found", warnings
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found", warnings
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", warnings
    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary", warnings
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}", warnings

    unknown = set(frontmatter.keys()) - KNOWN_KEYS
    if unknown:
        warnings.append(
            f"unrecognised frontmatter key(s): {', '.join(sorted(unknown))}. "
            "Harness schemas move; verify against the target agent's docs before "
            "treating this as a defect."
        )

    if "name" not in frontmatter or "description" not in frontmatter:
        return False, "Missing required frontmatter fields", warnings

    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return False, "metadata must be a YAML dictionary", warnings
    for key in ("author", "license"):
        value = (metadata or {}).get(key)
        if value is None:
            warnings.append(
                f"metadata.{key} is not set. Required for a skill authored here; "
                "expected to be absent on a third-party skill under evaluation."
            )
        elif not str(value).strip():
            return False, f"metadata.{key} cannot be empty", warnings

    name = str(frontmatter.get("name", "")).strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' should be hyphen-case", warnings

    description = str(frontmatter.get("description", "")).strip()
    if not description:
        return False, "Description cannot be empty", warnings
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets", warnings
    if len(description) > 1024:
        return False, f"Description too long ({len(description)} chars)", warnings

    return True, "Skill is structurally valid.", warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message, warnings = validate_skill(sys.argv[1])
    for warning in warnings:
        print(f"warning: {warning}")
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
