"""Behavioral tests for the Agents Context Docs skill's bundled command-line script."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

CHECK_SCRIPT = skill_directory("agents-context-docs") / "scripts" / "check_agent_context.py"

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK_SCRIPT), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class CheckAgentContextTests(unittest.TestCase):
    """Cover the script's findings, its exclusions, and its exit statuses."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def _clean_tree(self) -> None:
        """A minimal repository that should report nothing."""
        _write(
            self.root,
            "AGENTS.md",
            "# Root\n\nA rule.\n\n| Symptom | Read |\n"
            "| --- | --- |\n| It broke | `docs/findings/thing.md` |\n",
        )
        _write(self.root, "docs/findings/thing.md", "# Thing\n\nEvidence.\n")

    def test_clean_tree_reports_nothing(self) -> None:
        self._clean_tree()
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("1 instruction file(s) checked, 0 finding(s)", result.stdout)

    def test_dangling_evidence_link_fails(self) -> None:
        self._clean_tree()
        (self.root / "docs/findings/thing.md").unlink()
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("dangling", result.stdout)

    def test_unindexed_evidence_file_is_orphaned(self) -> None:
        self._clean_tree()
        _write(self.root, "docs/findings/lonely.md", "# Lonely\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("orphaned", result.stdout)
        self.assertIn("lonely.md", result.stdout)

    def _indexed_tree(self, index_name: str = "README.md") -> None:
        """A floor that routes to an evidence index, which indexes the evidence."""
        _write(
            self.root,
            "AGENTS.md",
            f"# Root\n\nThe index is `docs/findings/{index_name}`.\n",
        )
        _write(
            self.root,
            f"docs/findings/{index_name}",
            "# Findings\n\n| Symptom | Read |\n| --- | --- |\n"
            "| It broke | [thing.md](thing.md) |\n",
        )
        _write(self.root, "docs/findings/thing.md", "# Thing\n\nEvidence.\n")

    def test_routed_index_reaches_the_evidence_it_lists(self) -> None:
        self._indexed_tree()
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertNotIn("orphaned", result.stdout)

    def test_index_md_is_honored_as_well_as_readme(self) -> None:
        self._indexed_tree(index_name="index.md")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_unrouted_index_grants_no_hop(self) -> None:
        """The hop is self-correcting: drop the floor's route and it closes."""
        self._indexed_tree()
        _write(self.root, "AGENTS.md", "# Root\n\nNo route to the index.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("orphaned", result.stdout)
        self.assertIn("thing.md", result.stdout)
        self.assertIn("README.md", result.stdout)

    def test_root_relative_reference_in_the_index_also_resolves(self) -> None:
        """An index may spell an entry the long way without breaking the hop."""
        self._indexed_tree()
        _write(
            self.root,
            "docs/findings/README.md",
            "# Findings\n\nSee `docs/findings/thing.md`.\n",
        )
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_hop_is_one_level_only(self) -> None:
        """An indexed finding citing a sibling does not thereby index it."""
        self._indexed_tree()
        _write(
            self.root,
            "docs/findings/thing.md",
            "# Thing\n\nSee also [sibling.md](sibling.md).\n",
        )
        _write(self.root, "docs/findings/sibling.md", "# Sibling\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("orphaned", result.stdout)
        self.assertIn("sibling.md", result.stdout)

    def test_dangling_link_inside_the_index_is_attributed_to_it(self) -> None:
        self._indexed_tree()
        (self.root / "docs/findings/thing.md").unlink()
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("dangling   docs/findings/README.md", result.stdout)

    def test_file_over_budget_warns_without_failing(self) -> None:
        _write(self.root, "AGENTS.md", "word " * 50)
        result = _run(str(self.root), "--budget", "10")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("oversize", result.stdout)
        self.assertIn("budget 10", result.stdout)

    def test_budget_override_applies_to_one_file(self) -> None:
        _write(self.root, "AGENTS.md", "word " * 50)
        _write(self.root, "sub/AGENTS.md", "word " * 50)
        result = _run(str(self.root), "--budget", "10", "--budget-for", "AGENTS.md=100")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("oversize   sub/AGENTS.md", result.stdout)
        self.assertNotIn("oversize   AGENTS.md", result.stdout)

    def test_nested_file_resolves_parent_relative_link(self) -> None:
        _write(self.root, "docs/findings/thing.md", "# Thing\n")
        _write(self.root, "sub/AGENTS.md", "See `../docs/findings/thing.md`.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertNotIn("dangling", result.stdout)

    def test_symlinked_claude_md_is_counted_once(self) -> None:
        _write(self.root, "AGENTS.md", "word " * 50)
        (self.root / "CLAUDE.md").symlink_to("AGENTS.md")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("1 instruction file(s) checked", result.stdout)

    def test_fixture_payload_is_excluded(self) -> None:
        _write(self.root, "tests/fixtures/repo/AGENTS.md", "word " * 500)
        result = _run(str(self.root), "--budget", "10")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("0 instruction file(s) checked", result.stdout)

    def test_top_level_payload_directory_is_excluded(self) -> None:
        """A `*/fixtures/*` pattern must also catch `fixtures/` at the root.

        It only does so because paths are matched as "/<relative>"; without the
        leading separator fnmatch requires a parent directory and a top-level
        payload slips through.
        """
        _write(self.root, "fixtures/AGENTS.md", "word " * 500)
        result = _run(str(self.root), "--budget", "10")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("0 instruction file(s) checked", result.stdout)

    def test_evaluations_payload_is_excluded(self) -> None:
        _write(self.root, "docs/evaluations/run-1/AGENTS.md", "word " * 500)
        result = _run(str(self.root), "--budget", "10")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_extra_exclude_is_honored(self) -> None:
        _write(self.root, "scratch/AGENTS.md", "word " * 500)
        result = _run(str(self.root), "--budget", "10", "--exclude", "*/scratch/*")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_dated_line_warns_without_failing(self) -> None:
        _write(self.root, "AGENTS.md", "Measured 2026-08-25 on a thing.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertIn("dated", result.stdout)
        self.assertIn("1 advisory warning(s) to review", result.stdout)
        self.assertIn("fine when it records a decision", result.stdout)

    def test_dated_hint_is_absent_without_dated_lines(self) -> None:
        _write(self.root, "AGENTS.md", "No dates here.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)
        self.assertNotIn("fine when it records a decision", result.stdout)

    def test_missing_evidence_directory_is_skipped(self) -> None:
        _write(self.root, "AGENTS.md", "No evidence here.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_link_escaping_the_root_is_reported(self) -> None:
        _write(self.root, "AGENTS.md", "See `../docs/findings/outside.md`.\n")
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        self.assertIn("escapes", result.stdout)

    def test_json_output_has_the_documented_shape(self) -> None:
        self._clean_tree()
        _write(self.root, "docs/findings/lonely.md", "# Lonely\n")
        result = _run(str(self.root), "--json")
        self.assertEqual(result.returncode, EXIT_FINDINGS)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["checked"], 1)
        self.assertEqual(payload["findings"][0]["kind"], "orphaned")
        self.assertIn("warnings", payload)

    def test_help_exits_zero(self) -> None:
        result = _run("--help")
        self.assertEqual(result.returncode, EXIT_OK)
        self.assertIn("--budget-for", result.stdout)

    def test_missing_root_exits_usage(self) -> None:
        result = _run(str(self.root / "absent"))
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("not a directory", result.stderr)

    def test_malformed_budget_override_exits_usage(self) -> None:
        result = _run(str(self.root), "--budget-for", "AGENTS.md")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("expected PATH=N", result.stderr)

    def test_non_integer_budget_override_exits_usage(self) -> None:
        result = _run(str(self.root), "--budget-for", "AGENTS.md=lots")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("must be an integer", result.stderr)

    def test_reference_links_route_through_an_evidence_index(self) -> None:
        for reference in ("[Thing][route]", "[route][]", "[route]", "[Thing][ROUTE   name]"):
            with self.subTest(reference=reference):
                _write(
                    self.root,
                    "AGENTS.md",
                    "[Evidence][index]\n\n[index]: docs/findings/README.md\n",
                )
                _write(
                    self.root,
                    "docs/findings/README.md",
                    f"# Evidence\n\n{reference}\n\n[route]: thing.md\n[route name]: thing.md\n",
                )
                _write(self.root, "docs/findings/thing.md", "# Thing\n")
                result = _run(str(self.root))
                self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_unused_reference_definition_does_not_grant_an_index_hop(self) -> None:
        _write(self.root, "AGENTS.md", "# Root\n\n[index]: docs/findings/README.md\n")
        _write(self.root, "docs/findings/README.md", "[Thing](thing.md)\n")
        _write(self.root, "docs/findings/thing.md", "# Thing\n")
        self.assertIn("orphaned", _run(str(self.root)).stdout)

    def test_index_reference_code_examples_do_not_reach_evidence(self) -> None:
        for content in (
            "```md\n[route]\n[route]: thing.md\n```",
            "`[route]`\n\n[route]: thing.md",
            "[missing]\n\n[route]: thing.md",
        ):
            with self.subTest(content=content):
                _write(self.root, "AGENTS.md", "See `docs/findings/README.md`.\n")
                _write(self.root, "docs/findings/README.md", content)
                _write(self.root, "docs/findings/thing.md", "# Thing\n")
                self.assertIn("orphaned", _run(str(self.root)).stdout)

    def test_nested_git_boundaries_exclude_instruction_files(self) -> None:
        _write(self.root, "AGENTS.md", "# Root\n")
        _write(self.root, "other/linked/.git", "gitdir: somewhere\n")
        _write(self.root, "other/linked/AGENTS.md", "See `docs/findings/missing.md`.\n")
        (self.root / "other" / "checkout" / ".git").mkdir(parents=True)
        _write(self.root, "other/checkout/AGENTS.md", "See `docs/findings/missing.md`.\n")
        result = _run(str(self.root), "--json")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["checked"], 1)
        self.assertEqual(payload["findings"], [])

    def test_evidence_directory_inside_nested_worktree_is_excluded(self) -> None:
        _write(self.root, "AGENTS.md", "# Root\n")
        _write(self.root, "docs/foreign/.git", "gitdir: somewhere\n")
        _write(self.root, "docs/foreign/findings/thing.md", "# Thing\n")
        result = _run(str(self.root), "--evidence-dir", "docs/foreign/findings")
        self.assertEqual(result.returncode, EXIT_OK, result.stdout)

    def test_selected_root_may_itself_be_a_git_worktree(self) -> None:
        _write(self.root, ".git", "gitdir: somewhere\n")
        self._clean_tree()
        self.assertEqual(_run(str(self.root)).returncode, EXIT_OK)

    def test_unreadable_unrelated_directory_does_not_crash_the_scan(self) -> None:
        self._clean_tree()
        blocked = self.root / "unreadable"
        blocked.mkdir()
        self.addCleanup(blocked.chmod, 0o700)
        blocked.chmod(0)
        result = _run(str(self.root))
        self.assertEqual(result.returncode, EXIT_OK, result.stderr)

    def test_index_links_with_fragments_reach_evidence(self) -> None:
        for link in ("[Thing](thing.md#details)", "[Thing][route]\n\n[route]: thing.md#details"):
            with self.subTest(link=link):
                _write(self.root, "AGENTS.md", "See `docs/findings/README.md`.\n")
                _write(self.root, "docs/findings/README.md", f"# Evidence\n\n{link}\n")
                _write(self.root, "docs/findings/thing.md", "# Thing\n\n## Details\n")
                result = _run(str(self.root))
                self.assertEqual(result.returncode, EXIT_OK, result.stdout)


if __name__ == "__main__":
    unittest.main()
