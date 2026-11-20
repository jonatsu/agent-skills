"""Behavioral tests for the markdown-tools skill's Markdown rewrap script."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from skill_locator import skill_directory

SCRIPT = skill_directory("markdown-tools") / "scripts" / "mdwrap.py"

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2

LONG = (
    "This sentence is long enough that the wrapper has to break it somewhere, and it keeps going "
    "for a while so that it needs more than one line at the default width of the script."
)
# A line that a wrap would turn into a list, heading, quote, rule or fence if it began with one of these.
BLOCK_OPENER = re.compile(r"^\s*(?:[-+*]|\d{1,9}[.)]|#{1,6}|>|=+|\*{3,}|_{3,}|\||```|~~~)(?:\s|$)")

# One synthetic input per structure or hazard the script must handle, plus controls that must pass unchanged.
# The widths that exercise them are small so each input stays short.
REPRODUCTIONS = {
    "trailing-space-break": (
        "# Address\n\nExample Corp  \n1 Example Street  \nSample City\n\n"
        "First line ends with an HTML break<br>\nsecond line follows.\n"
    ),
    "table-no-leading-pipe": "Name | Value\n--- | ---\nhost | example.com\nport | 8080\n",
    "table-row-no-pipe-long": (
        "| Name | Value |\n| --- | --- |\n"
        "host | the example host is example.com and this cell has a long description that runs well beyond the "
        "width limit of sixty\n"
    ),
    "unbalanced-backtick": (
        "The example parser treats a lone ` character as literal text, so this sentence keeps going for many "
        "more words after it and should wrap normally at the width.\n"
    ),
    "double-backtick-span": (
        "The example setting is ``a`b`` and after it this sentence keeps going for many more words that should "
        "wrap normally at the width limit.\n"
    ),
    "double-backtick-in-list": (
        "- `License`: the identifier in backticks, such as `` `GPL-2.0-or-later` `` or "
        "`` `MIT AND CC-BY-SA-4.0` ``. Another sentence follows it.\n"
    ),
    "unbalanced-bracket": (
        "The example range [0, 10) is half open, so this sentence keeps going for many more words after the "
        "bracket and should wrap normally at the width.\n"
    ),
    "fence-nested-list": (
        "- Step one\n  - Sub step\n    ```sh\n    example-command --option value --another-option value "
        "--third-option value --fourth-option value\n    ```\n"
    ),
    "fence-in-quote": (
        "> Run this:\n>\n> ```sh\n> example-command --option value --another-option value --third-option value "
        "--fourth-option value\n> ```\n"
    ),
    "fence-four-space-list": (
        "1. Run the example command:\n    ```sh\n    example-command --option value --another-option value "
        "--third-option value --fourth-option value\n    ```\n"
    ),
    "html-block": (
        "<!-- example-directive: this comment spans lines\nand this second comment line is long enough to pass "
        "the sixty column limit used here -->\n\n<div>\n<p>An example paragraph inside a div that is long "
        "enough to pass the sixty column limit used here.</p>\n</div>\n"
    ),
    "html-block-text": (
        "<details>\n<summary>Example summary</summary>\nAn example line of text inside a details block that is "
        "long enough to pass the sixty column limit used here.\n</details>\n"
    ),
    "inline-html-start": (
        "<kbd>Ctrl</kbd> and <kbd>C</kbd> copy the selection in the example editor, and this prose line is long "
        "enough to pass the limit.\n\nAn example paragraph where a wrapped line\n<name> starts with a placeholder "
        "and the line goes on for quite a while past the limit of sixty.\n"
    ),
    "crlf": (
        "# Title\r\n\r\nAn example paragraph that is long enough to pass the sixty column limit used for this "
        "test run.\r\n\r\nShort line.\r\n"
    ),
    "bom-front-matter": (
        "\ufeff---\ntitle: Example\ndescription: an example front matter line that is long enough to pass the "
        "sixty column limit used\n---\n\nBody.\n"
    ),
    "long-link": (
        "See [an example link whose visible text is long enough that it cannot fit within the sixty column "
        "limit used here](https://example.com/a) for details.\n\nAn example URL "
        "https://example.com/a/very/long/path/that/never/ends/and/cannot/be/broken/at/all/so/it/overflows/the/"
        "limit/ok here.\n"
    ),
    "soft-wrapped": (
        "This example paragraph is wrapped softly, as many repositories\ndo, with no trailing backslash on any "
        "line, and every line is\nwell within the width limit.\n\n- A soft wrapped list item that\n  continues "
        "on a second line.\n"
    ),
    "stranded-last-line": (
        "The example service reads its configuration from a file, validates every key against the schema, and "
        "then starts listening.\n"
    ),
    "footnote": (
        "An example claim.[^1]\n\n[^1]: An example footnote text that is long enough to pass the sixty column "
        "limit used for this test run, and then\n    continues on an indented line that is also long enough to "
        "pass the sixty column limit used here.\n"
    ),
    "escaped-backslash": (
        "The example path on Windows ends with C:\\\\ and this first line is long enough to pass the limit of "
        "sixty\nand the next line continues the same paragraph and ends the paragraph with a trailing "
        "backslash\\\\\n"
    ),
    "setext": (
        "An example setext heading title that is long enough to pass the sixty column limit used here\n"
        "===========================================================================================\n\nBody.\n"
    ),
    "nested-list": (
        "- Parent item\n\n    - Nested example item indented four spaces that is long enough to pass the sixty "
        "column limit used here.\n\n1. Ordered parent\n\n    A continuation paragraph indented four spaces that is "
        "long enough to pass the sixty column limit used here.\n"
    ),
    "quote-in-list": (
        "- > An example quote on the bullet line that is long enough to pass the sixty column limit used for this "
        "test run.\n- Item with a quote below\n  > An example quote below the item that is long enough to pass "
        "the sixty column limit used for this test run.\n"
    ),
    "number-line-start": (
        "The example release shipped in the year\n2026. It was a good one and this sentence keeps going to pass "
        "the limit of sixty.\n"
    ),
    "math-block": "$$\nx = a very long example expression that is long enough to pass the sixty column limit used here\n$$\n",
    "thematic-token": "The example text ends in a run of markers that renders as a rule ***\n",
    "underscore-rule": "The example text ends in a run of markers that renders as a rule ___\n",
    "ignore-region": (
        "<!-- mdformat off -->\nAn example paragraph that sits inside a formatter-off region and is long enough "
        "to pass the sixty column limit used here.\n<!-- mdformat on -->\n"
    ),
    "front-matter-lookalike": (
        "---\n\nAn example intro paragraph that is long enough to pass the sixty column limit used for this test "
        "run.\n\n---\n\nAnother example paragraph that is long enough to pass the sixty column limit used for this "
        "test run.\n"
    ),
    "list-continuation-indent": (
        "1. First step has a long example sentence that is long enough to pass the sixty column limit used here\n"
        "   and a second line.\n10. Tenth step has a long example sentence that is long enough to pass the sixty "
        "column limit used here\n    and a second line.\n"
    ),
    "task-list": (
        "- [ ] An example task whose description is long enough to pass the sixty column limit used for this "
        "test run.\n- [x] Done example task with a [link](https://example.com) and `code` that is long enough to "
        "pass the limit.\n"
    ),
    "empty-list-items": "## Steps to reproduce\n\n1.\n2.\n3.\n",
    "label-lines": "Status: <proposed or accepted>\nBasis: the accepted requirements\nOpen items: none\n",
    "pipe-line-start": (
        "The example shell prints alpha beta gamma | grep delta | wc and then more words follow in this long "
        "sentence ok.\n"
    ),
    "backslash-at-line-end": (
        "The example folder is named C:\\Example\\ in the prose and the sentence keeps going for many more words "
        "after it ok.\n"
    ),
    "code-span-edge-space": (
        "An example sentence with a code span that was broken by hand: `\nexample-value` and then more words "
        "follow so the line is long enough here.\n"
    ),
    "code-span": (
        "The example project uses `example.com` as its host and a `very long code span with several words inside "
        "it` for configuration of the thing, and it keeps going on past the width.\n"
    ),
    "regressions": (
        "---\ntitle: Example\ndescription: an example front matter line that is long enough to pass the sixty "
        "column limit used here\n---\n\n# Heading\n\n***\n\nAn example setext title\n"
        "-----------------------\n\n"
        "<https://example.com/a/very/long/autolink/path/that/is/long/enough/to/pass/the/sixty/limit>\n\n"
        "An example line with some words and then an autolink that starts the next line\n"
        "<https://example.com/a/b> and then more words follow until the end of the para.\n\n* * *\n___\n+++\n"
    ),
}


def _load_script() -> ModuleType:
    """Import the script in-process, for the matrix tests that would be slow as subprocesses."""
    spec = importlib.util.spec_from_file_location("mdwrap_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up here
    spec.loader.exec_module(module)
    return module


MDWRAP = _load_script()


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _main(*arguments: str) -> tuple[int, str, str]:
    """Run the script in-process; return its exit status, stdout and stderr."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            status = MDWRAP.main(list(arguments))
        except SystemExit as stop:
            status = stop.code
    return status, out.getvalue(), err.getvalue()


def _rendering(text: str) -> str:
    """Render with every break and whitespace run reduced to one space.

    The parser configuration repeats the script's on purpose: the tests judge the script against their own
    rendering, so a mistake in the script's setup cannot hide in both.
    """
    parser = (
        MarkdownIt("commonmark")
        .enable(["table", "strikethrough"])
        .use(front_matter_plugin)
        .use(footnote_plugin)
    )
    return re.sub(
        r"\s+",
        " ",
        parser.render(text.removeprefix("\ufeff").replace("\r\n", "\n")).replace("<br />", " "),
    )


class ScriptTestCase(unittest.TestCase):
    """A temporary directory and helpers to write a document and run the script over it."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def _file(self, text: str, name: str = "doc.md") -> Path:
        path = self.root / name
        path.write_bytes(text.encode("utf-8"))
        return path

    def _text(self, path: Path) -> str:
        return path.read_bytes().decode("utf-8")

    def _write(self, text: str, *options: str) -> str:
        """Rewrap in place and return the new text; the run must succeed."""
        path = self._file(text)
        status, _, err = _main("--write", *options, str(path))
        self.assertEqual(status, EXIT_CLEAN, err)
        return self._text(path)

    def _write_any(self, text: str, *options: str) -> tuple[int, str, str]:
        """Rewrap in place; return the exit status, the new text and stdout, whatever the status."""
        path = self._file(text)
        status, out, _ = _main("--write", *options, str(path))
        return status, self._text(path), out.replace(str(path), "doc.md")

    def _check(self, text: str, *options: str) -> tuple[int, str]:
        """Run check mode; return the status and stdout with the path shortened to `doc.md`."""
        path = self._file(text)
        status, out, _ = _main(*options, str(path))
        self.assertEqual(self._text(path), text, "check mode must not change the file")
        return status, out.replace(str(path), "doc.md")


class MdwrapTests(ScriptTestCase):
    """Cover rewrapping, the structures it must leave alone, and the interface."""

    def test_check_mode_reports_and_changes_nothing(self) -> None:
        path = self._file(f"# Title\n\n{LONG}\n")
        result = _run(str(path))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(result.stdout, f"{path}:3: rewrap: line exceeds 120 characters\n")
        self.assertEqual(result.stderr, "mdwrap: 1 file(s), 1 paragraph(s) to rewrap, 0 skipped\n")
        self.assertEqual(path.read_text(encoding="utf-8"), f"# Title\n\n{LONG}\n")

    def test_write_uses_hard_breaks_within_the_width_and_is_idempotent(self) -> None:
        path = self._file(f"{LONG}\n")
        result = _run("--write", str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "mdwrap: 1 file(s), 1 paragraph(s) rewrapped, 0 skipped\n")
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertTrue(all(len(line) <= 120 for line in lines))
        self.assertTrue(all(line.endswith("\\") for line in lines[:-1]))
        self.assertFalse(lines[-1].endswith("\\"))
        self.assertEqual(_run(str(path)).returncode, EXIT_CLEAN)

    def test_soft_wrapped_lines_that_fit_are_not_touched(self) -> None:
        # Soft-wrapped lines that all fit are the author's layout, so neither mode joins them or adds backslashes.
        original = "one two\nthree four\nfive six\n"
        self.assertEqual(self._write(original, "--width", "20"), original)
        self.assertEqual(self._check(original, "--width", "20"), (EXIT_CLEAN, ""))

    def test_a_paragraph_with_a_long_line_is_rejoined_and_rewrapped(self) -> None:
        text = self._write(
            "one two\nthree four five six seven eight nine ten\nfive six\n", "--width", "20"
        )
        self.assertEqual(
            text, "one two three four\\\nfive six seven\\\neight nine ten five\\\nsix\n"
        )

    def test_a_conformant_block_is_untouched(self) -> None:
        original = "short line one\\\nshort line two\n"
        self.assertEqual(self._write(original), original)

    def test_indented_code_is_never_rewrapped(self) -> None:
        code = "    " + "code " * 30 + "\n    second line\n"
        original = f"Intro.\n\n{code}\nAfter.\n"
        self.assertEqual(self._write(original), original)

    def test_fences_front_matter_tables_and_reference_definitions_are_left_alone(self) -> None:
        long_words = "word " * 40
        original = (
            f"---\ntitle: {long_words}\n---\n\n"
            f"```text\n{long_words}\n```\n\n"
            f"| a | {long_words} |\n| - | - |\n\n"
            f"[ref]: https://example.com/{'x' * 130}\n"
        )
        self.assertEqual(self._write(original), original)

    def test_headings_and_html_blocks_are_left_alone(self) -> None:
        long_words = "word " * 40
        original = f"# {long_words}\n\n<div>\n{long_words}\n</div>\n\n<!-- {long_words} -->\n"
        self.assertEqual(self._write(original), original)

    def test_no_wrapped_line_starts_with_a_block_opening_word(self) -> None:
        words = ["word"] * 40
        openers = ("-", "+", "*", "1.", "#", ">", "===", "---", "***", "___", "|", "```")
        cases = [(opener, position) for opener in openers for position in range(5, 35)]
        paragraphs = [
            " ".join([*words[:position], opener, *words[position:]]) for opener, position in cases
        ]
        for soft in ((), ("--soft",)):
            text = self._write("\n\n".join(paragraphs) + "\n", "--width", "40", *soft)
            for (opener, position), block, paragraph in zip(
                cases, text.split("\n\n"), paragraphs, strict=True
            ):
                with self.subTest(opener=opener, position=position, soft=bool(soft)):
                    lines = block.splitlines()
                    self.assertFalse(any(BLOCK_OPENER.match(line) for line in lines[1:]), lines)
                    self.assertEqual(_rendering(block), _rendering(paragraph))

    def test_code_spans_and_links_are_never_split(self) -> None:
        span = "`" + "inline code " * 12 + "`"
        link = "[link text that is long](https://example.com/" + "y" * 40 + ")"
        # The span is longer than the width, so the run reports it as over the limit.
        status, text, out = self._write_any(
            f"Before {span} middle {link} after.\n", "--width", "60"
        )
        self.assertEqual(status, EXIT_FINDINGS)
        self.assertEqual(out, "doc.md:1: over limit: a word longer than 60 characters\n")
        joined = text.replace("\\\n", " ")
        self.assertIn(span, joined)
        self.assertIn(link, joined)
        self.assertNotIn("\\\n", span)

    def test_list_items_and_quotes_keep_their_prefixes(self) -> None:
        text = self._write(f"- {LONG}\n\n> {LONG}\n")
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("- "))
        self.assertTrue(lines[1].startswith("  ") and not lines[1].startswith("   "))
        quoted = [line for line in lines if line.startswith(">")]
        self.assertGreater(len(quoted), 1)

    def test_nested_prefixes_rebuild_from_the_source(self) -> None:
        text = self._write(f"> - {LONG}\n\n  1. {LONG}\n\n10. {LONG}\n", "--width", "60")
        blocks = text.split("\n\n")
        self.assertEqual(
            {line[:4] for line in blocks[0].splitlines()},
            {"> - ", ">   "},
        )
        self.assertEqual({line[:5] for line in blocks[1].splitlines()}, {"  1. ", "     "})
        self.assertEqual({line[:4] for line in blocks[2].splitlines()}, {"10. ", "    "})

    def test_a_missing_file_is_an_error(self) -> None:
        result = _run(str(self.root / "missing.md"))
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("missing.md", result.stderr)
        self.assertTrue(result.stderr.startswith("mdwrap: error: cannot read "))

    def test_a_width_below_the_floor_is_a_usage_error(self) -> None:
        result = _run("--width", "5", str(self._file("text\n")))
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("mdwrap: error: argument --width", result.stderr)

    def test_no_files_is_a_usage_error(self) -> None:
        result = _run()
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("mdwrap: error:", result.stderr)

    def test_help_shows_an_example(self) -> None:
        result = _run("--help")
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertIn("example:", result.stdout)
        self.assertIn("--write --width 100", result.stdout)
        for option in ("--write", "--soft", "--width"):
            self.assertIn(option, result.stdout)

    def test_a_missing_dependency_exits_with_a_hint(self) -> None:
        program = (
            "import runpy, sys\n"
            "sys.modules['markdown_it'] = None\n"  # makes `import markdown_it` raise ImportError
            f"sys.argv = ['mdwrap.py', {str(self._file('text\n'))!r}]\n"
            f"runpy.run_path({str(SCRIPT)!r}, run_name='__main__')\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", program], check=False, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("mdwrap: error: cannot import a required package", result.stderr)
        self.assertIn("uv run scripts/mdwrap.py", result.stderr)
        self.assertIn("pip install markdown-it-py mdit-py-plugins", result.stderr)

    def test_the_script_declares_its_dependencies_inline(self) -> None:
        header = SCRIPT.read_text(encoding="utf-8").split('"""', 1)[0]
        self.assertIn("# /// script", header)
        self.assertRegex(header, r'dependencies = \[.*"markdown-it-py.*"mdit-py-plugins')

    def test_exit_status_reflects_what_is_left(self) -> None:
        self.assertEqual(self._check(f"{LONG}\n")[0], EXIT_FINDINGS)
        self.assertEqual(self._check("short\n")[0], EXIT_CLEAN)
        status, _, _ = self._write_any(f"{LONG}\n")
        self.assertEqual(status, EXIT_CLEAN)
        status, _, out = self._write_any(f"$$ {LONG}\n")
        self.assertEqual(
            (status, out), (EXIT_FINDINGS, "doc.md:1: skipped: possible display math\n")
        )

    def test_a_line_with_no_whitespace_past_the_width_is_left_alone(self) -> None:
        # markdownlint's MD013 accepts it, because no break can shorten it.
        url = "https://example.com/" + "a" * 120
        for text in (f"{'x' * 130}\n", f"- [A long link]({url})\n"):
            status, out = self._check(text)
            self.assertEqual((status, out), (EXIT_CLEAN, ""), text)


class MdwrapSoftModeTests(ScriptTestCase):
    """The `--soft` option wraps with plain line breaks."""

    def test_soft_wrapping_adds_no_backslashes(self) -> None:
        text = self._write(f"{LONG}\n", "--soft")
        self.assertGreater(len(text.splitlines()), 1)
        self.assertNotIn("\\", text)
        self.assertTrue(all(len(line) <= 120 for line in text.splitlines()))

    def test_soft_mode_keeps_a_backslash_break_as_deliberate(self) -> None:
        original = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu\\\nsecond segment words that are also quite long enough to need wrapping at the width ok\\\nthird\n"
        self.assertEqual(
            self._write(original, "--width", "30", "--soft"),
            "Alpha beta gamma delta\nepsilon zeta eta theta iota\nkappa lambda mu\\\nsecond segment words that are\n"
            "also quite long enough to\nneed wrapping at the width ok\\\nthird\n",
        )

    def test_hard_mode_treats_a_backslash_break_as_an_earlier_wrap(self) -> None:
        original = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu\\\nsecond segment words that are also quite long enough to need wrapping at the width ok\\\nthird\n"
        self.assertEqual(
            self._write(original, "--width", "30"),
            "Alpha beta gamma delta\\\nepsilon zeta eta theta iota\\\nkappa lambda mu second\\\nsegment words that are also\\\n"
            "quite long enough to need\\\nwrapping at the width ok\\\nthird\n",
        )

    def test_a_paragraph_that_fits_is_untouched_in_both_modes(self) -> None:
        original = REPRODUCTIONS["soft-wrapped"]
        for options in ((), ("--soft",)):
            with self.subTest(options=options):
                self.assertEqual(self._check(original, "--width", "65", *options), (EXIT_CLEAN, ""))
                self.assertEqual(self._write(original, "--width", "65", *options), original)


class MdwrapStructureTests(ScriptTestCase):
    """Parser-decided structure, inline atoms, line-start hazards, file handling and tested limitations."""

    def test_code_spans_of_any_backtick_run_length_never_break(self) -> None:
        text = self._write(REPRODUCTIONS["double-backtick-in-list"], "--width", "60")
        self.assertIn("`` `GPL-2.0-or-later` ``", text)
        self.assertIn("`` `MIT AND CC-BY-SA-4.0` ``", text)
        text = self._write(REPRODUCTIONS["double-backtick-span"], "--width", "60")
        self.assertIn("``a`b``", text)
        self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS["double-backtick-span"]))

    def test_a_code_span_broken_by_hand_stays_one_unit(self) -> None:
        text = self._write(REPRODUCTIONS["code-span-edge-space"], "--width", "60")
        self.assertIn("` example-value`", text)
        text = self._write(REPRODUCTIONS["code-span"], "--width", "60")
        self.assertIn("`very long code span with several words inside it`", text)

    def test_fences_inside_lists_and_quotes_are_not_prose(self) -> None:
        for name in ("fence-nested-list", "fence-in-quote", "fence-four-space-list"):
            with self.subTest(name=name):
                original = REPRODUCTIONS[name]
                self.assertEqual(self._write(original, "--width", "60"), original)

    def test_a_paragraph_next_to_a_nested_fence_is_still_wrapped(self) -> None:
        original = f"- {LONG}\n  ```sh\n  {'x ' * 80}\n  ```\n"
        text = self._write(original, "--width", "60")
        self.assertTrue(text.endswith(f"  ```sh\n  {'x ' * 80}\n  ```\n"))
        wrapped_item = text.split("  ```sh")[0].splitlines()
        self.assertGreater(len(wrapped_item), 1, "the list item's paragraph is wrapped")
        self.assertTrue(all(len(line) <= 60 for line in wrapped_item), wrapped_item)

    def test_two_space_and_html_breaks_stay_and_split_the_paragraph(self) -> None:
        for name in ("trailing-space-break", "label-lines", "empty-list-items"):
            with self.subTest(name=name):
                original = REPRODUCTIONS[name]
                self.assertEqual(self._write(original, "--width", "60"), original)
        original = (
            "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu  \n"
            "second segment words that are also quite long enough to need wrapping at the width ok\n"
            "third line<br>\nfourth segment short\n"
        )
        self.assertEqual(
            self._write(original, "--width", "30"),
            "Alpha beta gamma delta\\\nepsilon zeta eta theta iota\\\nkappa lambda mu  \nsecond segment words that are\\\n"
            "also quite long enough to\\\nneed wrapping at the width ok\\\nthird line<br>\nfourth segment short\n",
        )

    def test_unbalanced_backticks_and_brackets_do_not_stop_wrapping(self) -> None:
        for name in ("unbalanced-backtick", "unbalanced-bracket"):
            with self.subTest(name=name):
                text = self._write(REPRODUCTIONS[name], "--width", "60")
                self.assertGreater(len(text.splitlines()), 1)
                self.assertTrue(all(len(line) <= 60 for line in text.splitlines()), text)
                self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS[name]))

    def test_tables_with_or_without_outer_pipes_are_left_alone(self) -> None:
        for name in ("table-no-leading-pipe", "table-row-no-pipe-long"):
            with self.subTest(name=name):
                original = REPRODUCTIONS[name]
                self.assertEqual(self._write(original, "--width", "60"), original)

    def test_a_number_is_never_left_at_a_line_start(self) -> None:
        text = self._write(REPRODUCTIONS["number-line-start"], "--width", "60")
        self.assertIn("2026.", text)
        self.assertFalse(any(line.startswith("2026.") for line in text.splitlines()))

    def test_a_line_start_escape_is_dropped_when_the_word_moves_mid_line(self) -> None:
        original = "The example release shipped in the year\n2018\\. It was a good one and this sentence keeps going on.\n"
        text = self._write(original, "--width", "50")
        self.assertIn("year 2018. It", text)
        self.assertNotIn("\\.", text)

    def test_a_line_start_escape_stays_where_the_word_opens_a_line(self) -> None:
        words = ["word"] * 12
        original = " ".join([*words, "2018\\.", *words]) + "\n"
        text = self._write(original, "--width", "20", "--soft")
        for line in text.splitlines():
            if line.startswith("2018"):
                self.assertTrue(line.startswith("2018\\."), line)
            self.assertFalse(line.endswith("2018\\."), line)
        self.assertEqual(_rendering(text), _rendering(original))

    def test_lines_over_the_width_are_reported_not_ignored(self) -> None:
        status, out = self._check(REPRODUCTIONS["long-link"], "--width", "60")
        self.assertEqual(status, EXIT_FINDINGS)
        self.assertEqual(
            out,
            "doc.md:1: rewrap: line exceeds 60 characters\n"
            "doc.md:3: rewrap: line exceeds 60 characters\n",
        )
        status, text, out = self._write_any(REPRODUCTIONS["long-link"], "--width", "60")
        # The unbreakable URL ends up alone on its line, which MD013 accepts, so nothing is left to report.
        self.assertEqual(status, EXIT_CLEAN)
        self.assertEqual(out, "")
        self.assertIn(
            "\nhttps://example.com/a/very/long/path/that/never/ends/and/cannot/be/broken/at/all/so/",
            text,
        )
        link = "here](https://example.com/a)"
        self.assertIn(link, text)

    def test_an_inline_html_start_is_prose_and_wraps(self) -> None:
        text = self._write(REPRODUCTIONS["inline-html-start"], "--width", "60")
        self.assertTrue(all(len(line) <= 60 for line in text.splitlines()), text)
        self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS["inline-html-start"]))

    def test_list_continuations_indented_four_spaces_are_wrapped(self) -> None:
        text = self._write(REPRODUCTIONS["nested-list"], "--width", "60")
        self.assertTrue(all(len(line) <= 60 for line in text.splitlines()), text)
        self.assertIn(
            "    - Nested example item indented four spaces that is long\\\n      enough", text
        )
        self.assertIn(
            "    A continuation paragraph indented four spaces that is\\\n    long enough", text
        )

    def test_the_first_line_of_a_footnote_definition_is_wrapped(self) -> None:
        text = self._write(REPRODUCTIONS["footnote"], "--width", "60")
        self.assertTrue(all(len(line) <= 60 for line in text.splitlines()), text)
        self.assertIn(
            "[^1]: An example footnote text that is long enough to pass\\\n    the sixty column limit",
            text,
        )
        self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS["footnote"]))

    def test_thematic_breaks_between_paragraphs_are_not_front_matter(self) -> None:
        text = self._write(REPRODUCTIONS["front-matter-lookalike"], "--width", "60")
        self.assertTrue(all(len(line) <= 60 for line in text.splitlines()), text)
        self.assertTrue(text.startswith("---\n\nAn example intro"))

    def test_html_blocks_and_comments_are_never_rewrapped(self) -> None:
        for name in ("html-block", "html-block-text"):
            with self.subTest(name=name):
                original = REPRODUCTIONS[name]
                self.assertEqual(self._write(original, "--width", "60"), original)

    def test_a_formatter_off_region_is_skipped_silently(self) -> None:
        original = REPRODUCTIONS["ignore-region"]
        self.assertEqual(self._check(original, "--width", "60"), (EXIT_CLEAN, ""))
        self.assertEqual(self._write(original, "--width", "60"), original)
        text = self._write(original + f"\n{LONG}\n", "--width", "60")
        self.assertTrue(text.startswith(original))
        self.assertGreater(len(text.removeprefix(original).splitlines()), 2)

    def test_a_literal_backslash_never_meets_the_hard_break_marker(self) -> None:
        for name in ("escaped-backslash", "backslash-at-line-end"):
            for width in range(21, 62):
                with self.subTest(name=name, width=width):
                    text = self._write(REPRODUCTIONS[name], "--width", str(width))
                    for line in text.splitlines()[:-1]:
                        self.assertEqual(
                            (len(line) - len(line.rstrip("\\"))) % 2, 1, line
                        )  # the marker, after any escaped pairs
                    self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS[name]))
        text = self._write(REPRODUCTIONS["escaped-backslash"], "--width", "60")
        self.assertTrue(text.endswith("trailing backslash\\\\\n"))

    def test_a_backslash_ending_a_word_is_never_a_break_point(self) -> None:
        for soft in ((), ("--soft",)):
            text = self._write(REPRODUCTIONS["backslash-at-line-end"], "--width", "46", *soft)
            self.assertIn("C:\\Example\\ in", text)

    def test_crlf_line_endings_and_a_byte_order_mark_survive(self) -> None:
        text = self._write(REPRODUCTIONS["crlf"], "--width", "60")
        self.assertEqual(text.count("\r\n"), text.count("\n"))
        self.assertIn("sixty\\\r\ncolumn limit", text)
        self.assertEqual(
            self._write(REPRODUCTIONS["bom-front-matter"], "--width", "60"),
            REPRODUCTIONS["bom-front-matter"],
        )
        body = "\ufeff" + f"{LONG}\n"
        text = self._write(body, "--width", "60")
        self.assertTrue(text.startswith("\ufeffThis sentence"))
        self.assertEqual(text.count("\ufeff"), 1)

    def test_rule_and_pipe_tokens_never_open_a_wrapped_line(self) -> None:
        for name in ("thematic-token", "underscore-rule", "pipe-line-start"):
            for width in range(20, 70):
                with self.subTest(name=name, width=width):
                    text = self._write(REPRODUCTIONS[name], "--width", str(width))
                    self.assertFalse(
                        any(BLOCK_OPENER.match(line) for line in text.splitlines()[1:]), text
                    )
                    self.assertEqual(_rendering(text), _rendering(REPRODUCTIONS[name]))

    def test_an_unreadable_file_stops_every_write(self) -> None:
        first = self._file(f"{LONG}\n", "first.md")
        third = self._file(f"{LONG}\n", "third.md")
        status, _, err = _main("--write", str(first), str(self.root / "missing.md"), str(third))
        self.assertEqual(status, EXIT_ERROR)
        self.assertIn("mdwrap: error: cannot read", err)
        self.assertEqual(self._text(first), f"{LONG}\n")
        self.assertEqual(self._text(third), f"{LONG}\n")
        bad = self.root / "bad.md"
        bad.write_bytes(b"\xff\xfe broken")
        status, _, err = _main("--write", str(third), str(bad))
        self.assertEqual(status, EXIT_ERROR)
        self.assertIn("cannot read", err)
        self.assertEqual(self._text(third), f"{LONG}\n")
        self.assertEqual(
            sorted(path.name for path in self.root.iterdir()), ["bad.md", "first.md", "third.md"]
        )

    def test_several_files_are_rewritten_through_temporary_files(self) -> None:
        one = self._file(f"{LONG}\n", "one.md")
        two = self._file(f"{LONG}\n", "two.md")
        status, out, err = _main("--write", str(one), str(two))
        self.assertEqual((status, out), (EXIT_CLEAN, ""))
        self.assertEqual(err, "mdwrap: 2 file(s), 2 paragraph(s) rewrapped, 0 skipped\n")
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["one.md", "two.md"])
        self.assertGreater(len(self._text(one).splitlines()), 1)

    # Tested limitations: behaviour the specification keeps as it is.

    def test_limitation_a_stranded_last_line_is_not_balanced(self) -> None:
        text = self._write(REPRODUCTIONS["stranded-last-line"], "--width", "60")
        self.assertEqual(text.splitlines()[-1], "listening.")

    def test_limitation_width_counts_code_points_not_display_columns(self) -> None:
        wide = "日本語の例文です。" * 12 + "\n"
        self.assertEqual(self._check(wide), (EXIT_CLEAN, ""))
        self.assertEqual(self._write(wide), wide)

    def test_limitation_display_math_is_skipped_not_rewrapped(self) -> None:
        status, text, out = self._write_any(REPRODUCTIONS["math-block"], "--width", "60")
        self.assertEqual(status, EXIT_FINDINGS)
        self.assertEqual(text, REPRODUCTIONS["math-block"])
        self.assertEqual(out, "doc.md:1: skipped: possible display math\n")

    def test_limitation_a_bracket_group_that_is_not_a_link_may_span_lines(self) -> None:
        # mdformat escapes the brackets of such a group once a hard break splits it; soft wrapping shows the split.
        original = "Alpha beta gamma [delta epsilon zeta] eta theta iota kappa lambda mu nu xi.\n"
        text = self._write(original, "--width", "30", "--soft")
        self.assertIn("[delta\nepsilon", text)

    def test_limitation_closing_dots_do_not_end_yaml_front_matter(self) -> None:
        original = f"---\ntitle: Example\n...\n\n{LONG}\n"
        self.assertEqual(self._check(original)[0], EXIT_FINDINGS)


class MdwrapSafetyTests(ScriptTestCase):
    """The rendering check keeps a paragraph whose rewrap would change what the document says."""

    TEXT = "Alpha beta gamma [delta epsilon zeta] eta theta iota kappa lambda mu nu xi.\n\n[delta epsilon zeta]: https://example.com/x\n"

    def test_a_reference_label_broken_by_a_hard_break_is_skipped(self) -> None:
        status, out = self._check(self.TEXT, "--width", "30")
        self.assertEqual(status, EXIT_FINDINGS)
        self.assertEqual(out, "doc.md:1: skipped: rewrap would change the rendering\n")
        status, text, out = self._write_any(self.TEXT, "--width", "30")
        self.assertEqual((status, text), (EXIT_FINDINGS, self.TEXT))
        self.assertEqual(out, "doc.md:1: skipped: rewrap would change the rendering\n")

    def test_the_same_paragraph_wraps_softly_because_a_soft_break_keeps_the_label(self) -> None:
        text = self._write(self.TEXT, "--width", "30", "--soft")
        self.assertEqual(_rendering(text), _rendering(self.TEXT))
        self.assertNotEqual(text, self.TEXT)

    def test_a_skipped_paragraph_does_not_stop_the_others(self) -> None:
        status, text, out = self._write_any(f"{self.TEXT}\n{LONG}\n", "--width", "30")
        self.assertEqual(status, EXIT_FINDINGS)
        self.assertTrue(text.startswith(self.TEXT))
        self.assertGreater(len(text.splitlines()), len(self.TEXT.splitlines()) + 3)
        self.assertEqual(out, "doc.md:1: skipped: rewrap would change the rendering\n")

    def test_the_summary_counts_skipped_paragraphs(self) -> None:
        _, _, err = _main("--width", "30", str(self._file(self.TEXT)))
        self.assertEqual(err, "mdwrap: 1 file(s), 0 paragraph(s) to rewrap, 1 skipped\n")


class MdwrapIdempotenceTests(ScriptTestCase):
    """Running the script twice changes nothing the second time, and the rendering never changes."""

    def test_every_reproduction_is_stable_and_renders_the_same(self) -> None:
        for name, original in REPRODUCTIONS.items():
            for width in (30, 60, 120):
                for soft in ((), ("--soft",)):
                    with self.subTest(name=name, width=width, soft=bool(soft)):
                        path = self._file(original)
                        _main("--write", "--width", str(width), *soft, str(path))
                        once = path.read_bytes()
                        _main("--write", "--width", str(width), *soft, str(path))
                        self.assertEqual(path.read_bytes(), once)
                        _, out, _ = _main("--width", str(width), *soft, str(path))
                        self.assertNotIn(": rewrap:", out)
                        self.assertEqual(_rendering(once.decode("utf-8")), _rendering(original))


if __name__ == "__main__":
    unittest.main()
