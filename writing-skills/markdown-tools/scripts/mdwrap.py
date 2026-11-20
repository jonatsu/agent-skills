#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=4.3,<5", "mdit-py-plugins>=0.7,<1"]
# ///
"""Rewrap Markdown paragraphs that have a line over a width limit, leaving everything else untouched.

A CommonMark parser (markdown-it-py, with tables, strikethrough, footnotes and front matter) decides what is a
paragraph, so headings, tables, HTML blocks, fenced and indented code, front matter and reference definitions
are never rewritten, wherever they sit in lists or quotes. A paragraph whose lines all fit is never touched.
Only a paragraph with a line over the limit is rewrapped, and the script reports it by default without
changing the file.

Rewrapping keeps each line's block-quote markers and list indentation. A code span, an inline HTML tag, an
autolink and a link destination are never broken. A line break the author made on purpose (two trailing spaces,
a trailing `<br>`, and with --soft a trailing backslash) splits the paragraph into segments that are wrapped
separately. No wrapped line starts with a token that would open a heading, list, quote, fence, rule, table or
HTML block, and a backslash escape that only protected a word at a line start is dropped when the word moves.

Before writing, the script renders the original and the rewrapped document with the same parser and compares
them with every soft break, hard break and whitespace run reduced to one space. A paragraph whose rewrap would
change the rendering stays as it was and is reported as skipped.

Exit status: 0 when nothing would change (check mode) or everything was rewrapped within the limit (--write), 1
when check mode found work or any paragraph was skipped or left over the limit, 2 for a usage error, an
unreadable file or a missing dependency.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import tempfile
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple, NoReturn

try:
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
    from mdit_py_plugins.footnote import footnote_plugin
    from mdit_py_plugins.front_matter import front_matter_plugin
except ImportError as error:  # a runner that ignored the inline script metadata above
    print(f"mdwrap: error: cannot import a required package: {error}", file=sys.stderr)
    print(
        "hint: run it as `uv run scripts/mdwrap.py`, which installs the dependencies, "
        "or `pip install markdown-it-py mdit-py-plugins`",
        file=sys.stderr,
    )
    sys.exit(2)

PROGRAM = "mdwrap"
DEFAULT_WIDTH = 120
MIN_WIDTH = 20
EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2

HARD_BREAK = "\\"
SPACE_BREAK = "  "
# The ending recorded for a line that ends with any `<br>` tag; the tag itself stays in the last word.
HTML_BREAK = "<br>"
NO_BREAK = ""
# What a wrapped segment's last line carries after its words: the break markers are text, `<br>` is a word.
EMITTED_ENDING = {NO_BREAK: "", SPACE_BREAK: SPACE_BREAK, HTML_BREAK: "", HARD_BREAK: HARD_BREAK}
FOOTNOTE_INDENT = " " * 4

PUNCTUATION = frozenset("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
BACKTICKS = re.compile(r"`+")
# CommonMark's autolinks and raw inline HTML, so an atom ends where the parser says it ends.
AUTOLINK = re.compile(
    r"<(?:[A-Za-z][A-Za-z0-9+.\-]{1,31}:[^\s<>]*"
    r"|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*)>"
)
_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
_ATTRIBUTE = r"""\s+[A-Za-z_:][A-Za-z0-9_.:-]*(?:\s*=\s*(?:[^\s"'=<>`]+|'[^']*'|"[^"]*"))?"""
INLINE_HTML = re.compile(
    rf"<{_TAG_NAME}(?:{_ATTRIBUTE})*\s*/?>"
    rf"|</{_TAG_NAME}\s*>"
    r"|<!---->|<!--(?:-?[^>-])(?:-?[^-])*-->"
    r"|<\?[\s\S]*?\?>"
    r"|<![A-Za-z][^>]*>"
    r"|<!\[CDATA\[[\s\S]*?\]\]>"
)
# `](destination "title")` of an inline link or image: one unit, because a break inside it changes the target.
LINK_TARGET = re.compile(
    r"""\]\(\s*(?:<[^<>\n]*>|(?:[^\s()\\]|\\.|\((?:[^\s()\\]|\\.)*\))*)"""
    r"""(?:\s+(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\((?:[^()\\]|\\.)*\)))?\s*\)""",
    re.DOTALL,
)
BREAK_TAG_END = re.compile(r"<br\s*/?>\Z", re.IGNORECASE)
# A word that would open a block if a wrap put it first on a line: a list marker, an ATX heading, a quote, a
# setext underline, a thematic break, a fence, a table row, display math, a footnote definition or an HTML tag.
BLOCK_START = re.compile(
    r"^(?:[-+*]|\d{1,9}[.)]|#{1,6}|>.*|=+|-+|\*{3,}|_{3,}|```.*|~~~.*|\|.*|\$\$.*|\[\^[^\]]*\]:.*"
    r"|<[!?].*|</?[A-Za-z][A-Za-z0-9-]*(?:/?>.*)?)$"
)
# markdownlint's MD018 fix reads any unindented line that starts with `#` and a character other than `#`, space or tab
# as a heading missing its space, such as `#140)`, and inserts one. CommonMark reads it as text, so it is kept out
# of BLOCK_START and refused separately.
LINT_HEADING = re.compile(r"^#")
# A line that MD013's stern mode accepts however long: no whitespace after its leading `#`, `>` and spaces.
NOT_WRAPPABLE = re.compile(r"^(?:[#>\s]*\s)?\S*$")
DELIMITER_RUN = re.compile(r"^[*_~]+$")
# A line holding only one of these is a thematic break, a setext underline or a complete HTML tag (a block).
RULE_WORD = re.compile(rf"^(?:\*{{3,}}|_{{3,}}|-+|=+|<{_TAG_NAME}(?:{_ATTRIBUTE})*\s*/?>|</{_TAG_NAME}\s*>)$")
LIST_MARKER = re.compile(r"(?<![^\s>])(?:[-+*]|\d{1,9}[.)])(?=\s)")
FOOTNOTE_LABEL = re.compile(r"\[\^[^\]\s]+\]:[ ]*")
MDFORMAT_SWITCH = re.compile(r"<!--\s*mdformat\s+(off|on)\s*-->")
# The first line of real front matter is a key, a comment or a table header; prose between two rules is not.
FRONT_MATTER_START = re.compile(r"""^(?:#|\[|[\w."'/-]+\s*[:=](?:\s|$))""")
BREAK_HTML = re.compile(r"<br\s*/?>", re.IGNORECASE)
WHITESPACE = re.compile(r"\s+")
LINE_ENDING = re.compile(r"(\r\n|\n)")


@dataclass(frozen=True)
class Word:
    """A run of non-space text that wrapping never splits."""

    text: str  # as it reads in the middle of a line, without any escape that only mattered at a line start
    opening: str  # as written, which is how it reads at the start of a line


@dataclass(frozen=True)
class Segment:
    """Words between two deliberate line breaks, and the break that ends them."""

    words: tuple[Word, ...]
    ending: str  # NO_BREAK, SPACE_BREAK, HTML_BREAK or HARD_BREAK


@dataclass(frozen=True)
class Paragraph:
    start: int  # first source line, zero-based
    end: int  # one past the last source line
    content: str  # the parser's text for the paragraph, without container prefixes


@dataclass(frozen=True)
class Rewrite:
    paragraph: Paragraph
    lines: tuple[str, ...]
    over_limit: bool
    merged_breaks: int  # hard breaks of the source that the rewrap turns into ordinary wraps


class LengthMode(StrEnum):
    """How a line counts as too long; the values are markdownlint's MD013 modes."""

    DEFAULT = "default"
    STERN = "stern"
    STRICT = "strict"


class Kind(StrEnum):
    """The kind of a finding; the values are the words printed in the report."""

    REWRAP = "rewrap"
    SKIPPED = "skipped"
    OVER_LIMIT = "over limit"


@dataclass(frozen=True)
class Finding:
    line: int  # one-based
    kind: Kind
    message: str


@dataclass(frozen=True)
class Options:
    width: int
    soft: bool
    length_mode: LengthMode = LengthMode.DEFAULT


@dataclass(frozen=True)
class Outcome:
    """What rewrapping one document yields."""

    text: str | None  # the rewritten text, or None when nothing changes
    findings: tuple[Finding, ...]

    @property
    def counts(self) -> Counter[Kind]:
        """The number of findings of each kind: paragraphs rewrapped, skipped and left over the limit."""
        return Counter(finding.kind for finding in self.findings)


@dataclass(frozen=True)
class FileResult:
    path: Path
    output: bytes | None  # the rewritten file, or None when nothing changes
    outcome: Outcome


class DocumentError(Exception):
    """A file that cannot be processed; the message names what failed."""


class EmptySegment(Exception):
    """A deliberate line break with no text before it, which the script cannot place."""


def over_limit_finding(line: int, width: int) -> Finding:
    return Finding(line, Kind.OVER_LIMIT, f"a word longer than {width} characters")


def line_start_form(word: str) -> str:
    """Return the word without the backslash that only protected it at the start of a line."""
    if word[:1] == "\\" and word[1:2] in {"-", "+", "*", "#", ">", "=", "_"}:
        candidate = word[1:]
    elif match := re.fullmatch(r"(\d{1,9})\\([.)])", word):
        candidate = match.group(1) + match.group(2)
    else:
        return word
    return candidate if BLOCK_START.match(candidate) else word


class Scanner:
    """Split paragraph text into words and segments in one left-to-right pass.

    The pass follows the parser's inline precedence. A backslash escape consumes its next character, a code
    span (an opening backtick run and the next run of exactly that length) is one word-part even with spaces
    inside, and so are an autolink, an inline HTML tag and a link destination. An unmatched backtick run is
    plain text. A line that ends with two spaces or a `<br>` tag ends a segment; so does one that ends with a
    backslash when `soft` is set, otherwise that backslash is an earlier wrap and is dropped.
    """

    def __init__(self, text: str, *, soft: bool) -> None:
        self.text = text
        self.soft = soft
        self.words: list[Word] = []
        self.segments: list[Segment] = []
        self.parts: list[str] = []
        self.line_begin = 0
        self.merged = 0  # backslash breaks dropped as earlier wraps

    def flush(self) -> None:
        if self.parts:
            written = "".join(self.parts)
            self.parts = []
            self.words.append(Word(line_start_form(written), written))

    def end_segment(self, ending: str) -> None:
        """Close the words so far as a segment; raise EmptySegment when there are none."""
        self.flush()
        if not self.words:
            raise EmptySegment
        self.segments.append(Segment(tuple(self.words), ending))
        self.words = []

    def run(self) -> list[Segment]:
        """Return the segments; raise EmptySegment when a deliberate break has no text before it."""
        text = self.text
        index = 0
        while index < len(text):
            character = text[index]
            following = text[index + 1 : index + 2]
            if character == "\\":
                if following == "\n":
                    index = self.take_backslash_newline(index)
                elif following and following in PUNCTUATION:
                    self.parts.append(character + following)
                    index += 2
                else:
                    self.parts.append(character)
                    index += 1
            elif character == "`":
                index = self.take_code_span(index)
            elif character == "<":
                match = AUTOLINK.match(text, index) or INLINE_HTML.match(text, index)
                self.parts.append(match.group().replace("\n", " ") if match else character)
                index = match.end() if match else index + 1
            elif character == "]" and (match := LINK_TARGET.match(text, index)):
                self.parts.append(match.group().replace("\n", " "))
                index = match.end()
            elif character in " \t":
                self.flush()
                index += 1
            elif character == "\n":
                self.take_newline(index)
                index += 1
            else:
                self.parts.append(character)
                index += 1
        self.end_segment(NO_BREAK)
        return self.segments

    def take_backslash_newline(self, index: int) -> int:
        """Handle a backslash that ends a line; return the index of the next line's first character."""
        if self.soft:
            self.end_segment(HARD_BREAK)
        else:
            self.flush()  # an earlier wrap: the next line joins the same segment
            self.merged += 1
        self.line_begin = index + 2
        return index + 2

    def take_code_span(self, index: int) -> int:
        """Add the code span or backtick run at `index` as one word-part; return the next index."""
        opening = BACKTICKS.match(self.text, index)
        assert opening is not None  # the caller saw a backtick
        for closing in BACKTICKS.finditer(self.text, opening.end()):
            if len(closing.group()) == len(opening.group()):
                self.parts.append(self.text[index : closing.end()].replace("\n", " "))
                return closing.end()
        self.parts.append(opening.group())
        return opening.end()

    def take_newline(self, index: int) -> None:
        """Handle a line end outside any atom: a deliberate break ends the segment, a soft one does not."""
        self.flush()
        line = self.text[self.line_begin : index]
        if BREAK_TAG_END.search(line.rstrip(" \t")):
            self.end_segment(HTML_BREAK)
        elif line.endswith(SPACE_BREAK):
            self.end_segment(SPACE_BREAK)
        self.line_begin = index + 1


def may_break(line: Sequence[Word], following: Word) -> bool:
    """Whether the line may end after its last word and the next line may open with `following`.

    A word that ends in an odd number of backslashes would turn the line break into a hard break (or, with the
    marker appended, into an escaped backslash). A `<br>` tag in mid-text would read as a deliberate break on
    the next run. A delimiter run such as `*` changes its flanking when it ends a line, and a line that holds
    only a rule word or a tag would be a thematic break, a setext underline or an HTML block. A line opening
    with `#` would become a heading under markdownlint's MD018 fix.
    """
    last = line[-1].text
    trailing = len(last) - len(last.rstrip("\\"))
    return (
        trailing % 2 == 0
        and not BREAK_TAG_END.search(last)
        and not DELIMITER_RUN.match(last)
        and not (len(line) == 1 and RULE_WORD.match(line[0].opening))
        and not BLOCK_START.match(following.opening)
        and not LINT_HEADING.match(following.opening)
    )


def render_line(words: Sequence[Word]) -> str:
    return words[0].opening + "".join(" " + word.text for word in words[1:])


def fill(words: Sequence[Word], first_room: int, other_room: int) -> list[list[Word]]:
    """Pack words greedily into lines.

    A line that cannot end after its last word, or whose next line could not open with the next word, gives
    that word back to the next line; when no word is left to give, the line overflows instead. The first word
    of the first line is where it was in the source and never moves.
    """
    lines: list[list[Word]] = [[]]
    for word in words:
        current = lines[-1]
        room = first_room if len(lines) == 1 else other_room
        if not current or len(render_line([*current, word])) <= room:
            current.append(word)
            continue
        carried = [word]
        while len(current) > 1 and not may_break(current, carried[0]):
            carried.insert(0, current.pop())
        if may_break(current, carried[0]):
            lines.append(carried)
        else:
            current.extend(carried)
    return lines


def container_prefix(first_line: str, content: str) -> tuple[str, str] | None:
    """Return the prefix of the paragraph's first line and the prefix for its other lines.

    The first line keeps its own markers and indentation. Other lines replace a list marker by spaces, keep
    block-quote markers, and indent a footnote definition by four spaces.
    """
    source = first_line.rstrip(" \t")
    text = content.split("\n", 1)[0].rstrip(" \t")
    if not text or not source.endswith(text):
        return None
    first = source[: len(source) - len(text)]
    other = LIST_MARKER.sub(lambda marker: " " * len(marker.group()), FOOTNOTE_LABEL.sub(FOOTNOTE_INDENT, first))
    return first, other


def too_long(line: str, width: int, mode: LengthMode = LengthMode.DEFAULT) -> bool:
    """Return whether a line breaks the width the way markdownlint's MD013 counts it in the given mode.

    The default mode accepts a line that runs past the width with no whitespace beyond it, such as one ending in
    a long URL, because no break can shorten it. Stern mode accepts only a line with no whitespace after its
    leading markers, and strict mode accepts no line past the width. Stern mode also accepts a line holding only
    links, which this function cannot see, so such a line may be rewrapped although the linter passes it.
    """
    if len(line) <= width:
        return False
    if mode is LengthMode.STRICT:
        return True
    if mode is LengthMode.STERN:
        return not NOT_WRAPPABLE.match(line)
    return any(character.isspace() for character in line[width:])


def wrap_segment(segment: Segment, lead: str, other_prefix: str, options: Options) -> list[str] | None:
    """Wrap one segment into lines, or return None when the prefixes leave no room for text.

    Every line but the segment's last ends with the hard-break marker unless `--soft` is set. The room reserved
    on each line is the longest marker the segment can carry, so the last line fits with its ending too.
    """
    inner = NO_BREAK if options.soft else HARD_BREAK
    closing = EMITTED_ENDING[segment.ending]
    reserve = max(len(inner), len(closing))
    first_room = options.width - len(lead) - reserve
    other_room = options.width - len(other_prefix) - reserve
    if min(first_room, other_room) < 1:
        return None
    packed = fill(segment.words, first_room, other_room)
    return [
        (lead if index == 0 else other_prefix) + render_line(words) + (inner if index < len(packed) - 1 else closing)
        for index, words in enumerate(packed)
    ]


def rewrap_paragraph(lines: Sequence[str], paragraph: Paragraph, options: Options) -> Rewrite | str:
    """Return the rewrapped lines for a paragraph, or the reason it must stay as it is."""
    content_lines = paragraph.content.split("\n")
    if len(content_lines) != paragraph.end - paragraph.start:
        return "could not match the paragraph to its source lines"
    if any(line.lstrip(" \t").startswith("$$") for line in content_lines):
        return "possible display math"
    prefixes = container_prefix(lines[paragraph.start], paragraph.content)
    if prefixes is None:
        return "could not find the container prefix"
    first_prefix, other_prefix = prefixes
    if "\t" in first_prefix:
        return "tab in the container prefix"
    scanner = Scanner("\n".join(line.lstrip(" \t") for line in content_lines), soft=options.soft)
    try:
        segments = scanner.run()
    except EmptySegment:
        return "line break with no text before it"

    wrapped: list[str] = []
    for position, segment in enumerate(segments):
        lead = first_prefix if position == 0 else other_prefix
        segment_lines = wrap_segment(segment, lead, other_prefix, options)
        if segment_lines is None:
            return "container prefix leaves no room for text"
        wrapped.extend(segment_lines)
    over_limit = any(too_long(line, options.width, options.length_mode) for line in wrapped)
    return Rewrite(paragraph, tuple(wrapped), over_limit, scanner.merged)


def looks_like_front_matter(body_lines: Iterable[str]) -> bool:
    """Whether the first non-blank line is a key, a comment or a table header, or the body is empty.

    Prose between two thematic breaks has none of these, so it is not front matter.
    """
    first = next((line for line in body_lines if line.strip()), "")
    return not first or bool(FRONT_MATTER_START.match(first))


def front_matter_lines(lines: Sequence[str]) -> int:
    """Return how many leading lines are TOML front matter fenced by `+++`, 0 when there is none.

    The front-matter plugin only knows `---`, so `+++` front matter is found here and blanked for the parser;
    left in place it would parse as a paragraph.
    """
    if not lines or lines[0].rstrip() != "+++":
        return 0
    for index in range(1, len(lines)):
        if lines[index].rstrip() == "+++":
            return index + 1 if looks_like_front_matter(lines[1:index]) else 0
    return 0


def build_markdown_parser(*, front_matter: bool) -> MarkdownIt:
    markdown = MarkdownIt("commonmark").enable(["table", "strikethrough"]).use(footnote_plugin)
    return markdown.use(front_matter_plugin) if front_matter else markdown


def paragraphs(tokens: Sequence[Token]) -> list[Paragraph]:
    """Collect the paragraphs outside a `mdformat off` region, using the parser's line maps."""
    found: list[Paragraph] = []
    enabled = True
    for index, token in enumerate(tokens):
        if token.type == "html_block":
            switch = MDFORMAT_SWITCH.fullmatch(token.content.strip())
            if switch:
                enabled = switch.group(1) == "on"
        elif token.type == "paragraph_open" and enabled and token.map and tokens[index + 1].type == "inline":
            found.append(Paragraph(token.map[0], token.map[1], tokens[index + 1].content))
    return found


class Rendering(NamedTuple):
    """A document's HTML with every break and whitespace run reduced to one space, and its hard-break count."""

    text: str
    hard_breaks: int


def render(markdown: MarkdownIt, text: str) -> Rendering:
    html = markdown.render(text)
    return Rendering(WHITESPACE.sub(" ", BREAK_HTML.sub(" ", html)), len(BREAK_HTML.findall(html)))


def same_rendering(before: Rendering, after: Rendering, merged: int) -> bool:
    """Whether the rendering is the same text and keeps every hard break that was not turned into a wrap."""
    return before.text == after.text and after.hard_breaks >= before.hard_breaks - merged


@dataclass(frozen=True)
class Document:
    """A file's lines with their original terminators, and how to give the parser the same lines."""

    lines: tuple[str, ...]
    endings: tuple[str, ...]
    # Leading `+++` front-matter lines that the parser sees as blank lines, so line numbers stay the same.
    blanked: int

    def parser_text(self, lines: Sequence[str]) -> str:
        return "\n".join([""] * self.blanked + list(lines[self.blanked :]))

    def apply(self, rewrites: Sequence[Rewrite]) -> tuple[list[str], list[str]]:
        """Return the lines and terminators with the rewrites in place; the first terminator fills new lines."""
        newline = "\r\n" if "\r\n" in self.endings else "\n"
        lines: list[str] = []
        endings: list[str] = []
        cursor = 0
        for rewrite in sorted(rewrites, key=lambda item: item.paragraph.start):
            start, end = rewrite.paragraph.start, rewrite.paragraph.end
            lines.extend(self.lines[cursor:start])
            endings.extend(self.endings[cursor:start])
            lines.extend(rewrite.lines)
            inner = self.endings[start] or newline
            endings.extend([inner] * (len(rewrite.lines) - 1) + [self.endings[end - 1]])
            cursor = end
        lines.extend(self.lines[cursor:])
        endings.extend(self.endings[cursor:])
        return lines, endings


def parse_document(document: Document) -> tuple[MarkdownIt, list[Token]]:
    """Parse the document; return the parser that did it and its tokens.

    A `---` block at the top that does not look like front matter is parsed again without the front-matter
    plugin, so the thematic breaks and the prose between them stay ordinary content.
    """
    text = document.parser_text(document.lines)
    markdown = build_markdown_parser(front_matter=True)
    tokens = markdown.parse(text)
    lookalike = (
        bool(tokens) and tokens[0].type == "front_matter" and not looks_like_front_matter(tokens[0].content.split("\n"))
    )
    if lookalike:
        markdown = build_markdown_parser(front_matter=False)
        tokens = markdown.parse(text)
    return markdown, tokens


def plan_paragraphs(
    document: Document, tokens: Sequence[Token], options: Options
) -> tuple[list[Rewrite], list[Finding]]:
    """Rewrap every paragraph that has a too-long line.

    Return the rewrites that change a paragraph, and the findings for paragraphs that cannot be rewrapped or
    that stay over the limit with their text unchanged.
    """
    lines = document.lines
    candidates: list[Rewrite] = []
    findings: list[Finding] = []
    for paragraph in paragraphs(tokens):
        numbers = range(paragraph.start, paragraph.end)
        if not any(too_long(lines[number], options.width, options.length_mode) for number in numbers):
            continue
        result = rewrap_paragraph(lines, paragraph, options)
        if isinstance(result, str):
            findings.append(Finding(paragraph.start + 1, Kind.SKIPPED, result))
        elif result.lines != tuple(lines[paragraph.start : paragraph.end]):
            candidates.append(result)
        elif result.over_limit:
            findings.append(over_limit_finding(paragraph.start + 1, options.width))
    return candidates, findings


def verified(
    document: Document, markdown: MarkdownIt, rewrites: Sequence[Rewrite]
) -> tuple[list[Rewrite], list[Rewrite]]:
    """Split rewrites into those that keep the rendering and those that change it."""
    before = render(markdown, document.parser_text(document.lines))

    def keeps(candidates: Sequence[Rewrite]) -> bool:
        lines, _ = document.apply(candidates)
        after = render(markdown, document.parser_text(lines))
        return same_rendering(before, after, sum(rewrite.merged_breaks for rewrite in candidates))

    if not rewrites or keeps(rewrites):
        return list(rewrites), []
    good = [rewrite for rewrite in rewrites if keeps([rewrite])]
    if good and not keeps(good):
        good = []  # each is safe alone but not together, so none is safe to write
    return good, [rewrite for rewrite in rewrites if rewrite not in good]


def process_text(text: str, options: Options) -> Outcome:
    """Plan the rewraps for one document, drop those that would change the rendering, and apply the rest."""
    if "\r" in LINE_ENDING.sub("", text):
        raise DocumentError("lone carriage return line endings are not supported")
    parts = LINE_ENDING.split(text)
    lines = parts[0::2]
    document = Document(tuple(lines), tuple([*parts[1::2], ""]), front_matter_lines(lines))
    markdown, tokens = parse_document(document)
    candidates, findings = plan_paragraphs(document, tokens, options)

    accepted, rejected = verified(document, markdown, candidates)
    for rewrite in rejected:
        findings.append(Finding(rewrite.paragraph.start + 1, Kind.SKIPPED, "rewrap would change the rendering"))
    for rewrite in accepted:
        line = rewrite.paragraph.start + 1
        findings.append(Finding(line, Kind.REWRAP, f"line exceeds {options.width} characters"))
        if rewrite.over_limit:
            findings.append(over_limit_finding(line, options.width))
    findings.sort(key=lambda finding: finding.line)
    if not accepted:
        return Outcome(None, tuple(findings))
    new_lines, new_endings = document.apply(accepted)
    new_text = "".join(line + ending for line, ending in zip(new_lines, new_endings, strict=True))
    return Outcome(new_text, tuple(findings))


def process_file(path: Path, options: Options) -> FileResult:
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise DocumentError(f"cannot read {path}: {error}") from error
    bom = "\ufeff" if text.startswith("\ufeff") else ""
    try:
        outcome = process_text(text.removeprefix(bom), options)
    except (DocumentError, RecursionError, ValueError) as error:
        raise DocumentError(f"cannot process {path}: {error}") from error
    output = None if outcome.text is None else (bom + outcome.text).encode("utf-8")
    return FileResult(path, output, outcome)


def write_files(results: Sequence[FileResult]) -> None:
    """Write every changed file through a temporary file and a rename, or change nothing."""
    staged: list[tuple[Path, Path]] = []
    try:
        for result in results:
            if result.output is None:
                continue
            target = result.path.resolve()
            descriptor, name = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp")
            temporary = Path(name)
            staged.append((temporary, target))
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(result.output)
            temporary.chmod(stat.S_IMODE(target.stat().st_mode))
        for temporary, target in staged:
            temporary.replace(target)
    except OSError:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)
        raise


class ExitTwoArgumentParser(argparse.ArgumentParser):
    """An argument parser whose usage errors read `mdwrap: error: ...` and exit with status 2."""

    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        self.exit(EXIT_ERROR, f"{PROGRAM}: error: {message}\n")


def width_argument(value: str) -> int:
    try:
        width = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"width must be a whole number, not {value!r}") from None
    if width < MIN_WIDTH:
        raise argparse.ArgumentTypeError(f"width must be at least {MIN_WIDTH}")
    return width


def build_argument_parser() -> argparse.ArgumentParser:
    parser = ExitTwoArgumentParser(
        prog="mdwrap.py",
        description="Rewrap Markdown paragraphs that have a line over a width limit. Reports by default.",
        epilog=(
            "example:\n"
            "  mdwrap.py docs/guide.md                    list paragraphs with a line over 120 characters\n"
            "  mdwrap.py --write --width 100 docs/*.md    rewrap them to 100 characters with backslash breaks\n"
            "\n"
            "Output is `path:line: rewrap|skipped|over limit: reason`, one line per paragraph."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE", help="Markdown files to check")
    parser.add_argument("--write", action="store_true", help="rewrap the files in place instead of reporting")
    parser.add_argument(
        "--soft",
        action="store_true",
        help="wrap with plain line breaks; by default every wrapped line but the last ends with a backslash",
    )
    parser.add_argument(
        "--width",
        type=width_argument,
        default=DEFAULT_WIDTH,
        help=f"maximum line length (default {DEFAULT_WIDTH}, minimum {MIN_WIDTH})",
    )
    parser.add_argument(
        "--line-length-mode",
        choices=[mode.value for mode in LengthMode],
        default=LengthMode.DEFAULT.value,
        help=(
            "count too-long lines as markdownlint's MD013 does: default allows a last word past the width, "
            "stern allows only a line with no space to break at, strict allows nothing (default: default)"
        ),
    )
    return parser


def summary_line(file_count: int, totals: Counter[Kind], *, write: bool) -> str:
    """Return the one-line summary for stderr."""
    action = "rewrapped" if write else "to rewrap"
    summary = f"{PROGRAM}: {file_count} file(s), {totals[Kind.REWRAP]} paragraph(s) {action}"
    summary += f", {totals[Kind.SKIPPED]} skipped"
    if totals[Kind.OVER_LIMIT]:
        summary += f", {totals[Kind.OVER_LIMIT]} over limit"
    return summary


def exit_status(totals: Counter[Kind], *, write: bool) -> int:
    """Return 1 when check mode found work or anything was skipped or left over the limit, else 0."""
    if totals[Kind.SKIPPED] or totals[Kind.OVER_LIMIT] or (totals[Kind.REWRAP] and not write):
        return EXIT_FINDINGS
    return EXIT_CLEAN


def main(arguments: Sequence[str] | None = None) -> int:
    parsed = build_argument_parser().parse_args(arguments)
    options = Options(parsed.width, parsed.soft, LengthMode(parsed.line_length_mode))

    results: list[FileResult] = []
    failed = False
    for path in parsed.files:
        try:
            results.append(process_file(path, options))
        except DocumentError as error:
            print(f"{PROGRAM}: error: {error}", file=sys.stderr)
            failed = True
    for result in results:
        for finding in result.outcome.findings:
            if parsed.write and finding.kind is Kind.REWRAP:
                continue
            print(f"{result.path}:{finding.line}: {finding.kind}: {finding.message}")
    if failed:
        return EXIT_ERROR

    if parsed.write:
        try:
            write_files(results)
        except OSError as error:
            print(f"{PROGRAM}: error: cannot write: {error}", file=sys.stderr)
            return EXIT_ERROR
    totals = sum((result.outcome.counts for result in results), Counter[Kind]())
    print(summary_line(len(results), totals, write=parsed.write), file=sys.stderr)
    return exit_status(totals, write=parsed.write)


if __name__ == "__main__":
    sys.exit(main())
