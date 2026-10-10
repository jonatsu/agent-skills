"""Behavioral tests for the repo-management skill's Markdown rewrap script."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("repo-management") / "scripts" / "mdwrap.py"

EXIT_CLEAN = 0
EXIT_WOULD_CHANGE = 1
EXIT_ERROR = 2

LONG = (
    "This sentence is long enough that the wrapper has to break it somewhere, and it keeps going "
    "for a while so that it needs more than one line at the default width of the script."
)
# A line that a wrap would turn into a list, heading, quote or fence if it began with one of these.
BLOCK_OPENER = re.compile(r"^\s*(?:[-+*]|\d{1,9}[.)]|#{1,6}|>|=+|```|~~~)(?:\s|$)")


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


class MdwrapTests(unittest.TestCase):
    """Cover rewrapping, the structures it must leave alone, and its exit statuses."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def _file(self, text: str) -> Path:
        path = self.root / "doc.md"
        path.write_text(text, encoding="utf-8")
        return path

    def _write(self, text: str, *options: str) -> str:
        path = self._file(text)
        result = _run("--write", *options, str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)
        return path.read_text(encoding="utf-8")

    def test_check_mode_reports_and_changes_nothing(self) -> None:
        path = self._file(f"# Title\n\n{LONG}\n")
        result = _run(str(path))
        self.assertEqual(result.returncode, EXIT_WOULD_CHANGE)
        self.assertIn(f"{path}:3: 1 -> 2 lines", result.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), f"# Title\n\n{LONG}\n")

    def test_write_uses_hard_breaks_within_the_width_and_is_idempotent(self) -> None:
        path = self._file(f"{LONG}\n")
        _run("--write", str(path))
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertTrue(all(len(line) <= 120 for line in lines))
        self.assertTrue(all(line.endswith("\\") for line in lines[:-1]))
        self.assertFalse(lines[-1].endswith("\\"))
        self.assertEqual(_run(str(path)).returncode, EXIT_CLEAN)

    def test_soft_wrapped_lines_become_one_hard_broken_block(self) -> None:
        text = self._write("one two\nthree four\nfive six\n", "--width", "20")
        self.assertEqual(text, "one two three four\\\nfive six\n")

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

    def test_no_wrapped_line_starts_with_a_block_opening_word(self) -> None:
        words = ["word"] * 40
        for opener in ("-", "+", "*", "1.", "#", ">", "===", "```"):
            for position in range(5, 35):
                with self.subTest(opener=opener, position=position):
                    text = " ".join([*words[:position], opener, *words[position:]])
                    lines = self._write(text + "\n", "--width", "40").splitlines()
                    self.assertFalse(any(BLOCK_OPENER.match(line) for line in lines[1:]), lines)

    def test_code_spans_and_links_are_never_split(self) -> None:
        span = "`" + "inline code " * 12 + "`"
        link = "[link text that is long](https://example.com/" + "y" * 40 + ")"
        text = self._write(f"Before {span} middle {link} after.\n", "--width", "60")
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

    def test_a_missing_file_is_an_error(self) -> None:
        result = _run(str(self.root / "missing.md"))
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("missing.md", result.stderr)

    def test_a_width_below_the_floor_is_a_usage_error(self) -> None:
        result = _run("--width", "5", str(self._file("text\n")))
        self.assertEqual(result.returncode, EXIT_ERROR)


if __name__ == "__main__":
    unittest.main()
