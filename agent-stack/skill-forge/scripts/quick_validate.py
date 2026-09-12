#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Check Skill Forge policies outside the Agent Skills specification.

Run ``skills-ref validate`` separately for specification compliance. This script does
not duplicate that external schema and must not be reported as an equivalent check.

The policies checked here are provenance (top-level ``license``, ``metadata.author``,
attribution files), portability scope (``metadata.scope``), scaffold placeholders, and
bundled-reference reachability -- every relative path ``SKILL.md`` promises must exist
inside the skill directory, because a deployed skill has no context outside it.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - depends on the caller's runner
    # The inline script metadata above declares PyYAML, so a runner that reads it
    # resolves this. A plain interpreter does not, and an import traceback tells
    # the caller nothing about how to fix it. Exit 2 rather than 1: this is a
    # broken invocation, and a gate must not record it as a policy failure.
    print(
        "error: PyYAML is required. Run this script with a PEP 723-aware runner, "
        "for example: uv run quick_validate.py <skill-directory>",
        file=sys.stderr,
    )
    sys.exit(2)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(?:\n|$)", re.DOTALL)
PLACEHOLDERS = ("[TODO", "FIXME", "<skill-name>", "<upstream-")

# Directories the Agent Skills specification defines for bundled resources. A path
# under one of these is a promise that the file ships with the skill.
BUNDLED_DIRECTORIES = ("references", "scripts", "assets", "evals")

# Fenced blocks hold illustrative paths -- example output, scaffold templates, a
# command shown for another repository -- so only prose and links promise real files.
FENCED_BLOCK_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)\s]+)")
BUNDLED_PATH_RE = re.compile(
    r"(?<![\w./-])((?:"
    + "|".join(BUNDLED_DIRECTORIES)
    + r")/[\w.:@+-]+(?:/[\w.:@+-]+)*)"
)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "#", "/", "<")


def find_bundled_references(body: str) -> list[str]:
    """Return the relative paths a SKILL.md body promises ship with the skill.

    Collects Markdown link targets and bare paths under the specification's bundled
    resource directories, ignoring fenced code blocks, external URLs, and anchors.

    Args:
        body: The SKILL.md text after the YAML frontmatter block.

    Returns:
        Sorted, deduplicated relative paths, each stripped of any ``#`` fragment.
    """
    prose = FENCED_BLOCK_RE.sub("", body)
    candidates = set(MARKDOWN_LINK_RE.findall(prose))
    candidates.update(BUNDLED_PATH_RE.findall(prose))

    references: set[str] = set()
    for candidate in candidates:
        # Prose punctuation attaches to a bare path at the end of a sentence.
        reference = candidate.split("#", 1)[0].rstrip(".,:;)`'\"")
        if not reference or reference.startswith(EXTERNAL_PREFIXES):
            continue
        references.add(reference)
    return sorted(references)


def check_bundled_references(skill_path: Path, body: str) -> list[str]:
    """Return errors for bundled references that are missing or escape the skill.

    A deployed skill is copied without its surrounding repository, so a reference
    that leaves the skill directory cannot resolve wherever the skill is installed.

    Args:
        skill_path: The skill directory holding SKILL.md.
        body: The SKILL.md text after the YAML frontmatter block.

    Returns:
        One error message per unresolvable reference, in path order.
    """
    errors: list[str] = []
    for reference in find_bundled_references(body):
        if ".." in Path(reference).parts:
            errors.append(
                f"SKILL.md reference {reference!r} leaves the skill directory; a "
                "deployed skill cannot reach its surrounding repository"
            )
        elif not (skill_path / reference).exists():
            errors.append(
                f"SKILL.md references {reference!r} but no such file ships with "
                "the skill"
            )
    return errors


def validate_skill(skill_path: str | Path) -> tuple[list[str], list[str]]:
    """Return local-policy errors and warnings for a skill directory.

    Args:
        skill_path: The skill directory expected to contain SKILL.md.

    Returns:
        A ``(errors, warnings)`` pair. Errors fail the check; warnings never do.
        Both are empty when the skill satisfies every Skill Forge policy.
    """
    errors: list[str] = []
    warnings: list[str] = []
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.is_file():
        return ["SKILL.md not found"], warnings

    # An unreadable or non-UTF-8 SKILL.md is a policy failure to report, not a
    # traceback: the caller is a repository gate that reports one line per skill.
    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [f"cannot read SKILL.md: {error}"], warnings

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

    body = content[match.end() :]

    scope = metadata.get("scope")
    if scope not in (None, "repo-local"):
        errors.append(
            "metadata.scope must be absent for portable skills or 'repo-local'"
        )
    if scope == "repo-local":
        if "repository" not in "\n".join(body.splitlines()[:12]).lower():
            errors.append("repo-local skill must name its repository near the start")

    errors.extend(check_bundled_references(skill_path, body))

    attribution = skill_path / "ATTRIBUTIONS.md"
    upstream_license = skill_path / "LICENSE.upstream"
    if upstream_license.exists() and not attribution.exists():
        errors.append("LICENSE.upstream requires a corresponding ATTRIBUTIONS.md")
    if attribution.exists():
        # Same contract as SKILL.md above: this runs as a repository gate that
        # reports one line per skill, so an unreadable file is a finding rather
        # than a traceback that takes the whole run down with it.
        try:
            attribution_text = attribution.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"cannot read ATTRIBUTIONS.md: {error}")
            attribution_text = ""
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
    """Parse the command line, exiting 2 on an invalid invocation."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Exit status: 0 valid, 1 policy failures, 2 invalid invocation.",
    )
    parser.add_argument("skill_directory", type=Path, help="Agent Skill directory")
    return parser.parse_args()


def main() -> None:
    """Report warnings then errors, exiting 1 when any policy failed."""
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
