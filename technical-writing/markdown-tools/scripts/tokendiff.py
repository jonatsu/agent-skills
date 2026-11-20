#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=4.3,<5", "mdit-py-plugins>=0.7,<1"]
# ///
"""Prove that moving, merging or splitting Markdown documents dropped no words.

The script counts word tokens in the source files and in the destination files, pools each side, and reports
every token the destination has fewer occurrences of. Pooling means a word may move between files freely: only
a word that disappears from the whole destination set, or appears fewer times, is a loss.

A token is a run of letters, digits, `_`, `-`, `.` and `/` that holds at least one letter or digit, compared
case-sensitively, with trailing `.` and `-` removed. The CommonMark parser decides what counts. These are
skipped: front matter, fenced and indented code blocks (Mermaid diagrams are fences), HTML comments, and inline
HTML tags. The content of inline code spans counts, and so does the text of an HTML block outside its tags.
Link destinations, link titles and reference definitions do not count, because a move rewrites them; check them
with a link checker instead. Image alt text counts.

Words deleted on purpose are removed from both sides with `--ignore WORD` (repeatable) or `--ignore-file FILE`,
which holds one word per line; blank lines are skipped.

Prints one line per lost token, the largest loss first, as `token: lost N of M`, where M is the token's count in
the sources. Exit status: 0 when nothing is lost, 1 when anything is lost, 2 for a usage error, an unreadable
file or a missing dependency.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import NoReturn

try:
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
    from mdit_py_plugins.front_matter import front_matter_plugin
except ImportError as error:  # a runner that ignored the inline script metadata above
    print(f"tokendiff.py: error: cannot import a required package: {error}", file=sys.stderr)
    print(
        "hint: run it as `uv run scripts/tokendiff.py`, which installs the dependencies",
        file=sys.stderr,
    )
    sys.exit(2)

SCRIPT = "tokendiff.py"
EXIT_CLEAN = 0
EXIT_LOST = 1
EXIT_ERROR = 2

TOKEN = re.compile(r"[\w./-]+")
HTML_COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)
HTML_TAG = re.compile(r"<[^>]*>")


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


def words(text: str) -> list[str]:
    """Return the word tokens of `text`: trailing `.` and `-` stripped, and each one holding a letter or digit."""
    found: list[str] = []
    for match in TOKEN.finditer(text):
        token = match.group(0).rstrip(".-")
        if any(character.isalnum() for character in token):
            found.append(token)
    return found


def visible_text(parsed: Iterable[Token]) -> Iterable[str]:
    """Yield the text a reader sees, chunk by chunk, from the parser's block and inline tokens."""
    for token in parsed:
        if token.type == "inline":
            for child in token.children or []:
                # Inline HTML is one tag or comment, so it never carries words. Image alt text is the
                # image token's content.
                if child.type in ("text", "code_inline", "image"):
                    yield child.content
        elif token.type == "html_block":
            yield HTML_TAG.sub(" ", HTML_COMMENT.sub(" ", token.content))
        # fence, code_block and front_matter tokens hold no inline children and are skipped here.


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        cause = error.strerror if isinstance(error, OSError) and error.strerror else str(error)
        raise CheckError(f"cannot read {path}: {cause}") from error


def count_file(path: Path) -> Counter[str]:
    text = read(path)
    parser = MarkdownIt("commonmark").use(front_matter_plugin)
    counts: Counter[str] = Counter()
    for chunk in visible_text(parser.parse(text)):
        counts.update(words(chunk))
    return counts


def pool(paths: Sequence[Path]) -> Counter[str]:
    total: Counter[str] = Counter()
    for path in paths:
        total.update(count_file(path))
    return total


def read_ignore_file(path: Path) -> list[str]:
    return [line.strip() for line in read(path).splitlines() if line.strip()]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = ArgumentParser(
        prog=SCRIPT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Prove that moving, merging or splitting Markdown documents dropped no words: report each "
        "word token the destination files have fewer occurrences of than the source files.",
        epilog="example:\n"
        "  uv run scripts/tokendiff.py --from docs/old-guide.md --to docs/guide.md docs/reference.md "
        "--ignore-file /tmp/deleted-words.txt\n"
        "\n"
        "Prints `token: lost N of M` per lost token. Exits 0 when nothing is lost, 1 when anything is lost, "
        "2 on a usage or file error.",
    )
    parser.add_argument(
        "--from",
        dest="sources",
        nargs="+",
        required=True,
        type=Path,
        metavar="FILE",
        help="source files, before the restructure",
    )
    parser.add_argument(
        "--to",
        dest="destinations",
        nargs="+",
        required=True,
        type=Path,
        metavar="FILE",
        help="destination files, after the restructure",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="WORD",
        help="word to leave out of the comparison; repeatable",
    )
    parser.add_argument(
        "--ignore-file",
        action="append",
        default=[],
        type=Path,
        metavar="FILE",
        help="file of words to leave out, one per line; repeatable",
    )
    return parser


def run(arguments: Sequence[str] | None) -> int:
    options = build_argument_parser().parse_args(arguments)
    ignored = set(options.ignore)
    for path in options.ignore_file:
        ignored.update(read_ignore_file(path))
    source = pool(options.sources)
    destination = pool(options.destinations)
    for word in ignored:
        # Deleting a key a Counter does not hold is a no-op, so an ignored word absent from a side is fine.
        del source[word]
        del destination[word]
    lost = {
        token: count - destination[token]
        for token, count in source.items()
        if count > destination[token]
    }
    for token in sorted(lost, key=lambda name: (-lost[name], name)):
        print(f"{token}: lost {lost[token]} of {source[token]}")
    print(
        f"tokendiff: {source.total()} source token(s), {sum(lost.values())} lost occurrence(s), "
        f"{len(lost)} distinct token(s) short",
        file=sys.stderr,
    )
    return EXIT_LOST if lost else EXIT_CLEAN


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
