#!/usr/bin/env python3
"""Check that every Mermaid diagram in Markdown or .mmd files renders.

Each fenced ``mermaid`` block in a Markdown file, and each whole .mmd or .mermaid
file, is piped to mermaidx (https://github.com/MohammadRaziei/mermaidx), which
renders offline without a browser. A diagram that fails prints one line on
stdout, ``path:line: message``, with the line in the file where Mermaid found
the error. A summary goes to stderr.

Standard library only; mermaidx must be on PATH or named with --mermaidx.

Exit status: 0 when every diagram renders, 1 when one or more fail, 2 on a usage
error, a missing file, or a missing mermaidx.

Example:
    python3 check_mermaid.py docs/*.md diagrams/flow.mmd
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROGRAM = "check_mermaid"
EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
RENDER_TIMEOUT_SECONDS = 60
DIAGRAM_SUFFIXES = {".mmd", ".mermaid"}

OPENING_FENCE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})\s*mermaid\b")
PARSE_LINE = re.compile(r"\bon line (\d+)")
FAILURE_PREFIX = re.compile(r"^.*?Mermaid rendering failed:\s*(?:Error:\s*)?")


@dataclass(frozen=True)
class Diagram:
    """One Mermaid diagram and the file line its first source line sits on."""

    path: Path
    first_line: int
    source: str


@dataclass(frozen=True)
class Failure:
    """A diagram that did not render, located at a line of its file."""

    path: Path
    line: int
    message: str


def markdown_diagrams(path: Path, text: str) -> list[Diagram]:
    """Return every fenced mermaid block in a Markdown text."""
    diagrams: list[Diagram] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        opening = OPENING_FENCE.match(lines[index])
        index += 1
        if not opening:
            continue
        fence = opening["fence"]
        indent = len(opening["indent"])
        closing = re.compile(rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        start = index
        while index < len(lines) and not closing.match(lines[index]):
            index += 1
        body = [
            line[indent:] if line[:indent].isspace() else line.lstrip()
            for line in lines[start:index]
        ]
        diagrams.append(Diagram(path, start + 1, "\n".join(body) + "\n"))
        index += 1
    return diagrams


def diagrams_in(path: Path) -> list[Diagram]:
    """Return the diagrams a file holds: the whole file for .mmd, the fenced blocks otherwise."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in DIAGRAM_SUFFIXES:
        return [Diagram(path, 1, text)]
    return markdown_diagrams(path, text)


def failure_message(stderr: str) -> tuple[str, int | None]:
    """Reduce mermaidx's error output to one line, and the diagram line it names."""
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    for position, line in enumerate(lines):
        if "Mermaid rendering failed" in line:
            message = FAILURE_PREFIX.sub("", line)
            expecting = [later for later in lines[position + 1 :] if later.startswith("Expecting")]
            if expecting:
                message = f"{message} {expecting[0]}"
            number = PARSE_LINE.search(message)
            return message, int(number.group(1)) if number else None
    return (lines[-1] if lines else "mermaidx failed with no message"), None


def render(diagram: Diagram, mermaidx: str) -> Failure | None:
    """Render one diagram, returning its failure or None when it renders."""
    try:
        result = subprocess.run(
            [mermaidx, "-q", "-i", "-", "-f", "svg", "-o", "-"],
            input=diagram.source,
            capture_output=True,
            text=True,
            timeout=RENDER_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return Failure(
            diagram.path,
            diagram.first_line,
            f"rendering timed out after {RENDER_TIMEOUT_SECONDS} s",
        )
    if result.returncode == 0:
        return None
    message, diagram_line = failure_message(result.stderr)
    line = diagram.first_line + diagram_line - 1 if diagram_line else diagram.first_line
    return Failure(diagram.path, line, message)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="check_mermaid.py",
        description="Check that every Mermaid diagram in Markdown or .mmd files renders, using mermaidx.",
        epilog="Example: python3 check_mermaid.py docs/*.md diagrams/flow.mmd",
    )
    _ = parser.add_argument(
        "files", nargs="+", type=Path, metavar="FILE", help="Markdown, .mmd, or .mermaid file"
    )
    _ = parser.add_argument(
        "--mermaidx",
        default="mermaidx",
        metavar="PATH",
        help="mermaidx executable (default: mermaidx)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    arguments = parse_arguments(argv)
    files: list[Path] = arguments.files
    requested: str = arguments.mermaidx
    mermaidx = shutil.which(requested)
    if mermaidx is None:
        print(
            f"{PROGRAM}: error: mermaidx not found: {requested}\n"
            + "hint: install it with `pipx install mermaidx` or `mise use -g pipx:mermaidx`",
            file=sys.stderr,
        )
        return EXIT_USAGE
    diagrams: list[Diagram] = []
    for path in files:
        try:
            diagrams.extend(diagrams_in(path))
        except (OSError, UnicodeDecodeError) as error:
            print(f"{PROGRAM}: error: cannot read {path}: {error}", file=sys.stderr)
            return EXIT_USAGE
    failures = [failure for diagram in diagrams if (failure := render(diagram, mermaidx))]
    for failure in failures:
        print(f"{failure.path}:{failure.line}: {failure.message}")
    print(f"{PROGRAM}: {len(diagrams)} diagram(s) checked, {len(failures)} failed", file=sys.stderr)
    return EXIT_FAILED if failures else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
