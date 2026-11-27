#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=4.3,<5", "mdit-py-plugins>=0.7,<1"]
# ///
"""Prove that rewriting a Markdown document left every code block untouched.

Give the script the version before the rewrite (OLD) and the version after (NEW). It finds the code blocks of
each file in document order with a CommonMark parser and compares them as exact text. A code block is a fenced
block (Mermaid diagrams are fences) or an indented block; front matter is not one.

The parser supplies only where each block sits, never what it holds: its token content has CRLF and lone CR
line endings turned into LF, NUL characters replaced, and indentation stripped. The script therefore cuts each
block out of the original file by the parser's line range and compares those lines byte for byte. A block's
text includes its fence lines, so the info string (the language tag), the fence characters and their count, the
indentation, trailing whitespace, every line ending and every character inside the block all count. A block
inside a list or quote carries that nesting prefix, so re-indenting a whole list counts as a change to each
fenced block in it. The script reads files as UTF-8 and keeps their line endings.

Blocks pair by position when both files hold the same number of them. When the counts differ, the script
aligns the two sequences with `difflib.SequenceMatcher`, so one inserted or deleted block does not make every
later block look changed: identical blocks match, and what falls between them pairs by position as changed,
with any surplus reported as missing from NEW or added in NEW.

The script never runs git. Produce the old version yourself, for example with
`git show HEAD:docs/guide.md > /tmp/old.md`.

Prints one finding per line, in document order, with non-printing and non-ASCII characters escaped Python-style
(`\\u2192`, `\\xa0`, `\\r`) so a swapped look-alike is readable in a terminal. Line numbers are 1-based:

    OLD block 3 (line 12), NEW block 3 (line 14): block line 2 differs: OLD 'a \\\\\\n' NEW 'a\\n'
    OLD block 2 (line 8): missing from NEW
    NEW block 4 (line 30): added, absent from OLD

A block line counts from the block's first line, which is its opening fence for a fenced block. The summary goes
to stderr as `codeblocks: N block(s) in OLD, M in NEW, C changed, X missing, Y added`.

Exit status: 0 when every block is identical and the counts match, 1 when any difference is reported, 2 for a
usage error, an unreadable or undecodable file or a missing dependency.
"""

from __future__ import annotations

import argparse
import difflib
import itertools
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

try:
    from markdown_it import MarkdownIt
    from mdit_py_plugins.front_matter import front_matter_plugin
except ImportError as error:  # a runner that ignored the inline script metadata above
    print(f"codeblocks.py: error: cannot import a required package: {error}", file=sys.stderr)
    print(
        "hint: run it as `uv run scripts/codeblocks.py`, which installs the dependencies",
        file=sys.stderr,
    )
    sys.exit(2)

SCRIPT = "codeblocks.py"
EXIT_CLEAN = 0
EXIT_DIFFERENCES = 1
EXIT_ERROR = 2

CODE_TOKENS = frozenset({"fence", "code_block"})
# One line with its ending, the way the parser splits: CRLF, CR or LF. `str.splitlines` also splits on
# characters such as U+2028, which would shift line numbers.
LINE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+")
NO_LINE = "(no line)"


class CheckError(Exception):
    """A failure that ends the run with exit status 2."""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.hint = hint


class ArgumentParser(argparse.ArgumentParser):
    """An argparse parser whose usage errors follow this script's error format."""

    def error(self, message: str) -> NoReturn:
        print(f"{SCRIPT}: error: invalid arguments: {message}", file=sys.stderr)
        print(f"hint: run `{SCRIPT} --help` for the usage", file=sys.stderr)
        sys.exit(EXIT_ERROR)


@dataclass(frozen=True)
class Block:
    """One code block as written in the file: its text from the first line to the last, with line endings."""

    line: int  # 1-based line of the block's first line
    text: str

    def lines(self) -> list[str]:
        return LINE.findall(self.text)


@dataclass
class Tally:
    """The findings of one comparison."""

    findings: list[str]
    changed: int = 0
    missing: int = 0
    added: int = 0


def read(path: Path) -> str:
    """Return the file's text with its line endings intact; `Path.read_text` would translate them."""
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        cause = error.strerror if isinstance(error, OSError) and error.strerror else str(error)
        raise CheckError(f"cannot read {path}: {cause}") from error


def extract_blocks(text: str) -> list[Block]:
    """Return the code blocks of `text` in document order, each cut from `text` by the parser's line range."""
    lines = LINE.findall(text)
    parser = MarkdownIt("commonmark").use(front_matter_plugin)
    blocks: list[Block] = []
    for token in parser.parse(text):
        if token.type not in CODE_TOKENS:
            continue
        assert token.map is not None, "the parser maps every fence and code block"
        start, end = token.map
        # An unclosed fence at the end of the file can map one line past it; slicing clamps that.
        blocks.append(Block(start + 1, "".join(lines[start:end])))
    return blocks


def visible(line: str | None) -> str:
    """Return `line` with non-printing and non-ASCII characters escaped, or a marker when the block has no such line."""
    return NO_LINE if line is None else ascii(line)


def describe_difference(old: Block, new: Block) -> str:
    """Return the first differing line of two blocks, as `block line N differs: OLD ... NEW ...`."""
    pairs = itertools.zip_longest(old.lines(), new.lines())
    for number, (old_line, new_line) in enumerate(pairs, start=1):
        if old_line != new_line:
            return f"block line {number} differs: OLD {visible(old_line)} NEW {visible(new_line)}"
    raise AssertionError("two different blocks have no differing line")


def pair_changed(old: list[Block], new: list[Block], old_index: int, new_index: int, tally: Tally) -> None:
    """Compare the blocks at two 0-based indices; report a difference."""
    if old[old_index].text == new[new_index].text:
        return
    tally.changed += 1
    tally.findings.append(
        f"OLD block {old_index + 1} (line {old[old_index].line}), NEW block {new_index + 1} "
        f"(line {new[new_index].line}): {describe_difference(old[old_index], new[new_index])}"
    )


def report_missing(old: list[Block], index: int, tally: Tally) -> None:
    tally.missing += 1
    tally.findings.append(f"OLD block {index + 1} (line {old[index].line}): missing from NEW")


def report_added(new: list[Block], index: int, tally: Tally) -> None:
    tally.added += 1
    tally.findings.append(f"NEW block {index + 1} (line {new[index].line}): added, absent from OLD")


def compare(old: list[Block], new: list[Block]) -> Tally:
    """Pair the blocks and report each difference; see the module docstring for the pairing rules."""
    tally = Tally(findings=[])
    if len(old) == len(new):
        for index in range(len(old)):
            pair_changed(old, new, index, index, tally)
        return tally
    matcher = difflib.SequenceMatcher(
        None, [block.text for block in old], [block.text for block in new], autojunk=False
    )
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        shared = min(old_end - old_start, new_end - new_start)
        for offset in range(shared):
            pair_changed(old, new, old_start + offset, new_start + offset, tally)
        for index in range(old_start + shared, old_end):
            report_missing(old, index, tally)
        for index in range(new_start + shared, new_end):
            report_added(new, index, tally)
    return tally


def build_argument_parser() -> argparse.ArgumentParser:
    parser = ArgumentParser(
        prog=SCRIPT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Prove that rewriting a Markdown document left every code block untouched: report each "
        "block that differs between OLD, the version before, and NEW, the version after.",
        epilog="example:\n"
        "  git show HEAD:docs/guide.md > /tmp/old.md\n"
        "  uv run scripts/codeblocks.py /tmp/old.md docs/guide.md\n"
        "\n"
        "Prints one line per differing, missing or added block. Exits 0 when every block is identical, 1 when "
        "any differs, 2 on a usage or file error.",
    )
    parser.add_argument("old", type=Path, metavar="OLD", help="the Markdown file before the rewrite")
    parser.add_argument("new", type=Path, metavar="NEW", help="the Markdown file after the rewrite")
    return parser


def run(arguments: Sequence[str] | None) -> int:
    options = build_argument_parser().parse_args(arguments)
    old = extract_blocks(read(options.old))
    new = extract_blocks(read(options.new))
    tally = compare(old, new)
    for finding in tally.findings:
        print(finding)
    print(
        f"codeblocks: {len(old)} block(s) in OLD, {len(new)} in NEW, {tally.changed} changed, "
        f"{tally.missing} missing, {tally.added} added",
        file=sys.stderr,
    )
    return EXIT_DIFFERENCES if tally.findings else EXIT_CLEAN


def main(arguments: Sequence[str] | None = None) -> int:
    try:
        return run(arguments)
    except CheckError as error:
        print(f"{SCRIPT}: error: {error}", file=sys.stderr)
        if error.hint:
            print(f"hint: {error.hint}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
