#!/usr/bin/env python3
"""Report or rewrap Markdown prose lines that exceed a width limit.

A rewrapped paragraph, list item or quote ends every line but its last with a
trailing-backslash hard break, so the rendered output keeps the source's line
lengths instead of joining them into one long line. Front matter, headings,
tables, fenced and indented code, link reference definitions, HTML blocks,
thematic breaks, setext underlines and GitHub alert markers are left alone. A
block that already fits the limit with the hard-break convention is untouched.

Exit status: 0 when nothing needs rewrapping or --write rewrote the files, 1
when check mode found blocks to rewrap, 2 on a usage or file error.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

DEFAULT_WIDTH = 120
EXIT_CLEAN = 0
EXIT_WOULD_CHANGE = 1
EXIT_ERROR = 2
HARD_BREAK = "\\"
CODE_INDENT = 4

FENCE = re.compile(r"^\s{0,3}(```+|~~~+)")
TABLE = re.compile(r"^\s*\|")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s")
HEADING = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
# An HTML block opens with a tag, a closing tag, a comment, or a declaration. An
# autolink such as <https://example.com> is inline text and stays prose.
HTML = re.compile(r"^\s{0,3}<(?:[A-Za-z][A-Za-z0-9-]*(?:[\s/>]|$)|/[A-Za-z]|[!?])")
# A thematic break (---, ***, ___) or a setext heading underline (=== or ---) is
# structure; joined into a paragraph it would become text.
RULE = re.compile(r"^\s{0,3}(?:([-*_])(?:[ \t]*\1){2,}|=+)[ \t]*$")
# YAML (---) or TOML (+++) front matter, only as the file's first line. YAML may
# also close with "...".
FRONT_MATTER_CLOSE = {"---": ("---", "..."), "+++": ("+++",)}
BULLET = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
# The quote marker is structure, not text: it is stripped before wrapping and
# re-applied to every produced line. A GitHub alert marker owns its own line.
QUOTE = re.compile(r"^\s{0,3}(?:> ?)+")
ALERT = re.compile(r"^\s{0,3}(?:> ?)+\[!")
# A word that would open a new block if a wrap put it first on a line: a list
# marker, an ATX heading, a quote, a setext underline, a fence, or an HTML tag.
# Each of these can interrupt a paragraph, so the word must not start a line. An
# autolink such as <https://example.com> is not tag-shaped and may start a line.
BLOCK_START = re.compile(
    r"^(?:[-+*]|\d{1,9}[.)]|#{1,6}|>.*|=+|-+|```.*|~~~.*|<[!?].*|</?[A-Za-z][A-Za-z0-9-]*(?:/?>.*)?)$"
)


def front_matter_end(lines: Sequence[str]) -> int:
    """Return how many leading lines are front matter, 0 when there is none."""
    closers = FRONT_MATTER_CLOSE.get(lines[0].rstrip()) if lines else None
    if not closers:
        return 0
    for index in range(1, len(lines)):
        if lines[index].rstrip() in closers:
            return index + 1
    return 0  # never closed, so not front matter


def quote_prefix(line: str) -> str:
    match = QUOTE.match(line)
    return match.group(0) if match else ""


def classify(lines: Sequence[str]) -> list[bool]:
    """Return, per line, whether it is prose the wrapper may touch."""
    start = front_matter_end(lines)
    prose = [False] * start
    fence = ""
    in_indented_code = False
    previous_blank = True
    for line in lines[start:]:
        match = FENCE.match(line)
        if fence:
            prose.append(False)
            closer = match.group(1) if match else ""
            if closer[:1] == fence[0] and len(closer) >= len(fence):
                fence = ""
            continue
        if match:
            fence = match.group(1)
            prose.append(False)
            continue
        body = line[len(quote_prefix(line)) :]
        blank = not body.strip()
        indent = len(body) - len(body.lstrip(" "))
        # Indented code starts after a blank line and runs through blank lines
        # until a line indents less. List continuations indented as deep also
        # stop here, which only leaves them unwrapped.
        if not blank and indent >= CODE_INDENT and (previous_blank or in_indented_code):
            in_indented_code = True
        elif not blank:
            in_indented_code = False
        previous_blank = blank
        structural = (
            TABLE.match(body)
            or REFERENCE_DEFINITION.match(body)
            or HTML.match(body)
            or RULE.match(body)
            or ALERT.match(line)
        )
        prose.append(not (in_indented_code or structural))
    return prose


def blocks(lines: Sequence[str], prose: Sequence[bool]) -> list[list[int]]:
    """Group consecutive prose lines into blocks: a paragraph, list item or quote."""
    found: list[list[int]] = []
    current: list[int] = []
    for index, line in enumerate(lines):
        body = line[len(quote_prefix(line)) :]
        if not prose[index] or not body.strip() or HEADING.match(body):
            if current:
                found.append(current)
                current = []
            continue
        # A list marker, or a change of quote depth, starts a new block.
        if current and (
            BULLET.match(body) or quote_prefix(lines[current[-1]]) != quote_prefix(line)
        ):
            found.append(current)
            current = []
        current.append(index)
    if current:
        found.append(current)
    return found


def split_tokens(text: str) -> list[str]:
    """Split on spaces, but never inside a code span, link text, or link target."""
    tokens: list[str] = []
    buffer = ""
    in_code = False
    index = 0
    while index < len(text):
        character = text[index]
        if character == "`":
            in_code = not in_code
            buffer += character
        elif character in "[(" and not in_code and (character == "[" or buffer.endswith("]")):
            # A hard break inside link text renders inside the link, so the whole
            # link stays one token even when it overflows the limit.
            closing = "]" if character == "[" else ")"
            depth = 1
            buffer += character
            index += 1
            while index < len(text) and depth:
                if text[index] == character:
                    depth += 1
                elif text[index] == closing:
                    depth -= 1
                buffer += text[index]
                index += 1
            continue
        elif character == " " and not in_code:
            if buffer:
                tokens.append(buffer)
                buffer = ""
        else:
            buffer += character
        index += 1
    if buffer:
        tokens.append(buffer)
    return tokens


def fill(tokens: Sequence[str], room: int, continued_room: int) -> list[list[str]]:
    """Pack tokens into lines; never start a line with a block-opening word."""
    lines: list[list[str]] = [[]]
    for token in tokens:
        current = lines[-1]
        limit = room if len(lines) == 1 else continued_room
        if not current or len(" ".join([*current, token])) <= limit:
            current.append(token)
            continue
        carried = [token]
        while BLOCK_START.match(carried[0]) and len(current) > 1:
            carried.insert(0, current.pop())
        if BLOCK_START.match(carried[0]):
            current.extend(carried)  # nothing left to carry; overflow instead
            continue
        lines.append(carried)
    return lines


def rewrap(lines: Sequence[str], indexes: Sequence[int], width: int) -> list[str]:
    quote = quote_prefix(lines[indexes[0]])
    first = lines[indexes[0]][len(quote) :]
    bullet = BULLET.match(first)
    lead = bullet.group(0) if bullet else first[: len(first) - len(first.lstrip())]
    continuation = " " * len(lead) if bullet else lead

    parts: list[str] = []
    for position, index in enumerate(indexes):
        raw = lines[index][len(quote_prefix(lines[index])) :].rstrip()
        raw = raw.removesuffix(HARD_BREAK).rstrip()
        if position == 0:
            raw = raw[len(lead) :]
        parts.append(raw.strip())
    tokens = split_tokens(" ".join(part for part in parts if part))

    # Every line but the last carries the hard break, so reserve its column.
    reserve = len(quote) + len(HARD_BREAK)
    packed = fill(tokens, width - reserve - len(lead), width - reserve - len(continuation))
    text = [" ".join(words) for words in packed]
    produced = [lead + text[0]] + [continuation + line for line in text[1:]]
    produced = [line + HARD_BREAK for line in produced[:-1]] + produced[-1:]
    return [quote + line for line in produced]


def conformant(lines: Sequence[str], indexes: Sequence[int], width: int) -> bool:
    """Whether a block already fits: no line over the limit, every line but the last
    ending in a hard break, and the last line not ending in one."""
    body = [lines[index].rstrip() for index in indexes]
    if any(len(line) > width for line in body):
        return False
    return all(line.endswith(HARD_BREAK) for line in body[:-1]) and not body[-1].endswith(
        HARD_BREAK
    )


def process(path: Path, width: int, write: bool) -> list[tuple[int, int, int]]:
    """Return (line, old count, new count) per changed block; rewrite the file if asked."""
    lines = path.read_text(encoding="utf-8").split("\n")
    prose = classify(lines)
    result: list[list[str]] = [[line] for line in lines]
    changed: list[tuple[int, int, int]] = []
    for indexes in blocks(lines, prose):
        if conformant(lines, indexes, width):
            continue
        new = rewrap(lines, indexes, width)
        old = [lines[index] for index in indexes]
        if new == old:
            continue
        changed.append((indexes[0] + 1, len(old), len(new)))
        result[indexes[0]] = new
        for index in indexes[1:]:
            result[index] = []
    if write and changed:
        path.write_text("\n".join(line for group in result for line in group), encoding="utf-8")
    return changed


def positive_width(value: str) -> int:
    width = int(value)
    if width < 20:
        raise argparse.ArgumentTypeError("width must be at least 20")
    return width


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report or rewrap Markdown prose over a width limit, using "
        "trailing-backslash hard breaks. Reports by default; --write rewrites."
    )
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files to check")
    parser.add_argument(
        "--width",
        type=positive_width,
        default=DEFAULT_WIDTH,
        help=f"maximum line length (default {DEFAULT_WIDTH})",
    )
    parser.add_argument("--write", action="store_true", help="rewrite the files in place")
    options = parser.parse_args(arguments)

    total = 0
    for path in options.files:
        try:
            changed = process(path, options.width, options.write)
        except (OSError, UnicodeDecodeError) as error:
            print(f"mdwrap: {path}: {error}", file=sys.stderr)
            return EXIT_ERROR
        total += len(changed)
        if not options.write:
            for line, old, new in changed:
                print(f"{path}:{line}: {old} -> {new} lines")
    print(f"{total} block(s) {'rewrapped' if options.write else 'would change'}")
    return EXIT_WOULD_CHANGE if total and not options.write else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
