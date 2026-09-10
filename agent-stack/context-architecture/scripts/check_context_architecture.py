#!/usr/bin/env python3
"""Report system-level context defects: unreachable docs, blank routing, rotting references.

The floor file's routing table is the contract that every agent-facing document
can be found from a cold start. This measures that contract from the outside:
a document no structural route reaches is invisible at need, a routing row
without a trigger condition cannot be a load/skip classifier, and a
line-number reference is stale before it is read.

Instruction-file internals (size budgets, evidence indexing) belong to
agents-management's check_agent_context.py; run both. Stdlib only, so the
skill stays portable: no package manager, no repository commands, and no
assumption that the tree is a Git checkout.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path
from typing import NamedTuple

FLOOR_NAMES = ("AGENTS.md", "CLAUDE.md")
DEFAULT_DOCS_DIRS = ("docs",)

# Root-level files that are self-justifying and need no routing row.
DEFAULT_ROOT_EXEMPT = ("README.md", "LICENSE.md", "CHANGELOG.md", "TODO.md")

DEFAULT_EXCLUDES = (
    "*/fixtures/*",
    "*/testdata/*",
    "*/node_modules/*",
    "*/vendor/*",
    "*/.git/*",
    "*/archive/*",  # retired material is reachable through its directory, not per-file routing
    "*/archived/*",
)

# Frozen genres are dated snapshots: a line number there records where something
# was at write time, which is the point, not rot. Only living documents get the
# line-reference check.
FROZEN_DIR_GLOBS = ("*/decisions/*", "*/evaluations/*")

# Dated-record genres are reached by browsing their directory when their moment
# comes, not by per-file routing rows; requiring a row per record is noise. The
# orphan check binds only living, load-at-need documents.
RECORD_DIR_GLOBS = (
    "*/decisions/*",
    "*/evaluations/*",
    "*/plans/*",
    "*/working-notes/*",
)

# A living document may pin the revision its line references are valid at, which
# converts them from rot into dated snapshot coordinates. The declaration must sit
# in the document's head where a reader sees it before any citation.
PIN_HEAD_LINES = 15
PIN_WORD = re.compile(r"\bpinned\b", re.IGNORECASE)
PIN_REV = re.compile(r"`[0-9a-f]{7,40}`")

# A Markdown link target, and a backticked path accepted only in a routing-table file cell.
MD_LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
MD_BACKTICK = re.compile(r"`([^`\s]+\.md)`")
STANDALONE_MD_LINK = re.compile(r"^\s*\[[^]\n]+\]\(([^)#\s]+\.md)(?:#[^)]*)?\)\s*$")
ROUTE_TARGET_HEADERS = {"file", "read"}
ROUTE_TRIGGER_HEADER = re.compile(r"^(?:read when|symptom|read before\b|if you\b)")
# Line-number references that rot: file.ext:123 for code extensions, or GitHub-style #L123.
LINE_REF = re.compile(
    r"\b\S+\.(?:md|nix|py|sh|bash|rs|go|ts|js|c|h|cpp|yaml|yml|toml|lock|pl|json):\d+\b|#L\d+\b"
)

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2


class Finding(NamedTuple):
    """One reported problem.

    Attributes:
        path: Root-relative POSIX path the finding is about.
        message: What is wrong and what fixing it looks like.
    """

    path: str
    message: str


def _excluded(rel_posix: str, excludes: tuple[str, ...]) -> bool:
    probe = f"/{rel_posix}"
    return any(fnmatch.fnmatch(probe, pattern) for pattern in excludes)


def _find_floor(root: Path) -> Path | None:
    for name in FLOOR_NAMES:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def _structural_paths(text: str, base: Path, root: Path) -> set[Path]:
    """Resolve deliberate parent-child routes rather than incidental references."""
    found: set[Path] = set()
    raw_paths = [
        match.group(1)
        for line in text.splitlines()
        if (match := STANDALONE_MD_LINK.fullmatch(line))
    ]
    for _, (file_cell, _) in _routing_rows(text):
        raw_paths.extend(match.group(1) for match in MD_LINK.finditer(file_cell))
        raw_paths.extend(match.group(1) for match in MD_BACKTICK.finditer(file_cell))

    for raw in raw_paths:
        for origin in (base, root):
            candidate = (origin / raw).resolve()
            if candidate.is_file():
                found.add(candidate)
                break
    return found


def _routing_roots(root: Path, excludes: tuple[str, ...]) -> list[Path]:
    """The root floor plus every scoped instruction file — clients load these by location."""
    roots: list[Path] = []
    for name in FLOOR_NAMES:
        for candidate in root.rglob(name):
            rel = candidate.relative_to(root).as_posix()
            if candidate.is_file() and not _excluded(rel, excludes):
                roots.append(candidate)
    return roots


def _reachable(seeds: list[Path], root: Path) -> set[Path]:
    """Transitive closure of structural routes starting at the routing roots."""
    seen: set[Path] = {seed.resolve() for seed in seeds}
    queue = list(seen)
    while queue:
        current = queue.pop()
        try:
            text = current.read_text(encoding="utf-8")
        except OSError:
            continue
        for target in _structural_paths(text, current.parent, root):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


def _routing_rows(document_text: str) -> list[tuple[int, list[str]]]:
    """Return target and trigger cells from routing tables with recognized headers."""
    rows: list[tuple[int, list[str]]] = []
    in_table = False
    target_index = -1
    trigger_index = -1
    for lineno, line in enumerate(document_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        target_hit = next(
            (i for i, cell in enumerate(cells) if cell.lower() in ROUTE_TARGET_HEADERS),
            -1,
        )
        trigger_hit = next(
            (
                i
                for i, cell in enumerate(cells)
                if ROUTE_TRIGGER_HEADER.match(cell.lower())
            ),
            -1,
        )
        if target_hit >= 0 and trigger_hit >= 0:
            in_table = True
            target_index = target_hit
            trigger_index = trigger_hit
            continue
        if in_table and set(stripped) <= {"|", "-", " ", ":"}:
            continue  # separator row
        if in_table and max(target_index, trigger_index) < len(cells):
            rows.append((lineno, [cells[target_index], cells[trigger_index]]))
    return rows


def _scan(
    root: Path, docs_dirs: tuple[str, ...], excludes: tuple[str, ...]
) -> list[Finding]:
    findings: list[Finding] = []
    floor = _find_floor(root)
    if floor is None:
        return [
            Finding(".", f"no floor file found (looked for {', '.join(FLOOR_NAMES)})")
        ]

    reachable = _reachable(_routing_roots(root, excludes), root)

    candidates: list[Path] = []
    for docs_dir in docs_dirs:
        base = root / docs_dir
        if base.is_dir():
            candidates.extend(sorted(base.rglob("*.md")))
    for child in sorted(root.glob("*.md")):
        if child.name not in FLOOR_NAMES and child.name not in DEFAULT_ROOT_EXEMPT:
            candidates.append(child)

    for path in candidates:
        rel = path.relative_to(root).as_posix()
        if _excluded(rel, excludes):
            continue
        if path.resolve() not in reachable and not _excluded(rel, RECORD_DIR_GLOBS):
            findings.append(
                Finding(
                    rel,
                    "unreachable: no routing-table row or standalone inclusion link reaches here",
                )
            )
        if _excluded(rel, FROZEN_DIR_GLOBS):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        head = "\n".join(text.splitlines()[:PIN_HEAD_LINES])
        if PIN_WORD.search(head) and PIN_REV.search(head):
            continue
        for match in LINE_REF.finditer(text):
            findings.append(
                Finding(
                    rel,
                    f"line-number reference {match.group(0)!r} will rot; point at a stable anchor",
                )
            )

    floor_rel = floor.relative_to(root).as_posix()
    for lineno, (target_cell, trigger) in _routing_rows(
        floor.read_text(encoding="utf-8")
    ):
        if not trigger:
            findings.append(
                Finding(
                    floor_rel,
                    f"line {lineno}: routing row {target_cell!r} has an empty trigger cell",
                )
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path, help="repository root to scan")
    parser.add_argument(
        "--docs-dir",
        action="append",
        default=None,
        metavar="DIR",
        help=f"root-relative docs directory to scan (repeatable; default: {', '.join(DEFAULT_DOCS_DIRS)})",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        metavar="GLOB",
        help="extra glob matched against '/<root-relative path>' (repeatable, adds to defaults)",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {args.root}")
    docs_dirs = tuple(args.docs_dir) if args.docs_dir else DEFAULT_DOCS_DIRS
    excludes = DEFAULT_EXCLUDES + tuple(args.exclude or ())

    findings = _scan(root, docs_dirs, excludes)
    for finding in findings:
        print(f"{finding.path}: {finding.message}")
    if findings:
        print(f"{len(findings)} finding(s)", file=sys.stderr)
        return EXIT_FINDINGS
    print("clean")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
