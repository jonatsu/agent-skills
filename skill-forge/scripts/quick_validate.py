#!/usr/bin/env python3
"""Quick validation script for skills."""

import sys
import re
import yaml
from pathlib import Path

ALLOWED_PROPERTIES = {
    "name",
    "description",
    "metadata",
    "globs",
    "alwaysApply",
    "hide",
    "disable-model-invocation",
}


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"
    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, f"Unexpected key(s): {', '.join(sorted(unexpected))}"
    if "name" not in frontmatter or "description" not in frontmatter:
        return False, "Missing required frontmatter fields"
    metadata = frontmatter.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            return False, "metadata must be a YAML dictionary"
        for key in ("author", "license"):
            if key in metadata and not str(metadata[key]).strip():
                return False, f"metadata.{key} cannot be empty"
    name = str(frontmatter.get("name", "")).strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' should be hyphen-case"
    description = str(frontmatter.get("description", "")).strip()
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets"
    if len(description) > 1024:
        return False, f"Description too long ({len(description)} chars)"
    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
