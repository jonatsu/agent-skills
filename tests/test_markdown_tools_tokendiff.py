"""Behavioral tests for the markdown-tools skill's tokendiff.py, run as the command agents call."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("markdown-tools") / "scripts" / "tokendiff.py"

EXIT_CLEAN = 0
EXIT_LOST = 1
EXIT_USAGE = 2

SOURCE = """---
title: Widget Guide
---
# Widget guide

Install the widget with `widget-cli --verbose` and read docs/setup.md.
The widget is small, and the widget is fast.
"""


class TokendiffTestCase(unittest.TestCase):
    directory: Path

    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory)

    def write(self, name: str, text: str) -> Path:
        path = self.directory / name
        _ = path.write_text(text, encoding="utf-8")
        return path

    def run_check(
        self, *arguments: str, script: Path = SCRIPT, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-I", str(script), *arguments],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        )

    def compare(
        self, source: str, destination: str, *extra: str
    ) -> subprocess.CompletedProcess[str]:
        source_path = self.write("source.md", source)
        destination_path = self.write("destination.md", destination)
        return self.run_check("--from", str(source_path), "--to", str(destination_path), *extra)


class ReportsLostWords(TokendiffTestCase):
    def test_a_move_with_reordering_loses_nothing(self) -> None:
        moved = (
            "The widget is small, and the widget is fast.\n\n"
            "# Widget guide\n\n"
            "Install the widget with `widget-cli --verbose` and read docs/setup.md.\n\n"
            "Added words are fine.\n"
        )
        result = self.compare(SOURCE, moved)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)
        self.assertEqual(result.stdout, "")
        self.assertRegex(
            result.stderr, r"^tokendiff: \d+ source token\(s\), 0 lost occurrence\(s\), 0 distinct"
        )

    def test_a_lost_word_is_reported_with_its_counts(self) -> None:
        result = self.compare(
            SOURCE, SOURCE.replace("small, and the widget is fast", "small, and fast")
        )
        self.assertEqual(result.returncode, EXIT_LOST)
        self.assertEqual(result.stdout, "is: lost 1 of 2\nthe: lost 1 of 2\nwidget: lost 1 of 3\n")
        self.assertTrue(
            result.stderr.endswith("3 lost occurrence(s), 3 distinct token(s) short\n"),
            result.stderr,
        )

    def test_the_largest_loss_comes_first(self) -> None:
        result = self.compare("alpha alpha alpha beta gamma gamma\n", "beta\n")
        self.assertEqual(result.stdout, "alpha: lost 3 of 3\ngamma: lost 2 of 2\n")
        self.assertEqual(result.returncode, EXIT_LOST)

    def test_a_token_compares_case_sensitively_and_keeps_inner_punctuation(self) -> None:
        result = self.compare(
            "Widget docs/setup.md v1.2-beta end.\n", "widget docs/setup.md v1.2-beta end\n"
        )
        self.assertEqual(result.stdout, "Widget: lost 1 of 1\n")

    def test_inline_code_counts_but_a_fenced_block_does_not(self) -> None:
        source = "Run `rare_flag` now.\n\n```sh\nsecret_word\n```\n\n    indented_word\n"
        result = self.compare(source, "Run now.\n")
        self.assertEqual(result.stdout, "rare_flag: lost 1 of 1\n")

    def test_a_word_only_in_a_destination_code_block_does_not_count(self) -> None:
        result = self.compare("Plain.\n", "Plain.\n\n```text\nextra_word\n```\n")
        self.assertEqual(result.returncode, EXIT_CLEAN)

    def test_mermaid_blocks_are_ignored(self) -> None:
        diagram = "```mermaid\nflowchart LR\n  Start --> Finish\n```\n"
        result = self.compare("Words.\n\n" + diagram, "Words.\n")
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_front_matter_and_html_comments_are_ignored(self) -> None:
        source = "---\ntitle: hidden\n---\nBody.\n\n<!-- note: remove me -->\n\nText <!-- inline note --> end.\n"
        result = self.compare(source, "Body.\n\nText end.\n")
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_link_destinations_do_not_count_but_link_text_does(self) -> None:
        result = self.compare(
            "See [the guide](docs/old-path.md).\n", "See [the manual](docs/new-path.md).\n"
        )
        self.assertEqual(result.stdout, "guide: lost 1 of 1\n")

    def test_html_block_text_counts_but_its_tags_do_not(self) -> None:
        result = self.compare(
            "<details><summary>Fold</summary>\nInside\n</details>\n", "Fold Inside\n"
        )
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)


class IgnoresDeliberateDeletions(TokendiffTestCase):
    def test_ignore_removes_a_word_from_the_comparison(self) -> None:
        result = self.compare(
            "keep drop other\n", "keep\n", "--ignore", "drop", "--ignore", "other"
        )
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)
        self.assertTrue(
            result.stderr.startswith("tokendiff: 1 source token(s), 0 lost"), result.stderr
        )

    def test_ignore_leaves_other_losses_reported(self) -> None:
        result = self.compare("keep drop other\n", "keep\n", "--ignore", "drop")
        self.assertEqual(result.stdout, "other: lost 1 of 1\n")

    def test_ignore_file_lists_one_word_per_line(self) -> None:
        words = self.write("ignored.txt", "drop\n\n  other  \n")
        result = self.compare("keep drop other\n", "keep\n", "--ignore-file", str(words))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)


class MergesAndSplits(TokendiffTestCase):
    def test_two_sources_merged_into_one_destination_lose_nothing(self) -> None:
        first = self.write("first.md", "# One\n\nalpha beta\n")
        second = self.write("second.md", "# Two\n\nbeta gamma\n")
        merged = self.write("merged.md", "# One and Two\n\nalpha beta\n\nbeta gamma\n")
        result = self.run_check("--from", str(first), str(second), "--to", str(merged))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_a_merge_that_dedupes_a_word_reports_the_lost_occurrence(self) -> None:
        first = self.write("first.md", "alpha beta\n")
        second = self.write("second.md", "beta gamma\n")
        merged = self.write("merged.md", "alpha beta gamma\n")
        result = self.run_check("--from", str(first), str(second), "--to", str(merged))
        self.assertEqual(result.returncode, EXIT_LOST)
        self.assertEqual(result.stdout, "beta: lost 1 of 2\n")

    def test_a_split_across_two_destinations_is_pooled(self) -> None:
        source = self.write("source.md", "alpha beta gamma\n")
        left = self.write("left.md", "alpha\n")
        right = self.write("right.md", "beta gamma\n")
        result = self.run_check("--from", str(source), "--to", str(left), str(right))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)


class RejectsBadInvocations(TokendiffTestCase):
    def test_a_missing_file_exits_two(self) -> None:
        present = self.write("present.md", "word\n")
        result = self.run_check("--from", str(self.directory / "absent.md"), "--to", str(present))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertEqual(result.stdout, "")
        self.assertTrue(
            result.stderr.startswith("tokendiff.py: error: cannot read "), result.stderr
        )

    def test_a_missing_ignore_file_exits_two(self) -> None:
        present = self.write("present.md", "word\n")
        result = self.run_check(
            "--from",
            str(present),
            "--to",
            str(present),
            "--ignore-file",
            str(self.directory / "none.txt"),
        )
        self.assertEqual(result.returncode, EXIT_USAGE)

    def test_missing_options_exit_two(self) -> None:
        present = self.write("present.md", "word\n")
        result = self.run_check("--from", str(present))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("tokendiff.py: error: invalid arguments:", result.stderr)

    def test_help_shows_one_example(self) -> None:
        result = self.run_check("--help")
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertEqual(result.stdout.count("example:"), 1)

    def test_a_missing_dependency_exits_two(self) -> None:
        # -S leaves site-packages off the path, so markdown-it-py cannot be imported.
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(SCRIPT), "--from", "a.md", "--to", "b.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertTrue(
            result.stderr.startswith("tokendiff.py: error: cannot import"), result.stderr
        )


class RunsStandalone(TokendiffTestCase):
    def test_a_copy_outside_the_repository_works(self) -> None:
        copy = self.directory / "tokendiff.py"
        _ = shutil.copy(SCRIPT, copy)
        _ = self.write("source.md", "alpha beta\n")
        _ = self.write("destination.md", "alpha\n")
        result = self.run_check(
            "--from", "source.md", "--to", "destination.md", script=copy, cwd=self.directory
        )
        self.assertEqual(result.returncode, EXIT_LOST, result.stderr)
        self.assertEqual(result.stdout, "beta: lost 1 of 1\n")


if __name__ == "__main__":
    unittest.main()
