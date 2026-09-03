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
SCRIPT_ROOT = SKILLS_ROOT / "shared" / "agent-stack" / "skill-forge" / "scripts"
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
            self.assertIn(
                "lowercase letters, digits, and single hyphens", result.stderr
            )

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
                    "MISE_CACHE_DIR": str(SKILLS_ROOT / ".cache" / "mise" / "cache"),
                    "MISE_STATE_DIR": str(SKILLS_ROOT / ".cache" / "mise" / "state"),
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


if __name__ == "__main__":
    unittest.main()
