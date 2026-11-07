"""Behavioral tests for Context Architecture's bundled checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

CHECK_SCRIPT = skill_directory("context-architecture") / "scripts" / "check_context_architecture.py"

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

    def test_trigger_and_link_may_wrap_within_the_same_list_item(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- Read when changing the child:\n  [Child](child.md) has the details.\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertEqual(result.stdout.strip(), "clean")

    def test_wrapped_routes_accept_conditions_hard_breaks_and_reference_links(self) -> None:
        routes = (
            "- Read when changing the\n  child: [Child](child.md).",
            "- Read before changing the child:\\\n  [Child](child.md).",
            "- If you change the child:\n    [Child][route].\n\n[route]: child.md",
            "  - Symptom the child fails:\\\n    [Child][route].\n\n[route]: child.md",
        )
        _write(self.root, "docs/child.md", "# Child\n")
        for route in routes:
            with self.subTest(route=route):
                _write(self.root, "docs/index.md", f"# Index\n\n{route}\n")
                result = _run(self.root)
                self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_wrapped_route_stops_at_markdown_block_boundaries(self) -> None:
        boundaries = (
            "- See [Child](child.md).",
            "  - See [Child](child.md).",
            "  1. See [Child](child.md).",
            "  # See [Child](child.md)",
            "  | See [Child](child.md) |",
            "  ```md\n  [Child](child.md)\n  ```",
            "  ~~~md\n  [Child](child.md)\n  ~~~",
            "See [Child](child.md).",
            "\n  See [Child](child.md).",
        )
        _write(self.root, "docs/child.md", "# Child\n")
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                _write(
                    self.root,
                    "docs/index.md",
                    f"# Index\n\n- Read when changing the child:\n{boundary}\n",
                )
                result = _run(self.root)
                self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
                self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_wrapped_route_keeps_its_first_line_for_trigger_diagnostics(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- Read before:\\\n  [Child](child.md).\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn(
            "docs/index.md: line 3: routing list item has an empty trigger", result.stdout
        )
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_wrapping_does_not_promote_an_incidental_list_link(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- Read when changing the child, see\n  [Child](child.md) for background.\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")

        result = _run(self.root)

        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_explicit_sha256_pin_preserves_immutable_source_line_coordinates(self) -> None:
        digest = "ab" * 32
        for label in ("SHA-256", "sha256"):
            with self.subTest(label=label):
                _write(
                    self.root,
                    "docs/index.md",
                    f"# Index\n\nSources are pinned to {label} `{digest}`.\n\nSee `driver.c:42`.\n",
                )
                result = _run(self.root)
                self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_source_pin_can_wrap_but_must_be_in_the_document_head(self) -> None:
        digest = "cd" * 32
        _write(
            self.root,
            "docs/index.md",
            f"# Index\n\nSources are pinned to SHA-256:\\\n`{digest}`.\n\nSee `driver.c:42`.\n",
        )
        result = _run(self.root)
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

        _write(
            self.root,
            "docs/index.md",
            "# Index\n"
            + "\n" * 14
            + f"Sources are pinned to SHA-256 `{digest}`.\nSee `driver.c:42`.\n",
        )
        result = _run(self.root)
        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
        self.assertIn("line-number reference", result.stdout)

    def test_invalid_or_example_digests_do_not_exempt_line_references(self) -> None:
        digest = "ef" * 32
        declarations = (
            f"    Sources are pinned to SHA-256 `{digest}`.",
            f"SHA-256 `{digest}`.",
            f"Sources are pinned to `{digest}`.",
            f"Sources are pinned to SHA-256 `{digest[:-1]}`.",
            f"Sources are pinned to SHA-256 `{digest}0`.",
            f"Sources are pinned to SHA-256 `{'z' * 64}`.",
            f"```md\nSources are pinned to SHA-256 `{digest}`.\n```",
            f"``Sources are pinned to SHA-256 `{digest}`.``",
        )
        for declaration in declarations:
            with self.subTest(declaration=declaration):
                _write(
                    self.root, "docs/index.md", f"# Index\n\n{declaration}\n\nSee `driver.c:42`.\n"
                )
                result = _run(self.root)
                self.assertEqual(result.returncode, EXIT_FINDINGS, result.stdout)
                self.assertIn("line-number reference", result.stdout)

    def test_existing_commit_pin_still_exempts_source_line_coordinates(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\nSources are pinned to commit `abcdef1234`.\n\nSee `driver.c:42`.\n",
        )
        result = _run(self.root)
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

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

    def test_reference_links_route_in_tables_lists_and_standalone_inclusions(self) -> None:
        routes = (
            "| Read when | Read |\n| --- | --- |\n| Updating child | [Child][route] |",
            "- Read when updating child: [Child][route]",
            "[route][]",
            "[route]",
        )
        for route in routes:
            with self.subTest(route=route):
                _write(
                    self.root, "docs/index.md", f"# Index\n\n{route}\n\n[route]: child.md#details\n"
                )
                _write(self.root, "docs/child.md", "# Child\n")
                result = _run(self.root)
                self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_reference_labels_ignore_case_and_normalize_whitespace(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n- Read when updating child: [Child][ROUTE   name]\n\n[route name]: child.md\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")
        result = _run(self.root)
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_unused_or_undefined_reference_does_not_route(self) -> None:
        for content in (
            "[route]: child.md",
            "[missing]\n\n[route]: child.md",
            "[route][missing]\n\n[route]: child.md",
        ):
            with self.subTest(content=content):
                _write(self.root, "docs/index.md", f"# Index\n\n{content}\n")
                _write(self.root, "docs/child.md", "# Child\n")
                result = _run(self.root)
                self.assertIn("docs/child.md: unreachable", result.stdout)

    def test_incidental_reference_link_does_not_route(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\nSee [Child][route] for background.\n\n[route]: child.md\n",
        )
        _write(self.root, "docs/child.md", "# Child\n")
        self.assertIn("docs/child.md: unreachable", _run(self.root).stdout)

    def test_code_examples_cannot_define_or_follow_reference_routes(self) -> None:
        examples = (
            "```md\n[route]\n[route]: child.md\n```",
            "[route]\n\n~~~md\n[route]: child.md\n~~~",
            "- Read when updating child: `[Child][route]`\n\n[route]: child.md",
        )
        for example in examples:
            with self.subTest(example=example):
                _write(self.root, "docs/index.md", f"# Index\n\n{example}\n")
                _write(self.root, "docs/child.md", "# Child\n")
                self.assertIn("docs/child.md: unreachable", _run(self.root).stdout)

    def test_reference_links_still_require_table_trigger_headers(self) -> None:
        _write(
            self.root,
            "docs/index.md",
            "# Index\n\n| File | Description |\n| --- | --- |\n| [One][one] | First |\n| [Two][two] | Second |\n\n[one]: one.md\n[two]: two.md\n",
        )
        _write(self.root, "docs/one.md", "# One\n")
        _write(self.root, "docs/two.md", "# Two\n")
        self.assertIn("no recognized trigger column", _run(self.root).stdout)

    def test_nested_git_boundaries_exclude_candidates_and_routing_roots(self) -> None:
        for marker_kind in ("file", "directory"):
            with self.subTest(marker_kind=marker_kind):
                foreign = self.root / "docs" / marker_kind
                foreign.mkdir(parents=True)
                marker = foreign / ".git"
                if marker_kind == "file":
                    marker.write_text("gitdir: somewhere\n", encoding="utf-8")
                else:
                    marker.mkdir()
                _write(self.root, f"docs/{marker_kind}/AGENTS.md", "[Escape](../child.md)\n")
                _write(self.root, f"docs/{marker_kind}/foreign.md", "# Foreign\n")
        _write(self.root, "docs/index.md", "# Index\n")
        _write(self.root, "docs/child.md", "# Child\n")
        result = _run(self.root)
        self.assertIn("docs/child.md: unreachable", result.stdout)
        self.assertNotIn("foreign.md", result.stdout)

    def test_structural_route_cannot_enter_a_nested_worktree(self) -> None:
        _write(self.root, "docs/foreign/.git", "gitdir: somewhere\n")
        _write(self.root, "docs/foreign/index.md", "[Child](../child.md)\n")
        _write(self.root, "docs/index.md", "[Foreign](foreign/index.md)\n")
        _write(self.root, "docs/child.md", "# Child\n")
        self.assertIn("docs/child.md: unreachable", _run(self.root).stdout)

    def test_selected_root_may_itself_be_a_git_worktree(self) -> None:
        _write(self.root, ".git", "gitdir: somewhere\n")
        _write(self.root, "docs/index.md", "# Index\n")
        self.assertEqual(_run(self.root).returncode, EXIT_OK)

    def test_unreadable_unrelated_directory_does_not_crash_the_scan(self) -> None:
        _write(self.root, "docs/index.md", "# Index\n")
        blocked = self.root / "unreadable"
        blocked.mkdir()
        self.addCleanup(blocked.chmod, 0o700)
        blocked.chmod(0)
        result = _run(self.root)
        self.assertEqual(result.returncode, EXIT_OK, result.stderr)


if __name__ == "__main__":
    unittest.main()
