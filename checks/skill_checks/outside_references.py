"""Fail on a skill package file that references something outside its own package.

A skill is self-contained: once deployed, its directory is all an agent has. Two kinds of reference can reach
outside it, and both are checked:

- a Markdown link or image target, inline (`[text](target)`) or reference-style (`[label]: target`), outside a
  fenced code block; a target with a URL scheme or a bare `#anchor` is not a file reference;
- a path a bundled `.py`, `.sh` or `.bash` script builds from its own location: a `../` run in a string,
  resolved against the script's directory, or a `Path(__file__)` chain of `.parent` or `parents[n]` that climbs
  above the package.

Plain prose that names a path without linking it is not a reference and passes. An absolute path, a `~` path
or a `file:` URL in a link fails, because each points into one machine's files. The check reads lines with
patterns, not a parser: a link split across lines, an HTML `<a>` or `<img>`, a script without a suffix, and a
path built any other way pass unchecked.
"""

from __future__ import annotations

import re
from collections.abc import Iterator, Sequence
from pathlib import Path, PurePosixPath

import attrs

from skill_checks.skill_tree import package_files, skill_packages

MARKDOWN_SUFFIXES = frozenset({".md", ".markdown"})
SCRIPT_SUFFIXES = frozenset({".py", ".sh", ".bash"})
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FILE_URL = re.compile(r"^file:", re.IGNORECASE)
# A `../` run that opens a string, or that follows a shell directory expansion such as `$(dirname "$0")/` or
# `${SCRIPT_DIR}/`, both of which stand for the script's own directory.
SCRIPT_RELATIVE_PATH = re.compile(r"""(?:["'`]|\)/|\}/)((?:\.\./)+[^"'`\s)]*)""")
FILE_PARENT_CHAIN = re.compile(r"Path\(__file__\)(?:\.resolve\(\))?((?:\.parent)+)")
FILE_PARENTS_INDEX = re.compile(r"Path\(__file__\)(?:\.resolve\(\))?\.parents\[(\d+)\]")


@attrs.frozen
class Violation:
    """One reference that leaves its package."""

    path: Path
    line: int
    reference: str
    reason: str


def check_packages(roots: Sequence[Path]) -> tuple[Violation, ...]:
    """Return every outside reference in every package under `roots`."""
    violations: list[Violation] = []
    for package in skill_packages(roots):
        for path in package_files(package):
            violations.extend(check_file(package, path))
    return tuple(violations)


def check_file(package: Path, path: Path) -> Iterator[Violation]:
    """Yield the outside references in one file of a package."""
    if path.suffix not in MARKDOWN_SUFFIXES | SCRIPT_SUFFIXES:
        return
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    if path.suffix in MARKDOWN_SUFFIXES:
        yield from _markdown_violations(package, path, text)
    else:
        yield from _script_violations(package, path, text)


def _markdown_violations(package: Path, path: Path, text: str) -> Iterator[Violation]:
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        targets = [match.group(1) for match in INLINE_LINK.finditer(line)]
        definition = REFERENCE_DEFINITION.match(line)
        if definition:
            targets.append(definition.group(1))
        for target in targets:
            reason = _target_problem(package, path.parent, target)
            if reason:
                yield Violation(path, number, target, reason)


def _target_problem(package: Path, base: Path, target: str) -> str | None:
    if FILE_URL.match(target):
        return "file URL"
    if target.startswith("~"):
        return "home-relative path"
    if URL_SCHEME.match(target) or target.startswith("#"):
        return None
    file_part = target.split("#", 1)[0].split("?", 1)[0]
    if not file_part:
        return None
    if file_part.startswith("/") or PurePosixPath(file_part).is_absolute():
        return "absolute path"
    resolved = (base / file_part).resolve()
    if not resolved.is_relative_to(package.resolve()):
        return "resolves outside the package"
    return None


def _script_violations(package: Path, path: Path, text: str) -> Iterator[Violation]:
    depth = len(path.parent.relative_to(package).parts)
    for number, line in enumerate(text.splitlines(), start=1):
        for match in SCRIPT_RELATIVE_PATH.finditer(line):
            reference = match.group(1)
            if not (path.parent / reference).resolve().is_relative_to(package.resolve()):
                yield Violation(path, number, reference, "resolves outside the package")
        climbs = [len(chain) // len(".parent") - 1 for chain in FILE_PARENT_CHAIN.findall(line)]
        climbs += [int(index) for index in FILE_PARENTS_INDEX.findall(line)]
        for climb in climbs:
            if climb > depth:
                reference = f"Path(__file__) climbs {climb} level(s) from {depth} deep"
                yield Violation(path, number, reference, "climbs above the package")
