#!/usr/bin/env python3
"""Report instruction files that outgrew their budget or lost their evidence.

Instruction files load on every session, so their size is a recurring cost and
their oldest rules are the first a model stops reading. Accretion is invisible
to any per-addition test, because every passage was justified on the day it
arrived. This measures the file rather than the edit.

Stdlib only, so the skill stays portable: no package manager, no repository
commands, and no assumption that the tree is a Git checkout.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import NamedTuple

DEFAULT_BUDGET = 2000
DEFAULT_EVIDENCE_DIR = "docs/findings"
DEFAULT_NAMES = ("AGENTS.md", "CLAUDE.md")

# Directories whose instruction files are payloads the repository stores rather
# than context it obeys. Evaluation transcripts and test fixtures both contain
# realistic AGENTS.md files that must not be measured. The scratch directory
# holds task artefacts and cloned repositories, so it grows instruction files
# the repository never obeys; it is untracked, which is why walking the
# filesystem sees what a git-aware scan would not.
DEFAULT_EXCLUDES = (
    "*/fixtures/*",
    "*/testdata/*",
    "*/evaluations/*",
    "*/node_modules/*",
    "*/vendor/*",
    "*/.git/*",
    "*/.scratch/*",
)

ISO_DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2


class Config(NamedTuple):
    """Resolved options for one run.

    Attributes:
        root: Repository root the scan is relative to.
        budget: Word ceiling applied to any file without an override.
        budget_for: Per-file ceilings, keyed by root-relative POSIX path.
        evidence_dir: Root-relative directory holding the evidence files.
        names: Instruction filenames to treat as context.
        excludes: Glob patterns matched against "/<root-relative path>".
    """

    root: Path
    budget: int
    budget_for: dict[str, int]
    evidence_dir: str
    names: tuple[str, ...]
    excludes: tuple[str, ...]


class Finding(NamedTuple):
    """One reported problem.

    Attributes:
        kind: Machine-readable category, also the first output column.
        path: Root-relative path the finding belongs to.
        detail: Human-readable specifics.
    """

    kind: str
    path: str
    detail: str


def iter_context_files(config: Config) -> Iterator[tuple[str, Path]]:
    """Yield (root-relative path, path) for each instruction file to measure.

    Files are discovered rather than listed, so a new nested instruction file
    is covered the day it appears. Symlinks are skipped: the CLAUDE.md beside an
    AGENTS.md is usually a link to it, and counting both would double its cost.
    """
    for path in sorted(config.root.rglob("*")):
        if path.name not in config.names:
            continue
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(config.root).as_posix()
        if any(fnmatch.fnmatch(f"/{relative}", pattern) for pattern in config.excludes):
            continue
        yield relative, path


def evidence_links(text: str, evidence_dir: str) -> list[str]:
    """Return each distinct reference to an evidence file, in source order.

    Matches prose links and index-table cells alike, because both break the same
    way. A leading `../` run is kept so the reference resolves against the
    referring file's own directory.
    """
    pattern = re.compile(rf"((?:\.\./)*{re.escape(evidence_dir)}/[\w.\-]+\.md)")
    seen: dict[str, None] = {}
    for match in pattern.findall(text):
        seen.setdefault(match, None)
    return list(seen)


def check_links(
    relative: str, path: Path, text: str, config: Config, referenced: set[str]
) -> list[Finding]:
    """Resolve every evidence reference in one file, recording what it points at."""
    findings: list[Finding] = []
    for reference in evidence_links(text, config.evidence_dir):
        target = (path.parent / reference).resolve()
        try:
            resolved = target.relative_to(config.root.resolve()).as_posix()
        except ValueError:
            findings.append(
                Finding("escapes", relative, f"{reference} resolves outside the root")
            )
            continue
        referenced.add(resolved)
        if not target.is_file():
            findings.append(Finding("dangling", relative, reference))
    return findings


def check_budget(relative: str, text: str, config: Config) -> list[Finding]:
    """Compare a file's word count against its ceiling.

    `str.split` counts markup and fenced code too, so this is a proxy. It is
    monotonic in the quantity that matters, which is enough for a ceiling.
    """
    words = len(text.split())
    limit = config.budget_for.get(relative, config.budget)
    if words > limit:
        return [Finding("oversize", relative, f"{words} words, budget {limit}")]
    return []


def check_dates(relative: str, text: str) -> list[Finding]:
    """Report ISO dates, which usually mark a measurement that belongs elsewhere.

    Deliberately has no allowlist. A date fixing a rule's origin is legitimate, a
    date recording a measurement is not, and no regex separates them. An inert
    allowlist nobody prunes would be worse than a warning somebody reads.
    """
    return [
        Finding("dated", relative, str(number))
        for number, line in enumerate(text.splitlines(), 1)
        if ISO_DATE.search(line)
    ]


def check_orphans(config: Config, referenced: set[str]) -> list[Finding]:
    """Report evidence files no instruction file points at.

    A symptom index is the only thing that loads these, so an unindexed file is
    unreachable regardless of how good its contents are.
    """
    evidence_root = config.root / config.evidence_dir
    if not evidence_root.is_dir():
        return []
    findings: list[Finding] = []
    for path in sorted(evidence_root.glob("*.md")):
        relative = path.relative_to(config.root).as_posix()
        if relative not in referenced:
            findings.append(
                Finding("orphaned", relative, "no instruction file indexes it")
            )
    return findings


def run_checks(config: Config) -> tuple[list[Finding], list[Finding], int]:
    """Scan the tree.

    Returns:
        Failing findings, date warnings, and the number of files measured.
    """
    findings: list[Finding] = []
    warnings: list[Finding] = []
    referenced: set[str] = set()
    checked = 0

    for relative, path in iter_context_files(config):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(Finding("unreadable", relative, str(error)))
            continue
        checked += 1
        findings.extend(check_links(relative, path, text, config, referenced))
        findings.extend(check_budget(relative, text, config))
        warnings.extend(check_dates(relative, text))

    findings.extend(check_orphans(config, referenced))
    return findings, warnings, checked


def parse_budget_override(value: str) -> tuple[str, int]:
    """Parse one `PATH=N` override, rejecting anything ambiguous."""
    path, separator, count = value.partition("=")
    if not separator or not path:
        raise argparse.ArgumentTypeError(
            f"expected PATH=N, got {value!r}; for example AGENTS.md=2400"
        )
    try:
        return path, int(count)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"budget for {path!r} must be an integer, got {count!r}"
        ) from None


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line interface."""
    parser = argparse.ArgumentParser(
        prog="check_agent_context.py",
        description=(
            "Report instruction files that outgrew their budget or lost their evidence."
        ),
        epilog=(
            "Findings: dangling (an evidence link that does not resolve), "
            "orphaned (an evidence file nothing indexes), oversize (over budget), "
            "escapes (a link leaving the root), unreadable. Dated lines are "
            "reported as warnings and never fail the run. "
            "Exit 0 clean, 1 findings, 2 bad invocation. "
            "Example: check_agent_context.py . --budget-for AGENTS.md=2400"
        ),
    )
    parser.add_argument(
        "root", nargs="?", default=".", help="repository root (default: .)"
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=DEFAULT_BUDGET,
        help=f"word ceiling per instruction file (default: {DEFAULT_BUDGET})",
    )
    parser.add_argument(
        "--budget-for",
        action="append",
        default=[],
        metavar="PATH=N",
        type=parse_budget_override,
        help="ceiling for one file; repeatable",
    )
    parser.add_argument(
        "--evidence-dir",
        default=DEFAULT_EVIDENCE_DIR,
        help=f"directory holding evidence files (default: {DEFAULT_EVIDENCE_DIR})",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="skip matching paths, in addition to the built-in defaults; repeatable",
    )
    parser.add_argument(
        "--names",
        default=",".join(DEFAULT_NAMES),
        help=f"instruction filenames (default: {','.join(DEFAULT_NAMES)})",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable output on stdout"
    )
    return parser


def report_text(
    findings: Sequence[Finding], warnings: Sequence[Finding], checked: int
) -> None:
    """Write the human-readable report to stdout."""
    for finding in findings:
        print(f"{finding.kind:<10} {finding.path}: {finding.detail}")
    for warning in warnings:
        print(f"{warning.kind:<10} {warning.path}:{warning.detail}")
    print(
        f"\n{checked} instruction file(s) checked, {len(findings)} finding(s), "
        f"{len(warnings)} dated line(s) to review"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. See module docstring for the contract."""
    args = build_parser().parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: not a directory: {args.root}", file=sys.stderr)
        return EXIT_USAGE

    config = Config(
        root=root,
        budget=args.budget,
        budget_for=dict(args.budget_for),
        evidence_dir=args.evidence_dir.strip("/"),
        names=tuple(n.strip() for n in args.names.split(",") if n.strip()),
        excludes=DEFAULT_EXCLUDES + tuple(args.exclude),
    )
    if not config.names:
        print("error: --names resolved to nothing", file=sys.stderr)
        return EXIT_USAGE

    findings, warnings, checked = run_checks(config)

    if args.json:
        print(
            json.dumps(
                {
                    "checked": checked,
                    "findings": [f._asdict() for f in findings],
                    "warnings": [w._asdict() for w in warnings],
                },
                indent=2,
            )
        )
    else:
        report_text(findings, warnings, checked)

    if findings:
        print(
            "Relocate evidence into the evidence directory and index it by "
            "symptom, then re-run.",
            file=sys.stderr,
        )
        return EXIT_FINDINGS
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
