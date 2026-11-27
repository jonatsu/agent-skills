"""Behavioral tests for the markdown-tools skill's codeblocks.py, run as the command agents call."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("markdown-tools") / "scripts" / "codeblocks.py"

EXIT_CLEAN = 0
EXIT_DIFFERENCES = 1
EXIT_USAGE = 2

DOCUMENT = """---
title: Guide
---
# Guide

Install it first.

```sh
make build \\
  --target all
```

Then set the arrow:

```py
arrow = "→"
```

An indented block follows.

    first = 1
    second = 2

Last, a diagram.

```mermaid
graph TD
  A --> B
```
"""

# Line numbers of each block's first line in DOCUMENT, in order.
SH_LINE, PY_LINE, INDENTED_LINE, MERMAID_LINE = 8, 15, 21, 26


class CodeblocksTestCase(unittest.TestCase):
    directory: Path

    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory)

    def run_check(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def compare(self, old: str | bytes, new: str | bytes) -> subprocess.CompletedProcess[str]:
        """Check `old` against `new`, written byte for byte so that line endings survive."""
        old_path = self.directory / "old.md"
        new_path = self.directory / "new.md"
        for path, content in ((old_path, old), (new_path, new)):
            _ = path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        return self.run_check(str(old_path), str(new_path))

    def edited(self, before: str, after: str) -> subprocess.CompletedProcess[str]:
        """Check DOCUMENT against a copy of it in which `before` became `after`."""
        self.assertIn(before, DOCUMENT)
        return self.compare(DOCUMENT, DOCUMENT.replace(before, after))


class AcceptsUntouchedCode(CodeblocksTestCase):
    def test_identical_files_exit_zero(self) -> None:
        result = self.compare(DOCUMENT, DOCUMENT)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "codeblocks: 4 block(s) in OLD, 4 in NEW, 0 changed, 0 missing, 0 added\n")

    def test_prose_changes_outside_code_exit_zero(self) -> None:
        rewritten = (
            DOCUMENT.replace("Install it first.", "Start by installing it.")
            .replace("# Guide", "# The guide")
            .replace("title: Guide", "title: The guide")
            .replace("Last, a diagram.", "Finally, here is a diagram.\n\nA new paragraph with `inline code`.")
        )
        result = self.compare(DOCUMENT, rewritten)
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")

    def test_a_document_without_code_blocks_exits_zero(self) -> None:
        result = self.compare("# Title\n\nJust prose.\n", "# Title\n\nJust other prose.\n")
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertIn("0 block(s) in OLD, 0 in NEW", result.stderr)


class ReportsChangedBlocks(CodeblocksTestCase):
    def assert_one_changed(self, result: subprocess.CompletedProcess[str], line: int) -> list[str]:
        self.assertEqual(result.returncode, EXIT_DIFFERENCES, result.stdout + result.stderr)
        findings = result.stdout.splitlines()
        self.assertEqual(len(findings), 1, result.stdout)
        self.assertIn(f"(line {line})", findings[0])
        self.assertIn("1 changed, 0 missing, 0 added", result.stderr)
        return findings

    def test_a_stripped_trailing_backslash_is_reported_with_both_lines(self) -> None:
        result = self.edited("make build \\\n", "make build\n")
        (finding,) = self.assert_one_changed(result, SH_LINE)
        self.assertEqual(
            finding,
            f"OLD block 1 (line {SH_LINE}), NEW block 1 (line {SH_LINE}): "
            "block line 2 differs: OLD 'make build \\\\\\n' NEW 'make build\\n'",
        )

    def test_a_unicode_symbol_swapped_for_an_ascii_look_alike_is_readable(self) -> None:
        result = self.edited("→", "->")
        (finding,) = self.assert_one_changed(result, PY_LINE)
        self.assertIn("block 2", finding)
        self.assertIn("OLD 'arrow = \"\\u2192\"\\n' NEW 'arrow = \"->\"\\n'", finding)
        self.assertTrue(finding.isascii(), finding)

    def test_a_non_breaking_space_swapped_for_a_space_is_reported(self) -> None:
        old = "```sh\necho\u00a0hi\n```\n"
        result = self.compare(old, old.replace("\u00a0", " "))
        self.assertEqual(result.returncode, EXIT_DIFFERENCES)
        self.assertIn("OLD 'echo\\xa0hi\\n' NEW 'echo hi\\n'", result.stdout)

    def test_trailing_whitespace_removed_inside_a_block_is_reported(self) -> None:
        old = DOCUMENT.replace('"→"\n', '"→"  \n')
        result = self.compare(old, DOCUMENT)
        (finding,) = self.assert_one_changed(result, PY_LINE)
        self.assertIn("\\u2192\"  \\n' NEW 'arrow = \"\\u2192\"\\n'", finding)

    def test_a_changed_language_tag_is_reported(self) -> None:
        result = self.edited("```sh\n", "```bash\n")
        (finding,) = self.assert_one_changed(result, SH_LINE)
        self.assertIn("block line 1 differs: OLD '```sh\\n' NEW '```bash\\n'", finding)

    def test_a_changed_indent_inside_an_indented_block_is_reported(self) -> None:
        result = self.edited("    first = 1\n", "     first = 1\n")
        (finding,) = self.assert_one_changed(result, INDENTED_LINE)
        self.assertIn("OLD '    first = 1\\n' NEW '     first = 1\\n'", finding)

    def test_a_changed_line_inside_an_indented_block_is_reported(self) -> None:
        result = self.edited("    second = 2\n", "    second = 3\n")
        (finding,) = self.assert_one_changed(result, INDENTED_LINE)
        self.assertIn("block 3", finding)
        self.assertIn("OLD '    second = 2\\n' NEW '    second = 3\\n'", finding)

    def test_a_changed_mermaid_diagram_is_reported(self) -> None:
        result = self.edited("A --> B", "A -> B")
        self.assert_one_changed(result, MERMAID_LINE)

    def test_crlf_converted_to_lf_inside_a_block_is_reported(self) -> None:
        old = "```sh\r\nmake\r\n```\r\n"
        result = self.compare(old, old.replace("\r\n", "\n"))
        self.assertEqual(result.returncode, EXIT_DIFFERENCES, result.stdout + result.stderr)
        self.assertIn("OLD '```sh\\r\\n' NEW '```sh\\n'", result.stdout)

    def test_a_nul_character_inside_a_block_is_preserved_for_comparison(self) -> None:
        old = "```text\nfoo\x00bar\n```\n"
        result = self.compare(old, old.replace("\x00", "\ufffd"))
        self.assertEqual(result.returncode, EXIT_DIFFERENCES, result.stdout + result.stderr)
        self.assertIn("OLD 'foo\\x00bar\\n' NEW 'foo\\ufffdbar\\n'", result.stdout)

    def test_a_line_separator_character_does_not_shift_later_line_numbers(self) -> None:
        old = "Prose\u2028with a separator.\n\n```sh\nmake\n```\n"
        # The change sits on the fence line, which a block cut one line late would miss.
        result = self.compare(old, old.replace("```sh", "```bash"))
        self.assertEqual(result.returncode, EXIT_DIFFERENCES)
        self.assertIn("OLD block 1 (line 3), NEW block 1 (line 3)", result.stdout)
        self.assertIn("block line 1 differs: OLD '```sh\\n' NEW '```bash\\n'", result.stdout)

    def test_a_block_inside_a_list_is_compared_with_its_indent(self) -> None:
        old = "- step\n\n  ```sh\n  make \\\n    all\n  ```\n"
        result = self.compare(old, old.replace("make \\\n", "make\n"))
        self.assertEqual(result.returncode, EXIT_DIFFERENCES)
        self.assertIn("OLD '  make \\\\\\n' NEW '  make\\n'", result.stdout)


class AlignsAfterInsertionsAndDeletions(CodeblocksTestCase):
    def test_a_deleted_middle_block_reports_one_missing_block_and_nothing_else(self) -> None:
        deleted = DOCUMENT.replace('```py\narrow = "→"\n```\n\n', "")
        result = self.compare(DOCUMENT, deleted)
        self.assertEqual(result.returncode, EXIT_DIFFERENCES, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"OLD block 2 (line {PY_LINE}): missing from NEW\n")
        self.assertIn("4 block(s) in OLD, 3 in NEW, 0 changed, 1 missing, 0 added", result.stderr)

    def test_an_added_block_reports_one_added_block_and_nothing_else(self) -> None:
        added = DOCUMENT.replace("Then set the arrow:", "Then run it:\n\n```sh\n./run\n```\n\nThen set the arrow:")
        result = self.compare(DOCUMENT, added)
        self.assertEqual(result.returncode, EXIT_DIFFERENCES, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"NEW block 2 (line {PY_LINE}): added, absent from OLD\n")
        self.assertIn("4 block(s) in OLD, 5 in NEW, 0 changed, 0 missing, 1 added", result.stderr)

    def test_a_change_beside_a_deletion_is_still_reported_as_a_change(self) -> None:
        old = "```a\none\n```\n\n```b\ntwo\n```\n\n```c\nthree\n```\n"
        new = "```a\none\n```\n\n```c\nthree!\n```\n"
        result = self.compare(old, new)
        self.assertEqual(result.returncode, EXIT_DIFFERENCES)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "OLD block 2 (line 5), NEW block 2 (line 5): block line 1 differs: OLD '```b\\n' NEW '```c\\n'",
                "OLD block 3 (line 9): missing from NEW",
            ],
        )

    def test_a_deleted_first_block_is_reported_at_its_line(self) -> None:
        deleted = DOCUMENT.replace("```sh\nmake build \\\n  --target all\n```\n\n", "")
        result = self.compare(DOCUMENT, deleted)
        self.assertEqual(result.stdout, f"OLD block 1 (line {SH_LINE}): missing from NEW\n")

    def test_an_unclosed_fence_at_the_end_of_the_file_is_compared(self) -> None:
        old = "```sh\nmake\n"
        self.assertEqual(self.compare(old, old).returncode, EXIT_CLEAN)
        result = self.compare(old, "```sh\nmake all\n")
        self.assertEqual(result.returncode, EXIT_DIFFERENCES)
        self.assertIn("OLD 'make\\n' NEW 'make all\\n'", result.stdout)

    def test_findings_are_deterministic(self) -> None:
        first = self.compare(DOCUMENT, DOCUMENT.replace("```py", "```python").replace("```sh", "```bash"))
        second = self.compare(DOCUMENT, DOCUMENT.replace("```py", "```python").replace("```sh", "```bash"))
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(len(first.stdout.splitlines()), 2)


class HandlesErrors(CodeblocksTestCase):
    def test_a_missing_file_exits_two(self) -> None:
        new_path = self.directory / "new.md"
        _ = new_path.write_text(DOCUMENT, encoding="utf-8")
        result = self.run_check(str(self.directory / "absent.md"), str(new_path))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("codeblocks.py: error: cannot read "), result.stderr)

    def test_an_undecodable_file_exits_two_without_a_traceback(self) -> None:
        result = self.compare(DOCUMENT, b"```sh\nmake \xff\n```\n")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("codeblocks.py: error: cannot read "), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_one_argument_exits_two_with_a_hint(self) -> None:
        result = self.run_check("only-one.md")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("codeblocks.py: error: invalid arguments:", result.stderr)
        self.assertIn("hint:", result.stderr)

    def test_three_arguments_exit_two(self) -> None:
        self.assertEqual(self.run_check("a.md", "b.md", "c.md").returncode, EXIT_USAGE)

    def test_no_arguments_exit_two(self) -> None:
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
        self.assertTrue(result.stderr.startswith("codeblocks.py: error: cannot import"), result.stderr)
        self.assertIn("uv run", result.stderr)


if __name__ == "__main__":
    unittest.main()
