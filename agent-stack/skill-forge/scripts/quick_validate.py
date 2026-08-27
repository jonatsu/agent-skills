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
# Lowercase, digits, single hyphens; no leading, trailing or consecutive hyphens.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Rejected in a skill name by claude.ai uploads and the Skills API. Verified 2026-08-27
# against https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
# Warned rather than failed: Claude Code loads such a skill fine -- this repo's own
# claude-automation-recommender is deployed and working -- so the constraint bounds
# distribution, not local use.
RESERVED_WORDS = ("anthropic", "claude")

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
    if not 1 <= len(name) <= 64:
        return False, f"Name '{name}' is {len(name)} characters; must be 1-64", warnings
    if not NAME_RE.match(name):
        return (
            False,
            f"Name '{name}' must be lowercase letters, digits and single hyphens, "
            "with no leading, trailing or consecutive hyphens",
            warnings,
        )
    for word in RESERVED_WORDS:
        if word in name:
            warnings.append(
                f"name contains '{word}', which claude.ai uploads and the Skills API "
                "reject. Claude Code loads such a skill without complaint, so this "
                "blocks distribution rather than local use."
            )
    if name != skill_path.resolve().name:
        return (
            False,
            f"Name '{name}' does not match its directory "
            f"'{skill_path.resolve().name}'; the skill is unreachable under the "
            "name it advertises",
            warnings,
        )

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
