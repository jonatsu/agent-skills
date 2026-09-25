"""Behavioral tests for Context Architecture's bundled checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


REPOSITORY_ROOT = _repository_root()
CHECK_SCRIPT = (
    REPOSITORY_ROOT
    / "skills"
    / "shared"
    / "agent-stack"
    / "context-architecture"
    / "scripts"
    / "check_context_architecture.py"
)

EXIT_OK = 0
EXIT_FINDINGS = 1


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK_SCRIPT), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class CheckContextArchitectureTests(unittest.TestCase):
    """Cover the distinction between structural routes and ordinary references."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "| File | What it holds | Read when |\n"
            "| --- | --- | --- |\n"
            "| `docs/index.md` | Documentation routes | Working with project documentation |\n",
        )

    def test_inline_markdown_link_is_not_a_structural_route(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\nSee [Child](child.md) for background.\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_incidental_backticked_path_is_not_a_structural_route(self) -> None:
        _write(self.root, "docs/index.md", "# Index\n\nCompare behavior with `child.md`.\n")
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_standalone_inclusion_link_routes_through_an_intermediate_hub(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\nUse the child before changing the documentation structure.\n\n"
            "[Child](child.md)\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_read_when_table_routes_through_an_intermediate_hub(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n"
            "| File | What it holds | Read when |\n"
            "| --- | --- | --- |\n"
            "| `child.md` | Child guidance | Changing the child behavior |\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_read_when_table_file_cell_is_a_structural_route(self) -> None:
        _write(self.root, "docs/index.md", "# Index\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_symptom_table_read_cell_is_a_structural_route(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "| Symptom | Read |\n"
            "| --- | --- |\n"
            "| The build reports stale output | `docs/finding.md` |\n",
        )
        _write(self.root, "docs/finding.md", "# Finding\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_read_before_table_file_cell_is_a_structural_route(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "| Read before you touch | File | What it holds |\n"
            "| --- | --- | --- |\n"
            "| Service configuration | `docs/service.md` | Service rules |\n",
        )
        _write(self.root, "docs/service.md", "# Service\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_trigger_keyed_list_item_is_a_structural_route(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "- Read before changing service configuration: "
            "[Service instructions](docs/service.md) cover deployment boundaries.\n",
        )
        _write(self.root, "docs/service.md", "# Service\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_each_supported_list_trigger_is_a_structural_route(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "- Read when the build changes: [Build](docs/build.md).\n"
            "- Read before editing docs: [Docs](docs/documentation.md).\n"
            "- If you see configuration drift: [Drift](docs/drift.md).\n"
            "- Symptom error: generated output is stale: [Stale output](docs/stale.md).\n",
        )
        for name in ("build", "documentation", "drift", "stale"):
            _write(self.root, f"docs/{name}.md", f"# {name.title()}\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_trigger_keyed_list_item_requires_a_condition(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n- Read before: [Service instructions](docs/service.md).\n",
        )
        _write(self.root, "docs/service.md", "# Service\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("routing list item has an empty trigger condition", result.stdout)
        self.assertIn("docs/service.md: unreachable", result.stdout)

    def test_routing_table_row_requires_a_trigger_condition(self) -> None:
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\n"
            "| Read when | File |\n"
            "| --- | --- |\n"
            "| | [Service instructions](docs/service.md) |\n",
        )
        _write(self.root, "docs/service.md", "# Service\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("has an empty trigger cell", result.stdout)
        self.assertIn("docs/service.md: unreachable", result.stdout)

    def test_ordinary_list_link_is_not_a_structural_route(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- See [Child](child.md) for background.\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_trigger_and_link_must_share_the_first_physical_line(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- Read when changing the child:\n  [Child](child.md) has the details.\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_root_ledgers_are_exempt_without_exempting_other_root_files(self) -> None:
        _write(self.root, "BACKLOG.md", "# Backlog\n")
        _write(self.root, "NOTES.md", "# Notes\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertNotIn("BACKLOG.md: unreachable", result.stdout)
        self.assertIn("NOTES.md: unreachable", result.stdout)

    def test_route_table_with_unrecognized_target_header_reports_the_header(
        self,
    ) -> None:
        _write(self.root, "AGENTS.md", "# Root\n")
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n"
            "| Document | What it holds | Read when |\n"
            "| --- | --- | --- |\n"
            "| `child.md` | Child guidance | Changing the child behavior |\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn(
            "docs/index.md: line 3: routing table has trigger column 'Read when' "
            "but no recognized target column ('File' or 'Read')",
            result.stdout,
        )
        self.assertIn("docs/child.md: unreachable", result.stdout)


if __name__ == "__main__":
    unittest.main()
