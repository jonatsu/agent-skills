"""Behavioral tests for Skill Forge's bundled command-line scripts."""

from __future__ import annotations

import os
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
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SCRIPT_ROOT = SKILLS_ROOT / "shared" / "agent-skills" / "skill-forge" / "scripts"
INIT_SCRIPT = SCRIPT_ROOT / "init_skill.py"
VALIDATE_SCRIPT = SCRIPT_ROOT / "quick_validate.py"


def _run_python(
    script: Path, *arguments: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


class InitSkillTests(unittest.TestCase):
    def test_help_exits_successfully(self) -> None:
        result = _run_python(INIT_SCRIPT, "--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_valid_request_creates_minimal_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = _run_python(
                INIT_SCRIPT,
                "sample-skill",
                "--path",
                temporary_directory,
                "--author",
                "Test Author",
                "--license",
                "MIT",
            )

            skill_md = Path(temporary_directory) / "sample-skill" / "SKILL.md"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(skill_md.is_file())
            self.assertIn("name: sample-skill", skill_md.read_text())

    def test_invalid_name_reports_the_constraint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = _run_python(
                INIT_SCRIPT,
                "Invalid_Name",
                "--path",
                temporary_directory,
                "--author",
                "Test Author",
                "--license",
                "MIT",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("lowercase letters, digits, and single hyphens", result.stderr)

    def test_missing_author_reports_configuration_failure(self) -> None:
        environment = os.environ.copy()
        environment["GIT_CONFIG_GLOBAL"] = os.devnull
        environment["GIT_CONFIG_SYSTEM"] = os.devnull
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = _run_python(
                INIT_SCRIPT,
                "sample-skill",
                "--path",
                temporary_directory,
                "--license",
                "MIT",
                env=environment,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Pass --author or set git config user.name", result.stderr)


class QuickValidateTests(unittest.TestCase):
    def test_help_exits_successfully(self) -> None:
        result = _run_python(VALIDATE_SCRIPT, "--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_mise_managed_uv_run_resolves_declared_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            skill_directory.mkdir()
            (skill_directory / "SKILL.md").write_text(
                "---\n"
                "name: sample-skill\n"
                "description: Use for a sample task.\n"
                "license: MIT\n"
                "metadata:\n"
                "  author: Test Author\n"
                "---\n"
            )

            result = subprocess.run(
                [
                    "mise",
                    "exec",
                    "-C",
                    str(SKILLS_ROOT),
                    "--",
                    "uv",
                    "run",
                    "--script",
                    str(VALIDATE_SCRIPT),
                    str(skill_directory),
                ],
                check=False,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    # Keep mise's state out of the repository: its trusted-configs
                    # entries are symlinks to config roots, including the repository
                    # itself, and a link cycle inside the tree hangs tools that follow
                    # symlinks while walking it, such as markdownlint-cli2.
                    "MISE_CACHE_DIR": str(Path(temporary_directory) / "mise" / "cache"),
                    "MISE_STATE_DIR": str(Path(temporary_directory) / "mise" / "state"),
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Skill Forge local policy is valid", result.stdout)

    def test_missing_skill_returns_policy_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = _run_python(VALIDATE_SCRIPT, temporary_directory)

            self.assertEqual(result.returncode, 1)
            self.assertIn("SKILL.md not found", result.stdout)

    def test_malformed_frontmatter_returns_policy_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory)
            (skill_directory / "SKILL.md").write_text("---\nname: [\n---\n")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot inspect local policy", result.stdout)

    def test_idea_source_attribution_does_not_require_upstream_license(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory)
            (skill_directory / "SKILL.md").write_text(
                "---\n"
                "name: sample-skill\n"
                "description: Use for a sample task.\n"
                "license: MIT\n"
                "metadata:\n"
                "  author: Test Author\n"
                "---\n"
            )
            (skill_directory / "ATTRIBUTIONS.md").write_text(
                "# Attributions\n\n"
                "An external source influenced one independently expressed idea.\n"
            )

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("Skill Forge local policy is valid", result.stdout)

    def test_missing_argument_returns_usage_failure(self) -> None:
        result = _run_python(VALIDATE_SCRIPT)

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr.lower())

    def test_absent_dependency_names_itself_and_the_runner(self) -> None:
        """Without a PEP 723-aware runner the script must say so, not traceback.

        `-S` drops site-packages, which is where the declared dependency lives,
        so this reproduces the plain-interpreter case without uninstalling
        anything. Exit 2 rather than 1, because a gate must not record a broken
        invocation as a policy failure.
        """
        result = subprocess.run(
            [sys.executable, "-S", str(VALIDATE_SCRIPT), str(SCRIPT_ROOT.parent)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("PyYAML is required", result.stderr)
        self.assertIn("uv run", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


def _write_skill(skill_directory: Path, body: str) -> None:
    """Write a policy-clean SKILL.md whose only variable part is its body."""
    skill_directory.mkdir(parents=True, exist_ok=True)
    (skill_directory / "SKILL.md").write_text(
        "---\n"
        "name: sample-skill\n"
        "description: Use for a sample task.\n"
        "license: MIT\n"
        "metadata:\n"
        "  author: Test Author\n"
        "---\n"
        f"\n# Sample Skill\n\n{body}\n",
        encoding="utf-8",
    )
    (skill_directory / "ATTRIBUTIONS.md").write_text(
        "# Attributions\n\nIndependently written.\n", encoding="utf-8"
    )


class BundledReferenceTests(unittest.TestCase):
    """A deployed skill is copied alone, so every path it names must ship with it."""

    def test_missing_markdown_link_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "Read [the guide](references/guide.md).")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 1)
            self.assertIn("references/guide.md", result.stdout)
            self.assertIn("no such file ships with the skill", result.stdout)

    def test_missing_bare_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "Run scripts/verify.sh before delivery.")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 1)
            self.assertIn("scripts/verify.sh", result.stdout)

    def test_existing_reference_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "Read [the guide](references/guide.md).")
            (skill_directory / "references").mkdir()
            (skill_directory / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 0, result.stdout)

    def test_anchor_resolves_to_the_file_it_points_into(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "Read [part two](references/guide.md#two).")
            (skill_directory / "references").mkdir()
            (skill_directory / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 0, result.stdout)

    def test_fenced_example_path_is_not_a_promise(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "```bash\ncat references/example-output.md\n```")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 0, result.stdout)

    def test_reference_outside_the_skill_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(skill_directory, "Read [shared](../shared/references/x.md).")
            sibling = Path(temporary_directory) / "shared" / "references"
            sibling.mkdir(parents=True)
            (sibling / "x.md").write_text("# X\n", encoding="utf-8")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 1)
            self.assertIn("leaves the skill directory", result.stdout)

    def test_external_url_is_not_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            _write_skill(
                skill_directory,
                "See the [specification](https://agentskills.io/specification) "
                "and the [heading](#sample-skill).",
            )

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 0, result.stdout)

    def test_unreadable_skill_md_reports_a_policy_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_directory = Path(temporary_directory) / "sample-skill"
            skill_directory.mkdir()
            (skill_directory / "SKILL.md").write_bytes(b"---\nname: \xff\n---\n")

            result = _run_python(VALIDATE_SCRIPT, str(skill_directory))

            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot read SKILL.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
