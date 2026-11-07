#!/usr/bin/env python3
"""Report system-level context defects: unreachable docs, blank routing, rotting references.

The floor file's routing entries are the contract that every agent-facing document
can be found from a cold start. This measures that contract from the outside:
a document no structural route reaches is invisible at need, a routing entry
without a trigger condition cannot be a load/skip classifier, and a
line-number reference is stale before it is read.

Instruction-file internals (size budgets, evidence indexing) belong to
the agents-context-docs skill's check_agent_context.py; run both. Stdlib only, so the
skill stays portable: no package manager, no repository commands, and no
assumption that the tree is a Git checkout.

Contract:
    Output: one line per finding on stdout, a count on stderr.
    Exit:   0 clean, 1 findings, 2 bad invocation.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple

FLOOR_NAMES = ("AGENTS.md", "CLAUDE.md")
DEFAULT_DOCS_DIRS = ("docs",)

# Root-level files that are self-justifying and need no routing entry. The ledger
# pair is a documented default-layout contract protected by behavioral tests.
DEFAULT_ROOT_EXEMPT = (
    "README.md",
    "LICENSE.md",
    "CHANGELOG.md",
    "TODO.md",
    "BACKLOG.md",
)

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
# comes, not by per-file routing entries; requiring an entry per record is noise. The
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
MD_DOCUMENT_LINK = re.compile(r"\[[^]\n]+\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
MD_BACKTICK = re.compile(r"`([^`\s]+\.md)`")
STANDALONE_MD_LINK = re.compile(r"^\s*\[[^]\n]+\]\(([^)#\s]+\.md)(?:#[^)]*)?\)\s*$")
ROUTE_LIST_PREFIX = re.compile(
    r"^\s*-\s+(?:read when|read before|if you|symptom)\b(?P<rest>.*)$",
    re.IGNORECASE,
)
ROUTE_TARGET_HEADERS = {"file", "read"}
# Linked rows before a trigger-less table is read as an index rather than content.
MINIMUM_ROUTED_ROWS = 2
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


class RoutingEntry(NamedTuple):
    """One trigger-keyed route whose form the checker recognizes.

    Attributes:
        lineno: 1-based line the route starts on, so a finding can name it.
        target: The text containing the destination document link or path.
        trigger: The condition for reading that destination.
        form: The recognized Markdown structure, either ``table`` or ``list``.
    """

    lineno: int
    target: str
    trigger: str
    form: str


REFERENCE_DEFINITION = re.compile(r"^ {0,3}\[([^\]\n]+)\]:\s*(?:<([^>\n]+)>|(\S+))")
REFERENCE_LINK = re.compile(r"(?<!!)\[([^\[\]\n]+)\](?:[ \t]*\[([^\[\]\n]*)\])?")
CODE_SPAN = re.compile(r"(`+)(.*?)\1(?!`)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def _reference_label(label: str) -> str:
    """Apply Markdown's case-insensitive, whitespace-normalized label matching."""
    return " ".join(label.split()).casefold()


def _routing_text(text: str) -> str:
    """Expand used reference links while keeping code and definitions out of routes."""
    lines: list[str] = []
    fence = ""
    for line in text.splitlines():
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = ""
            lines.append("")
        elif marker:
            fence = marker[1]
            lines.append("")
        else:
            lines.append(line)
    definitions: dict[str, str] = {}
    for line in lines:
        if match := REFERENCE_DEFINITION.match(line):
            definitions.setdefault(_reference_label(match[1]), match[2] or match[3])

    def expand(match: re.Match[str]) -> str:
        if match.string[match.end() :].startswith("("):
            return match[0]
        label = match[1] if match[2] in (None, "") else match[2]
        destination = definitions.get(_reference_label(label))
        return f"[{match[1]}]({destination})" if destination else match[0]

    prepared: list[str] = []
    for line in lines:
        if REFERENCE_DEFINITION.match(line):
            prepared.append("")
            continue
        pieces: list[str] = []
        start = 0
        for code in CODE_SPAN.finditer(line):
            pieces.append(REFERENCE_LINK.sub(expand, line[start : code.start()]))
            # Routing tables also deliberately accept a lone backticked document path.
            literal = code[0] if re.fullmatch(r"`[^`\s]+\.md`", code[0]) else " " * len(code[0])
            pieces.append(literal)
            start = code.end()
        pieces.append(REFERENCE_LINK.sub(expand, line[start:]))
        prepared.append("".join(pieces))
    return "\n".join(prepared)


def _inside_nested_repository(path: Path, root: Path) -> bool:
    """Keep a chosen repository separate from nested checkouts and linked worktrees."""
    current = path.resolve()
    root = root.resolve()
    if not current.is_relative_to(root):
        return False
    while current != root:
        if os.path.lexists(current / ".git"):
            return True
        current = current.parent
    return False


def _repository_files(root: Path, excludes: tuple[str, ...]) -> Iterator[Path]:
    """Walk owned files without entering excluded directories or nested repositories."""
    for directory, names, filenames in os.walk(root):
        base = Path(directory)
        names[:] = [
            name
            for name in names
            if name != ".git"
            and not os.path.lexists(base / name / ".git")
            and not any(
                fnmatch.fnmatch(f"/{(base / name).relative_to(root).as_posix()}/", pattern)
                for pattern in excludes
            )
        ]
        for name in filenames:
            path = base / name
            relative = path.relative_to(root).as_posix()
            if not any(fnmatch.fnmatch(f"/{relative}", pattern) for pattern in excludes):
                yield path


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
    text = _routing_text(text)
    found: set[Path] = set()
    raw_paths = [
        match.group(1)
        for line in text.splitlines()
        if (match := STANDALONE_MD_LINK.fullmatch(line))
    ]
    for entry in _routing_entries(text):
        if not entry.trigger:
            continue
        raw_paths.extend(match.group(1) for match in MD_LINK.finditer(entry.target))
        raw_paths.extend(match.group(1) for match in MD_BACKTICK.finditer(entry.target))

    for raw in raw_paths:
        for origin in (base, root):
            candidate = (origin / raw).resolve()
            if candidate.is_file() and not _inside_nested_repository(candidate, root):
                found.add(candidate)
                break
    return found


def _routing_roots(root: Path, excludes: tuple[str, ...]) -> list[Path]:
    """The root floor plus every scoped instruction file — clients load these by location."""
    return sorted(path for path in _repository_files(root, excludes) if path.name in FLOOR_NAMES)


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


def _routing_table_entries(document_text: str) -> list[RoutingEntry]:
    """Return the rows of every routing table whose headers are recognized."""
    entries: list[RoutingEntry] = []
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
            (i for i, cell in enumerate(cells) if ROUTE_TRIGGER_HEADER.match(cell.lower())),
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
            entries.append(RoutingEntry(lineno, cells[target_index], cells[trigger_index], "table"))
    return entries


def _routing_list_entries(document_text: str) -> list[RoutingEntry]:
    """Return trigger-keyed list items that contain a Markdown document link."""
    entries: list[RoutingEntry] = []
    for lineno, line in enumerate(document_text.splitlines(), start=1):
        match = ROUTE_LIST_PREFIX.fullmatch(line)
        if match is None:
            continue
        rest = match.group("rest")
        target_link = MD_DOCUMENT_LINK.search(rest)
        if target_link is None:
            continue
        separator = rest.rfind(":", 0, target_link.start())
        if separator < 0 or rest[separator + 1 : target_link.start()].strip():
            continue
        entries.append(
            RoutingEntry(
                lineno,
                rest[separator + 1 :].strip(),
                rest[:separator].strip(),
                "list",
            )
        )
    return entries


def _routing_entries(document_text: str) -> list[RoutingEntry]:
    """Return every recognized trigger-keyed table row and list item."""
    document_text = _routing_text(document_text)
    return _routing_table_entries(document_text) + _routing_list_entries(document_text)


def _linked_target_rows(lines: list[str], start: int, target_index: int) -> int:
    """Count rows whose target cell links a document, until the table ends."""
    linked = 0
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if target_index < len(cells) and MD_LINK.search(cells[target_index]):
            linked += 1
    return linked


def check_routing_table_headers(document_text: str, relative: str) -> list[Finding]:
    """Report likely routing tables that only one recognized header reaches.

    A table routes only when both headers are recognized, so either one alone is
    a near miss worth reporting at its own line rather than as unreachable
    children elsewhere. The two directions need different evidence. A trigger
    header is distinctive enough to convict on its own. A target header is not —
    `File` heads many tables that route nothing — so the missing-trigger case is
    reported only when the target cells actually carry document links, which is
    what makes a reader treat the table as a route.
    """
    lines = _routing_text(document_text).splitlines()
    findings: list[Finding] = []
    for index, line in enumerate(lines[:-1]):
        stripped = line.strip()
        separator = lines[index + 1].strip()
        if not stripped.startswith("|") or not separator.startswith("|"):
            continue
        if not separator or not set(separator) <= {"|", "-", " ", ":"}:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        trigger = next(
            (cell for cell in cells if ROUTE_TRIGGER_HEADER.match(cell.lower())),
            None,
        )
        target_index = next(
            (i for i, cell in enumerate(cells) if cell.lower() in ROUTE_TARGET_HEADERS),
            -1,
        )
        if trigger is not None and target_index < 0:
            findings.append(
                Finding(
                    relative,
                    f"line {index + 1}: routing table has trigger column {trigger!r} "
                    "but no recognized target column ('File' or 'Read')",
                )
            )
            continue
        if trigger is None and target_index >= 0:
            linked = _linked_target_rows(lines, index + 2, target_index)
            if linked >= MINIMUM_ROUTED_ROWS:
                findings.append(
                    Finding(
                        relative,
                        f"line {index + 1}: table has target column "
                        f"{cells[target_index]!r} and links {linked} documents, but "
                        "no recognized trigger column ('Read when', 'Symptom', "
                        "'Read before', 'If you'), so it routes to none of them",
                    )
                )
    return findings


def _candidates(
    root: Path, docs_dirs: tuple[str, ...], excludes: tuple[str, ...]
) -> list[tuple[str, Path]]:
    """Yield (root-relative path, path) for every document the checks apply to.

    Every Markdown file under the docs directories, plus root-level Markdown
    that is neither the floor nor self-justifying by name.
    """
    bases = [root / docs_dir for docs_dir in docs_dirs]
    found = [
        path
        for path in _repository_files(root, excludes)
        if path.suffix == ".md"
        and (
            any(base in path.parents for base in bases)
            or (
                path.parent == root
                and path.name not in FLOOR_NAMES
                and path.name not in DEFAULT_ROOT_EXEMPT
            )
        )
    ]
    return [(path.relative_to(root).as_posix(), path) for path in sorted(found)]


def check_reachability(candidates: list[tuple[str, Path]], reachable: set[Path]) -> list[Finding]:
    """Report living documents no structural route reaches.

    Dated records are exempt: they are reached by browsing their genre directory
    when their moment comes, so a routing entry per record would be noise.
    """
    return [
        Finding(
            relative,
            "unreachable: no trigger-keyed route or standalone inclusion link reaches here",
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
                f"line-number reference {match.group(0)!r} will rot; point at a stable anchor",
            )
            for match in LINE_REF.finditer(text)
        )
    return findings


def check_route_triggers(document_text: str, relative: str) -> list[Finding]:
    """Report recognized routing entries with no trigger condition.

    An entry without a trigger condition cannot act as a load/skip classifier,
    which is the only job a route has.
    """
    return [
        Finding(
            relative,
            f"line {entry.lineno}: routing list item has an empty trigger condition"
            if entry.form == "list"
            else f"line {entry.lineno}: routing row {entry.target!r} has an empty trigger cell",
        )
        for entry in _routing_entries(document_text)
        if not entry.trigger
    ]


def _scan(root: Path, docs_dirs: tuple[str, ...], excludes: tuple[str, ...]) -> list[Finding]:
    """Run every system-level check over one repository."""
    floor = _find_floor(root)
    if floor is None:
        return [Finding(".", f"no floor file found (looked for {', '.join(FLOOR_NAMES)})")]

    routing_roots = _routing_roots(root, excludes)
    reachable, findings = _reachable(routing_roots, root)
    candidates = _candidates(root, docs_dirs, excludes)

    documents = {path.resolve(): path for path in routing_roots}
    documents.update({path.resolve(): path for _, path in candidates})
    for path in sorted(documents.values()):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # reachability and line-reference checks own unreadable-file findings
        findings.extend(check_routing_table_headers(text, _relative(path, root)))
        findings.extend(check_route_triggers(text, _relative(path, root)))

    findings.extend(check_reachability(candidates, reachable))
    findings.extend(check_line_references(candidates))
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
