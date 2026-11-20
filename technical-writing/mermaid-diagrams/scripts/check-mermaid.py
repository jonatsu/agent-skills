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
    python3 check-mermaid.py docs/*.md diagrams/flow.mmd
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROGRAM = "check-mermaid"
DEFAULT_RENDERER = "mermaidx"
INSTALL_HINT = "hint: install it with `pipx install mermaidx` or `mise use -g pipx:mermaidx`"
EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
RENDER_TIMEOUT_SECONDS = 60
DIAGRAM_SUFFIXES = {".mmd", ".mermaid"}

OPENING_FENCE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})\s*mermaid\b")
PARSE_LINE = re.compile(r"\bon line (\d+)")
FAILURE_PREFIX = re.compile(r"^.*?Mermaid rendering failed:\s*(?:Error:\s*)?")
# Quiet, diagram source on stdin, SVG on stdout. The SVG is discarded: mermaidx needs an output to run a full
# render, and only a full render reaches the errors a parse alone would miss.
RENDER_ARGUMENTS = ("-q", "-i", "-", "-f", "svg", "-o", "-")


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


def closing_fence_pattern(fence: str) -> re.Pattern[str]:
    """Match the line that closes a fence: the same character, at least as many times, indented up to three."""
    return re.compile(rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$")


def strip_fence_indent(line: str, width: int) -> str:
    """Remove up to `width` leading spaces, as CommonMark does for the lines of an indented fence.

    Any indentation beyond the fence's own stays, because diagram types such as mindmap read it.
    """
    leading = len(line) - len(line.lstrip(" "))
    return line[min(width, leading) :]


def markdown_diagrams(path: Path, text: str) -> list[Diagram]:
    """Return every fenced mermaid block in a Markdown text.

    A fence with no closing line runs to the end of the file, as CommonMark specifies.
    """
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
        closing = closing_fence_pattern(fence)
        start = index
        while index < len(lines) and not closing.match(lines[index]):
            index += 1
        body = [strip_fence_indent(line, indent) for line in lines[start:index]]
        # `start` indexes the first body line from 0; files number lines from 1.
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
    """Reduce mermaidx's error output to one line, and the diagram line it names.

    On a parse error mermaidx prints a Python traceback ending in
    `RuntimeError: Mermaid rendering failed: Error: Parse error on line N:`, then an excerpt of the source with a
    caret, then `Expecting ..., got ...`. N counts from 1 within the diagram source, not the file. The message keeps
    the error line and the first `Expecting` line; the excerpt does not fit on one line.
    """
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    for position, line in enumerate(lines):
        if "Mermaid rendering failed" in line:
            message = FAILURE_PREFIX.sub("", line)
            expecting = next(
                (candidate for candidate in lines[position + 1 :] if candidate.startswith("Expecting")),
                None,
            )
            if expecting:
                message = f"{message} {expecting}"
            parse_line_match = PARSE_LINE.search(message)
            return message, int(parse_line_match.group(1)) if parse_line_match else None
    # Without the marker, the last line of output is the best one-line summary there is.
    return (lines[-1] if lines else "mermaidx failed with no message"), None


def file_line(diagram: Diagram, diagram_line: int | None) -> int:
    """Turn a line number within the diagram source into a line of its file; without one, use the diagram's start."""
    if diagram_line is None:
        return diagram.first_line
    return diagram.first_line + diagram_line - 1


def render(diagram: Diagram, mermaidx: str) -> Failure | None:
    """Render one diagram, returning its failure or None when it renders."""
    try:
        result = subprocess.run(
            [mermaidx, *RENDER_ARGUMENTS],
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
    return Failure(diagram.path, file_line(diagram, diagram_line), message)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=f"{PROGRAM}.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.add_argument("files", nargs="+", type=Path, metavar="FILE", help="Markdown, .mmd, or .mermaid file")
    _ = parser.add_argument(
        "--mermaidx",
        default=DEFAULT_RENDERER,
        metavar="PATH",
        help=f"mermaidx executable (default: {DEFAULT_RENDERER})",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    arguments = parse_arguments(argv)
    files: list[Path] = arguments.files
    requested: str = arguments.mermaidx
    mermaidx = shutil.which(requested)
    if mermaidx is None:
        print(
            f"{PROGRAM}: error: mermaidx not found: {requested}\n{INSTALL_HINT}",
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
