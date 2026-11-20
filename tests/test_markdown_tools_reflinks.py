"""Behavioral tests for the markdown-tools skill's reflinks.py, run as the command agents call."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("markdown-tools") / "scripts" / "reflinks.py"

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2

OLD = """---
title: Guide
---
# Guide

Read [the **guide**](docs/guide.md#setup "Setup") or [the site](https://example.com/a).
An image ![logo](img/logo.png) sits here, and a [multi
line link](https://example.com/b) wraps.
"""

NEW = """---
title: Guide
---
# Guide

Read [the **guide**][guide] or [the site][site].
An image ![logo][logo] sits here, and a [multi line link][wrapped] wraps.

[guide]: docs/guide.md#setup "Setup"
[site]: https://example.com/a
[logo]: img/logo.png
[wrapped]: https://example.com/b
"""


def line_of(text: str, fragment: str) -> int:
    """Return the 1-based number of the first line of `text` that contains `fragment`."""
    for number, line in enumerate(text.split("\n"), start=1):
        if fragment in line:
            return number
    raise AssertionError(f"{fragment!r} is not in the text")


class ReflinksTestCase(unittest.TestCase):
    directory: Path
    old_path: Path
    new_path: Path

    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory)
        self.old_path = self.directory / "old.md"
        self.new_path = self.directory / "new.md"

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

    def compare(self, old: str, new: str) -> subprocess.CompletedProcess[str]:
        """Check `old` against `new`, written to `self.old_path` and `self.new_path`."""
        _ = self.old_path.write_text(old, encoding="utf-8")
        _ = self.new_path.write_text(new, encoding="utf-8")
        return self.run_check(str(self.old_path), str(self.new_path))


class ReportsConversionLoss(ReflinksTestCase):
    def test_a_clean_conversion_exits_zero(self) -> None:
        result = self.compare(OLD, NEW)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "reflinks: 1 file pair(s), 0 link(s) lost, 0 link(s) added, 0 unused definition(s), "
            "0 undefined reference(s)\n",
        )

    def test_a_lost_link_is_reported_at_its_old_line(self) -> None:
        new = NEW.replace(" or [the site][site]", "").replace("[site]: https://example.com/a\n", "")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout,
            f"{self.old_path}:{line_of(OLD, 'the site')}: link lost: [the site](https://example.com/a)\n",
        )

    def test_a_changed_destination_is_lost_and_added(self) -> None:
        new = NEW.replace("[site]: https://example.com/a", "[site]: https://example.com/other")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{self.old_path}:{line_of(OLD, 'the site')}: link lost: [the site](https://example.com/a)",
                f"{self.new_path}:{line_of(new, 'the site')}: "
                "link added: [the site](https://example.com/other)",
            ],
        )

    def test_a_changed_fragment_is_reported(self) -> None:
        new = NEW.replace("docs/guide.md#setup", "docs/guide.md#install")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{self.old_path}:{line_of(OLD, 'the **guide**')}: "
                'link lost: [the **guide**](docs/guide.md#setup "Setup")',
                f"{self.new_path}:{line_of(new, 'the **guide**')}: "
                'link added: [the **guide**](docs/guide.md#install "Setup")',
            ],
        )

    def test_a_changed_title_is_reported(self) -> None:
        new = NEW.replace(' "Setup"', ' "Install"')
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn('link added: [the **guide**](docs/guide.md#setup "Install")', result.stdout)

    def test_dropped_emphasis_in_the_text_is_a_change(self) -> None:
        new = NEW.replace("[the **guide**][guide]", "[the guide][guide]")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn(
            f"{self.old_path}:{line_of(OLD, 'the **guide**')}: link lost: [the **guide**]",
            result.stdout,
        )
        self.assertIn(
            f"{self.new_path}:{line_of(new, 'the guide')}: link added: [the guide]", result.stdout
        )

    def test_changed_text_is_reported(self) -> None:
        new = NEW.replace("[the site][site]", "[our site][site]")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{self.old_path}:{line_of(OLD, 'the site')}: link lost: [the site](https://example.com/a)",
                f"{self.new_path}:{line_of(new, 'our site')}: link added: [our site](https://example.com/a)",
            ],
        )

    def test_a_link_text_wrapped_over_two_lines_matches_the_same_text_on_one_line(self) -> None:
        # OLD wraps "multi\nline link"; NEW joins it. Neither whitespace nor line breaks count.
        result = self.compare(OLD, NEW)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_a_changed_image_is_reported(self) -> None:
        new = NEW.replace("[logo]: img/logo.png", "[logo]: img/mark.png")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{self.old_path}:{line_of(OLD, '![logo]')}: link lost: ![logo](img/logo.png)",
                f"{self.new_path}:{line_of(new, '![logo]')}: link added: ![logo](img/mark.png)",
            ],
        )

    def test_a_link_deep_in_a_paragraph_is_located_by_its_line(self) -> None:
        old = "# T\n\nfirst line\nsecond line\nthird [a](https://example.com/a) line\n"
        result = self.compare(old, "# T\n\nfirst line\nsecond line\nthird a line\n")
        self.assertEqual(
            result.stdout,
            f"{self.old_path}:{line_of(old, 'third')}: link lost: [a](https://example.com/a)\n",
        )


class ReportsReferenceProblems(ReflinksTestCase):
    def test_an_unused_definition_is_reported_with_its_label_as_written(self) -> None:
        new = NEW + "[Spare Label]: https://example.com/spare\n"
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout,
            f"{self.new_path}:{line_of(new, 'Spare Label')}: unused definition: [Spare Label]\n",
        )

    def test_an_undefined_reference_is_reported_at_its_line(self) -> None:
        new = NEW.replace("[the site][site]", "[the site][siet]")
        result = self.compare(OLD, new)
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{self.old_path}:{line_of(OLD, 'the site')}: link lost: [the site](https://example.com/a)",
                f"{self.new_path}:{line_of(new, '[site]: ')}: unused definition: [site]",
                f"{self.new_path}:{line_of(new, '[siet]')}: undefined reference: [siet]",
            ],
        )

    def test_a_shortcut_reference_without_a_definition_is_reported(self) -> None:
        text = "# T\n\nSee [missing] here.\n"
        result = self.compare(text, text)
        self.assertEqual(
            result.stdout,
            f"{self.new_path}:{line_of(text, '[missing]')}: undefined reference: [missing]\n",
        )

    def test_text_that_only_looks_like_a_reference_is_not_reported(self) -> None:
        cases = {
            "an escaped bracket": "Write \\[literal\\] here.\n",
            "a code span": "Write `[code]` here.\n",
            "a footnote marker": "A claim [^1] here.\n",
            "a task marker": "- [x] done\n- [ ] open\n",
            "an alert marker": "> [!NOTE]\n> Careful.\n",
        }
        for name, text in cases.items():
            with self.subTest(name):
                result = self.compare(text, text)
                self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_definitions_and_labels_match_case_and_whitespace_insensitively(self) -> None:
        text = "[A  Label][a label] and [x].\n\n[A LABEL]: https://example.com/one\n[X]: https://example.com/two\n"
        result = self.compare(text, text)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout)

    def test_a_line_separator_character_does_not_shift_definition_lines(self) -> None:
        # str.splitlines would split at U+0085 and U+2028; the parser does not, so line numbers must not move.
        text = "Odd\x85text\u2028here.\n\n[Spare]: https://example.com/spare\n"
        result = self.compare(text, text)
        self.assertEqual(
            result.stdout,
            f"{self.new_path}:{line_of(text, '[Spare]')}: unused definition: [Spare]\n",
        )


class HandlesPairsAndErrors(ReflinksTestCase):
    def test_several_pairs_are_checked_and_counted(self) -> None:
        old_path = self.write("old.md", OLD)
        new_path = self.write("new.md", NEW)
        broken = self.write("broken.md", NEW.replace("example.com/a", "example.com/z"))
        result = self.run_check(str(old_path), str(new_path), str(old_path), str(broken))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn(f"{old_path}:6: link lost:", result.stdout)
        self.assertTrue(
            result.stderr.startswith("reflinks: 2 file pair(s), 1 link(s) lost, 1 link(s) added")
        )

    def test_a_missing_file_exits_two(self) -> None:
        new_path = self.write("new.md", NEW)
        result = self.run_check(str(self.directory / "absent.md"), str(new_path))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("reflinks.py: error: cannot read "), result.stderr)

    def test_an_odd_number_of_files_exits_two_with_a_hint(self) -> None:
        new_path = self.write("new.md", NEW)
        result = self.run_check(str(new_path))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn(
            "reflinks.py: error: invalid arguments: expected OLD NEW pairs", result.stderr
        )
        self.assertIn("hint:", result.stderr)

    def test_no_arguments_exits_two(self) -> None:
        self.assertEqual(self.run_check().returncode, EXIT_USAGE)

    def test_help_shows_one_example(self) -> None:
        result = self.run_check("--help")
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertEqual(result.stdout.count("example:"), 1)

    def test_a_missing_dependency_exits_two(self) -> None:
        # -S leaves site-packages off the path, so markdown-it-py cannot be imported.
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(SCRIPT), "a.md", "b.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertTrue(
            result.stderr.startswith("reflinks.py: error: cannot import"), result.stderr
        )
        self.assertIn("uv run", result.stderr)


class RunsStandalone(ReflinksTestCase):
    def test_a_copy_outside_the_repository_works(self) -> None:
        copy = self.directory / "reflinks.py"
        _ = shutil.copy(SCRIPT, copy)
        old_path = self.write("old.md", OLD)
        new_path = self.write("new.md", NEW.replace("example.com/a", "example.com/z"))
        result = self.run_check(old_path.name, new_path.name, script=copy, cwd=self.directory)
        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "old.md:6: link lost: [the site](https://example.com/a)",
                "new.md:6: link added: [the site](https://example.com/z)",
            ],
        )


if __name__ == "__main__":
    unittest.main()
