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

Contract:
    Output: one line per finding on stdout, a count on stderr.
    Exit:   0 clean, 1 findings, 2 bad invocation.
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


class RoutingRow(NamedTuple):
    """One row of a routing table whose headers the checker recognizes.

    Attributes:
        lineno: 1-based line the row sits on, so a finding can name it.
        target: The cell naming the destination document.
        trigger: The cell stating when to read that destination.
    """

    lineno: int
    target: str
    trigger: str


def _excluded(rel_posix: str, excludes: tuple[str, ...]) -> bool:
    """Report whether a root-relative path matches any exclusion glob.

    Patterns are matched against "/<path>" so a `*/name/*` glob also catches a
    top-level `name/`, which it would not without the leading separator.
    """
    probe = f"/{rel_posix}"
    return any(fnmatch.fnmatch(probe, pattern) for pattern in excludes)


def _find_floor(root: Path) -> Path | None:
    """Return the root floor file, or None when the repository has none."""
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
    for row in _routing_rows(text):
        raw_paths.extend(match.group(1) for match in MD_LINK.finditer(row.target))
        raw_paths.extend(match.group(1) for match in MD_BACKTICK.finditer(row.target))

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


def _reachable(seeds: list[Path], root: Path) -> tuple[set[Path], list[Finding]]:
    """Walk structural routes from the routing roots to everything they reach.

    Args:
        seeds: Routing roots — the floor and every scoped instruction file.
        root: Repository root, used to resolve root-relative route targets.

    Returns:
        The reachable set, and findings for documents that could not be read.
        An unreadable document is reported rather than skipped, because every
        route it carried would otherwise surface as unrelated unreachable files.
    """
    seen: set[Path] = {seed.resolve() for seed in seeds}
    queue = list(seen)
    findings: list[Finding] = []
    while queue:
        current = queue.pop()
        try:
            text = current.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(
                Finding(
                    _relative(current, root),
                    f"unreadable, so any route it carries is invisible: {error}",
                )
            )
            continue
        for target in _structural_paths(text, current.parent, root):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen, findings


def _relative(path: Path, root: Path) -> str:
    """Return a root-relative POSIX path, falling back to the absolute one."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _routing_rows(document_text: str) -> list[RoutingRow]:
    """Return the rows of every routing table whose headers are recognized."""
    rows: list[RoutingRow] = []
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
            rows.append(RoutingRow(lineno, cells[target_index], cells[trigger_index]))
    return rows


def _candidates(
    root: Path, docs_dirs: tuple[str, ...], excludes: tuple[str, ...]
) -> list[tuple[str, Path]]:
    """Yield (root-relative path, path) for every document the checks apply to.

    Every Markdown file under the docs directories, plus root-level Markdown
    that is neither the floor nor self-justifying by name.
    """
    found: list[Path] = []
    for docs_dir in docs_dirs:
        base = root / docs_dir
        if base.is_dir():
            found.extend(sorted(base.rglob("*.md")))
    for child in sorted(root.glob("*.md")):
        if child.name not in FLOOR_NAMES and child.name not in DEFAULT_ROOT_EXEMPT:
            found.append(child)

    selected: list[tuple[str, Path]] = []
    for path in found:
        relative = path.relative_to(root).as_posix()
        if not _excluded(relative, excludes):
            selected.append((relative, path))
    return selected


def check_reachability(
    candidates: list[tuple[str, Path]], reachable: set[Path]
) -> list[Finding]:
    """Report living documents no structural route reaches.

    Dated records are exempt: they are reached by browsing their genre directory
    when their moment comes, so a routing row per record would be noise.
    """
    return [
        Finding(
            relative,
            "unreachable: no routing-table row or standalone inclusion link reaches here",
        )
        for relative, path in candidates
        if path.resolve() not in reachable and not _excluded(relative, RECORD_DIR_GLOBS)
    ]


def check_line_references(candidates: list[tuple[str, Path]]) -> list[Finding]:
    """Report line-number references in living documents that do not pin a revision.

    Frozen genres are skipped entirely: there a line number is a dated snapshot
    coordinate rather than rot. A living document may opt out the same way by
    declaring its pinned revision in its head.
    """
    findings: list[Finding] = []
    for relative, path in candidates:
        if _excluded(relative, FROZEN_DIR_GLOBS):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(Finding(relative, f"unreadable: {error}"))
            continue
        head = "\n".join(text.splitlines()[:PIN_HEAD_LINES])
        if PIN_WORD.search(head) and PIN_REV.search(head):
            continue
        findings.extend(
            Finding(
                relative,
                f"line-number reference {match.group(0)!r} will rot; "
                "point at a stable anchor",
            )
            for match in LINE_REF.finditer(text)
        )
    return findings


def check_trigger_cells(floor: Path, root: Path) -> list[Finding]:
    """Report floor routing rows with nothing in their trigger cell.

    A row without a trigger condition cannot act as a load/skip classifier, which
    is the only job the routing table has.
    """
    relative = _relative(floor, root)
    try:
        text = floor.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [Finding(relative, f"unreadable: {error}")]
    return [
        Finding(
            relative,
            f"line {row.lineno}: routing row {row.target!r} has an empty trigger cell",
        )
        for row in _routing_rows(text)
        if not row.trigger
    ]


def _scan(
    root: Path, docs_dirs: tuple[str, ...], excludes: tuple[str, ...]
) -> list[Finding]:
    """Run every system-level check over one repository."""
    floor = _find_floor(root)
    if floor is None:
        return [
            Finding(".", f"no floor file found (looked for {', '.join(FLOOR_NAMES)})")
        ]

    reachable, findings = _reachable(_routing_roots(root, excludes), root)
    candidates = _candidates(root, docs_dirs, excludes)

    findings.extend(check_reachability(candidates, reachable))
    findings.extend(check_line_references(candidates))
    findings.extend(check_trigger_cells(floor, root))
    return findings


def main(argv: list[str] | None = None) -> int:
    """Entry point. See the module docstring for the contract."""
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog="Exit status: 0 clean, 1 findings, 2 invalid invocation.",
    )
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
