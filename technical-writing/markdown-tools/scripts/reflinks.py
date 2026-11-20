#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=4.3,<5", "mdit-py-plugins>=0.7,<1"]
# ///
"""Prove that converting inline links to reference-style links lost nothing.

Give the script pairs of files, the version before the conversion and the version after. For each pair it
extracts every link and image from both versions with a CommonMark parser, resolving reference-style links to
their definitions, and compares the two as ordered sequences. A link is its kind (link or image), its
destination including any fragment, its title, and its visible text. The text compares with whitespace and line
breaks collapsed but formatting kept, so `**bold**` and `bold` differ, as do `*x*` and `x`, and `code` spans
keep their backticks.

It reports, one finding per line as `path:line: message`:

- a link in the old file that is missing or changed in the new one, at its old line;
- a link in the new file that the old one lacked, at its new line;
- a reference definition in the new file that no link or image uses;
- a `[label]` in the new file's text that matches no definition, which the parser leaves as plain text.

A link's line is exact when the link sits in a paragraph, heading or list item, where the script counts the
line breaks before it. It can be off by the lines of a multi-line destination or title. An undefined reference
inside a link's own text is not reported; neither are task-list markers (`[x]`), alert markers (`[!NOTE]`) and
footnote markers (`[^1]`).

The script never runs git. Produce the old version yourself, for example with
`git show HEAD:docs/guide.md > /tmp/old.md`.

Exit status: 0 when nothing differs, 1 when any finding is reported, 2 for a usage error, an unreadable file or a
missing dependency.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import Literal, NoReturn

try:
    from markdown_it import MarkdownIt
    from markdown_it.common.utils import normalizeReference
    from markdown_it.token import Token
    from mdit_py_plugins.front_matter import front_matter_plugin
except ImportError as error:  # a runner that ignored the inline script metadata above
    print(f"reflinks.py: error: cannot import a required package: {error}", file=sys.stderr)
    print(
        "hint: run it as `uv run scripts/reflinks.py`, which installs the dependencies",
        file=sys.stderr,
    )
    sys.exit(2)

SCRIPT = "reflinks.py"
EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2

# `[text][label]` or `[label]` as plain text. The second group is the label when it is present and not empty.
BRACKETS = re.compile(r"\[(?P<first>[^\[\]]+)\](?:\[(?P<second>[^\[\]]*)\])?")


# The opening of a reference definition, to recover its label as written; the parser keeps only a normalised one.
DEFINITION = re.compile(r"^[\s>*+\d.-]*\[([^\]]*)\]:")


class Category(StrEnum):
    """The kind of a finding; the value is the word the summary line uses for it."""

    LOST = "lost"
    ADDED = "added"
    UNUSED = "unused"
    UNDEFINED = "undefined"


class CheckError(Exception):
    """A failure that ends the run with exit status 2."""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.hint = hint


@dataclass(frozen=True)
class Link:
    """What a reader gets from a link or image, without its position."""

    kind: Literal["link", "image"]
    destination: str
    title: str
    text: str

    def describe(self) -> str:
        title = f' "{self.title}"' if self.title else ""
        prefix = "!" if self.kind == "image" else ""
        return f"{prefix}[{self.text}]({self.destination}{title})"


@dataclass(frozen=True)
class Located:
    """A link with the 1-based line it was found on."""

    link: Link
    line: int


@dataclass(frozen=True)
class Finding:
    """One reported problem, printed as `path:line: message`."""

    path: Path
    line: int
    category: Category
    message: str


@dataclass(frozen=True)
class Definition:
    """A reference definition, with its label as written."""

    label: str
    line: int


@dataclass
class Parsed:
    """Everything the check needs from one Markdown file; the scan fills it in as it goes."""

    links: list[Located]
    definitions: dict[str, Definition]  # by normalised label
    used: set[str]  # normalised labels that a link or image resolved through
    undefined: list[tuple[int, str]]  # line and label text, as written


class ArgumentParser(argparse.ArgumentParser):
    """An argparse parser whose usage errors follow this script's error format."""

    def error(self, message: str) -> NoReturn:
        print(f"{SCRIPT}: error: invalid arguments: {message}", file=sys.stderr)
        print(f"hint: run `{SCRIPT} --help` for the usage", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def make_parser() -> MarkdownIt:
    """Return a CommonMark parser that skips front matter and records which label each link used."""
    parser = MarkdownIt("commonmark", {"store_labels": True}).use(front_matter_plugin)
    # Keep an escaped bracket (`\[x\]`) as its own token, so scanning text tokens for `[label]` does not
    # mistake it for a reference the parser failed to resolve.
    parser.core.ruler.disable("text_join")
    return parser


def collapse(text: str) -> str:
    return " ".join(text.split())


def render(token: Token) -> str:
    """Return a link's inner token as text that keeps its formatting."""
    match token.type:
        case "em_open" | "em_close":
            return "*"
        case "strong_open" | "strong_close":
            return "**"
        case "code_inline":
            return f"{token.markup}{token.content}{token.markup}"
        case "softbreak" | "hardbreak":
            return " "
        case "image":
            return f"![{collapse(token.content)}]"
        case "text" | "text_special" | "html_inline":
            return token.content
        case _:
            return ""


def attribute(token: Token, name: str) -> str:
    value = token.attrs.get(name, "")
    return str(value)


def scan_inline(children: Sequence[Token], first_line: int, parsed: Parsed) -> None:
    """Add the links, used labels and undefined references of one inline token to `parsed`."""
    line = first_line
    open_index: int | None = None
    open_parts: list[str] = []
    for position, child in enumerate(children):
        if child.type in ("softbreak", "hardbreak"):
            line += 1
        if child.type == "link_open":
            link = Link("link", attribute(child, "href"), attribute(child, "title"), "")
            open_index = len(parsed.links)
            open_parts = []
            parsed.links.append(Located(link, line))
            note_label(child, parsed)
        elif child.type == "link_close" and open_index is not None:
            placeholder = parsed.links[open_index]
            link = replace(placeholder.link, text=collapse("".join(open_parts)))
            parsed.links[open_index] = replace(placeholder, link=link)
            open_index = None
        elif child.type == "image":
            link = Link("image", attribute(child, "src"), attribute(child, "title"), collapse(child.content))
            parsed.links.append(Located(link, line))
            note_label(child, parsed)
            if open_index is not None:
                open_parts.append(render(child))
        elif open_index is not None:
            open_parts.append(render(child))
        elif child.type == "text":
            # Reached only outside a link, so link text is never scanned for undefined references.
            find_undefined(child.content, line, position == 0, parsed)


def note_label(token: Token, parsed: Parsed) -> None:
    label = token.meta.get("label")
    if label:
        parsed.used.add(str(label))


def find_undefined(text: str, line: int, is_first_child: bool, parsed: Parsed) -> None:
    """Collect `[label]` patterns in a text token as candidates for undefined references.

    A candidate may still match a definition that appears later in the file; `parse_markdown` drops those.
    """
    for match in BRACKETS.finditer(text):
        label = match.group("second") or match.group("first")
        normalised = normalizeReference(label)
        # A task-list or alert marker counts only at the very start of the inline content.
        opens_inline = match.start() == 0 and is_first_child
        if not normalised or label.startswith("^"):
            continue  # an empty label, or a footnote marker
        if opens_inline and (label in ("x", "X") or label.startswith("!")):
            continue  # a task-list or alert marker
        parsed.undefined.append((line, label))


def read_definitions(text: str, references: object) -> dict[str, Definition]:
    """Return the parser's reference definitions with their labels as written and 1-based lines.

    The parser splits lines at `\\n` after turning `\\r\\n` and `\\r` into `\\n`, so this does the same;
    `str.splitlines` would also split at characters such as U+0085 and misalign the line numbers.
    """
    lines = re.sub(r"\r\n?", "\n", text).split("\n")
    definitions: dict[str, Definition] = {}
    if not isinstance(references, dict):
        return definitions
    for label, reference in references.items():
        line = int(reference["map"][0])
        written = DEFINITION.match(lines[line]) if line < len(lines) else None
        definitions[label] = Definition(written.group(1) if written else label, line + 1)
    return definitions


def parse_markdown(text: str) -> Parsed:
    parser = make_parser()
    env: dict[str, object] = {}
    tokens = parser.parse(text, env)
    parsed = Parsed(links=[], definitions={}, used=set(), undefined=[])
    for token in tokens:
        if token.type == "inline" and token.children and token.map:
            scan_inline(token.children, token.map[0] + 1, parsed)
    parsed.definitions = read_definitions(text, env.get("references"))
    parsed.undefined = [
        (line, label) for line, label in parsed.undefined if normalizeReference(label) not in parsed.definitions
    ]
    return parsed


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        cause = error.strerror if isinstance(error, OSError) and error.strerror else str(error)
        raise CheckError(f"cannot read {path}: {cause}") from error


def check_pair(old_path: Path, new_path: Path) -> list[Finding]:
    old = parse_markdown(read(old_path))
    new = parse_markdown(read(new_path))
    findings: list[Finding] = []
    matcher = difflib.SequenceMatcher(
        a=[located.link for located in old.links],
        b=[located.link for located in new.links],
        autojunk=False,
    )
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag in ("delete", "replace"):
            for located in old.links[old_start:old_end]:
                findings.append(
                    Finding(
                        old_path,
                        located.line,
                        Category.LOST,
                        f"link lost: {located.link.describe()}",
                    )
                )
        if tag in ("insert", "replace"):
            for located in new.links[new_start:new_end]:
                findings.append(
                    Finding(
                        new_path,
                        located.line,
                        Category.ADDED,
                        f"link added: {located.link.describe()}",
                    )
                )
    for label, definition in new.definitions.items():
        if label not in new.used:
            findings.append(
                Finding(
                    new_path,
                    definition.line,
                    Category.UNUSED,
                    f"unused definition: [{definition.label}]",
                )
            )
    for line, label in new.undefined:
        findings.append(Finding(new_path, line, Category.UNDEFINED, f"undefined reference: [{label}]"))
    return findings


def build_argument_parser() -> argparse.ArgumentParser:
    parser = ArgumentParser(
        prog=SCRIPT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Prove that an inline-to-reference link conversion lost no link or image. "
        "Takes OLD NEW pairs: the version before and the version after.",
        epilog="example:\n"
        "  git show HEAD:docs/guide.md > /tmp/old.md\n"
        "  uv run scripts/reflinks.py /tmp/old.md docs/guide.md\n"
        "\n"
        "Prints one finding per line as path:line: message. Exits 0 when nothing differs, "
        "1 on findings, 2 on a usage or file error.",
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="OLD NEW", help="pairs of old and new Markdown files")
    return parser


def run(arguments: Sequence[str] | None) -> int:
    options = build_argument_parser().parse_args(arguments)
    files: list[Path] = options.files
    if len(files) % 2:
        raise CheckError(
            f"invalid arguments: expected OLD NEW pairs, got {len(files)} file(s)",
            "pass each old file followed by its new file",
        )
    findings: list[Finding] = []
    pairs = list(zip(files[0::2], files[1::2], strict=True))
    for old_path, new_path in pairs:
        findings.extend(check_pair(old_path, new_path))
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.message}")
    counts = Counter(finding.category for finding in findings)
    print(
        f"reflinks: {len(pairs)} file pair(s), {counts[Category.LOST]} link(s) lost, {counts[Category.ADDED]} link(s) added, "
        f"{counts[Category.UNUSED]} unused definition(s), {counts[Category.UNDEFINED]} undefined reference(s)",
        file=sys.stderr,
    )
    return EXIT_FINDINGS if findings else EXIT_CLEAN


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
