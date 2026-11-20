"""Behavioral tests for the mermaid-diagrams skill's check-mermaid.py, run as the command agents call."""

from __future__ import annotations

import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("mermaid-diagrams") / "scripts" / "check-mermaid.py"

EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_USAGE = 2

# Stands in for mermaidx. A diagram containing BROKEN fails the way mermaidx reports a parse error on line 2 of the
# diagram. A mindmap whose child lines lost their indentation fails the way mermaidx reports a flattened mindmap.
FAKE_MERMAIDX_BODY = r"""
import sys
source = sys.stdin.read()
if "BROKEN" in source:
    sys.stderr.write(
        "Traceback (most recent call last):\n"
        "RuntimeError: Mermaid rendering failed: Error: Parse error on line 2:\n"
        "...A --> BROKEN\n"
        "---------^\n"
        "Expecting 'NODE_STRING', got 'EOF'\n"
    )
    sys.exit(1)
if source.startswith("mindmap") and "\n    Child" not in source:
    sys.stderr.write("RuntimeError: Mermaid rendering failed: Error: There can be only one root.\n")
    sys.exit(1)
sys.stdout.write("<svg/>")
"""

BROKEN_WORD = "BROKEN"

# Line numbers matter here: the second fence opens on line 10, so its body starts on line 11.
BROKEN_MARKDOWN = f"""# Title

```mermaid
flowchart LR
  A --> B
```

Some prose.

~~~~mermaid
flowchart LR
  A --> {BROKEN_WORD}
~~~~

```python
print("not a diagram")
```
"""
CLEAN_MARKDOWN = BROKEN_MARKDOWN.replace(BROKEN_WORD, "C")

MINDMAP = "mindmap\n  root((Root))\n    Child A\n    Child B\n"


class CheckMermaidTestCase(unittest.TestCase):
    directory: Path
    fake: Path

    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory)
        self.fake = self.directory / "fake-mermaidx"
        _ = self.fake.write_text(f"#!{sys.executable}{FAKE_MERMAIDX_BODY}", encoding="utf-8")
        self.fake.chmod(self.fake.stat().st_mode | stat.S_IXUSR)

    def write(self, name: str, text: str) -> Path:
        path = self.directory / name
        _ = path.write_text(text, encoding="utf-8")
        return path

    def run_check(
        self,
        *arguments: str,
        mermaidx: str | None = None,
        script: Path = SCRIPT,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        renderer = ["--mermaidx", mermaidx if mermaidx is not None else str(self.fake)]
        return subprocess.run(
            [sys.executable, "-I", str(script), *renderer, *arguments],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        )


class ChecksDiagrams(CheckMermaidTestCase):
    def test_a_broken_block_is_reported_at_its_file_line(self) -> None:
        path = self.write("doc.md", BROKEN_MARKDOWN)
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)
        # The body starts on line 11, so Mermaid's line 2 of the diagram is file line 12.
        self.assertEqual(
            result.stdout,
            f"{path}:12: Parse error on line 2: Expecting 'NODE_STRING', got 'EOF'\n",
        )
        self.assertIn("2 diagram(s) checked, 1 failed", result.stderr)

    def test_clean_markdown_exits_zero_with_empty_stdout(self) -> None:
        path = self.write("ok.md", CLEAN_MARKDOWN)
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_a_mmd_file_is_one_diagram(self) -> None:
        path = self.write("flow.mmd", f"flowchart LR\n  A --> {BROKEN_WORD}\n")
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertTrue(result.stdout.startswith(f"{path}:2: "), result.stdout)

    def test_a_file_without_diagrams_is_clean(self) -> None:
        path = self.write("plain.md", "# Nothing here\n")
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_CLEAN)
        self.assertIn("0 diagram(s) checked", result.stderr)


class KeepsDiagramIndentation(CheckMermaidTestCase):
    def test_an_unindented_fence_keeps_the_diagram_indentation(self) -> None:
        path = self.write("mind.md", f"```mermaid\n{MINDMAP}```\n")
        result = self.run_check(str(path))
        self.assertEqual((result.returncode, result.stdout), (EXIT_CLEAN, ""), result.stderr)

    def test_an_indented_fence_removes_only_its_own_indentation(self) -> None:
        indented = "".join(f"  {line}\n" for line in MINDMAP.splitlines())
        path = self.write("list.md", f"- A list item:\n\n  ```mermaid\n{indented}  ```\n")
        result = self.run_check(str(path))
        self.assertEqual((result.returncode, result.stdout), (EXIT_CLEAN, ""), result.stderr)

    def test_an_unclosed_fence_runs_to_the_end_of_the_file(self) -> None:
        path = self.write("open.md", f"# T\n\n```mermaid\nflowchart LR\n  A --> {BROKEN_WORD}\n")
        result = self.run_check(str(path))
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertTrue(result.stdout.startswith(f"{path}:5: "), result.stdout)


class RejectsBadInvocations(CheckMermaidTestCase):
    def test_missing_renderer_exits_two_and_names_the_install(self) -> None:
        path = self.write("doc.md", BROKEN_MARKDOWN)
        result = self.run_check(str(path), mermaidx="no-such-mermaidx")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertTrue(result.stderr.startswith("check-mermaid: error: mermaidx not found"))
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
        copy = self.directory / "check-mermaid.py"
        _ = shutil.copy(SCRIPT, copy)
        path = self.write("doc.md", BROKEN_MARKDOWN)
        result = self.run_check(str(path), script=copy, cwd=self.directory)
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)


@unittest.skipUnless(shutil.which("mermaidx"), "mermaidx is not installed")
class RendersWithRealMermaidx(CheckMermaidTestCase):
    def test_real_parse_error_is_located(self) -> None:
        lines = [
            "# T",  # 1
            "",  # 2
            "```mermaid",  # 3
            "flowchart LR",  # 4: diagram line 1
            "  A -->",  # 5: diagram line 2
            "  B -->> C[[",  # 6: diagram line 3, where Mermaid fails
            "```",
        ]
        path = self.write("doc.md", "\n".join(lines) + "\n")
        result = self.run_check(str(path), mermaidx="mermaidx")
        self.assertEqual(result.returncode, EXIT_FAILED, result.stderr)
        self.assertTrue(result.stdout.startswith(f"{path}:6: Parse error on line 3"), result.stdout)

    def test_real_valid_diagram_renders(self) -> None:
        path = self.write("ok.md", "```mermaid\nsequenceDiagram\n  Alice->>Bob: hi\n```\n")
        result = self.run_check(str(path), mermaidx="mermaidx")
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stderr)

    def test_real_mindmap_in_markdown_renders(self) -> None:
        path = self.write("mind.md", f"```mermaid\n{MINDMAP}```\n")
        result = self.run_check(str(path), mermaidx="mermaidx")
        self.assertEqual((result.returncode, result.stdout), (EXIT_CLEAN, ""), result.stderr)


if __name__ == "__main__":
    unittest.main()
