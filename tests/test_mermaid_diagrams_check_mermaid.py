"""Behavioral tests for the mermaid-diagrams skill's check_mermaid.py, run as the command agents call."""

from __future__ import annotations

import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("mermaid-diagrams") / "scripts" / "check_mermaid.py"

EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_USAGE = 2

# Stands in for mermaidx: a diagram containing BROKEN fails the way mermaidx reports a parse error on line 2.
FAKE_MERMAIDX = f"""#!{sys.executable}
import sys
source = sys.stdin.read()
if "BROKEN" in source:
    sys.stderr.write(
        "Traceback (most recent call last):\\n"
        "RuntimeError: Mermaid rendering failed: Error: Parse error on line 2:\\n"
        "...A --> BROKEN\\n"
        "---------^\\n"
        "Expecting 'NODE_STRING', got 'EOF'\\n"
    )
    sys.exit(1)
sys.stdout.write("<svg/>")
"""

MARKDOWN = """# Title

```mermaid
flowchart LR
  A --> B
```

Some prose.

~~~~mermaid
flowchart LR
  A --> BROKEN
~~~~

```python
print("not a diagram")
```
"""


class CheckMermaidTestCase(unittest.TestCase):
    directory: Path
    fake: Path

    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory)
        self.fake = self.directory / "fake-mermaidx"
        _ = self.fake.write_text(FAKE_MERMAIDX, encoding="utf-8")
        self.fake.chmod(self.fake.stat().st_mode | stat.S_IXUSR)

    def write(self, name: str, text: str) -> Path:
        path = self.directory / name
        _ = path.write_text(text, encoding="utf-8")
        return path

    def run_check(
        self, *arguments: str, mermaidx: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        renderer = ["--mermaidx", mermaidx if mermaidx is not None else str(self.fake)]
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), *renderer, *arguments],
            capture_output=True,
            text=True,
            check=False,
        )


class ReportsEachFailingBlock(CheckMermaidTestCase):
    def test_a_broken_block_is_reported_at_its_file_line(self) -> None:
        path = self.write("doc.md", MARKDOWN)
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)
        # The broken fence opens on line 10; Mermaid's line 2 of the block is file line 12.
        self.assertEqual(
            result.stdout,
            f"{path}:12: Parse error on line 2: Expecting 'NODE_STRING', got 'EOF'\n",
        )
        self.assertIn("2 diagram(s) checked, 1 failed", result.stderr)

    def test_clean_markdown_exits_zero_with_empty_stdout(self) -> None:
        path = self.write("ok.md", MARKDOWN.replace("BROKEN", "C"))
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_a_mmd_file_is_one_diagram(self) -> None:
        path = self.write("flow.mmd", "flowchart LR\n  A --> BROKEN\n")
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertTrue(result.stdout.startswith(f"{path}:2: "))

    def test_a_file_without_diagrams_is_clean(self) -> None:
        path = self.write("plain.md", "# Nothing here\n")
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertIn("0 diagram(s) checked", result.stderr)


class RejectsBadInvocations(CheckMermaidTestCase):
    def test_missing_renderer_exits_two_and_names_the_install(self) -> None:
        path = self.write("doc.md", MARKDOWN)
        result = self.run_check(str(path), mermaidx="no-such-mermaidx")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertTrue(result.stderr.startswith("check_mermaid: error: mermaidx not found"))
        self.assertIn("pipx install mermaidx", result.stderr)

    def test_missing_file_exits_two(self) -> None:
        result = self.run_check(str(self.directory / "absent.md"))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("cannot read", result.stderr)

    def test_no_files_is_a_usage_error(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, EXIT_USAGE)


class RunsStandalone(CheckMermaidTestCase):
    def test_a_copy_outside_the_repository_works(self) -> None:
        copy = self.directory / "check_mermaid.py"
        _ = shutil.copy(SCRIPT, copy)
        path = self.write("doc.md", MARKDOWN)
        result = subprocess.run(
            [sys.executable, "-I", str(copy), "--mermaidx", str(self.fake), str(path)],
            capture_output=True,
            text=True,
            check=False,
            cwd=self.directory,
        )
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)


@unittest.skipUnless(shutil.which("mermaidx"), "mermaidx is not installed")
class RendersWithRealMermaidx(CheckMermaidTestCase):
    def test_real_parse_error_is_located(self) -> None:
        path = self.write(
            "doc.md", "# T\n\n```mermaid\nflowchart LR\n  A --> \n  B -->> C[[\n```\n"
        )
        result = self.run_check(str(path), mermaidx="mermaidx")
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)
        self.assertTrue(result.stdout.startswith(f"{path}:6: Parse error on line 3"), result.stdout)

    def test_real_valid_diagram_renders(self) -> None:
        path = self.write("ok.md", "```mermaid\nsequenceDiagram\n  Alice->>Bob: hi\n```\n")
        result = self.run_check(str(path), mermaidx="mermaidx")
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)


if __name__ == "__main__":
    unittest.main()
