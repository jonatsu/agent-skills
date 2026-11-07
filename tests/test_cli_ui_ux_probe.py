"""Behavioral tests for the cli-ui-ux skill's probe_cli.py against synthetic command-line tools."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Any

from skill_locator import skill_directory

SCRIPT = skill_directory("cli-ui-ux") / "scripts" / "probe_cli.py"

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_ENVIRONMENT = 3

# A tool that keeps data on stdout, errors on stderr, and colour to terminals.
WELL_BEHAVED = """\
import os, sys
args = sys.argv[1:]
colour = sys.stdout.isatty() and not os.environ.get("NO_COLOR") and os.environ.get("TERM") != "dumb"
if args in (["--help"], ["-h"], ["help"], []):
    print("usage: good [--help] [--version] list")
    sys.exit(0)
if args == ["--version"]:
    print("good 1.0")
    sys.exit(0)
if args == ["list"]:
    print("\\033[32mitem\\033[0m" if colour else "item")
    sys.exit(0)
print(f"good: error: unknown argument '{args[0]}'", file=sys.stderr)
sys.exit(2)
"""

# A tool that colours unconditionally, reports errors on stdout with exit 0, and deletes data when run bare.
BADLY_BEHAVED = """\
import os, shutil, sys
args = sys.argv[1:]
if not args:
    shutil.rmtree("cache", ignore_errors=True)
    print("ok")
    sys.exit(0)
if args[0] == "secret":
    print(os.environ.get("PROBE_TEST_SECRET", "absent"))
    sys.exit(0)
if args[0] == "ask":
    input("Continue? [y/N] ")
    sys.exit(0)
print("\\033[31merror\\033[0m")
sys.exit(0)
"""


class ProbeCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        (self.root / "good.py").write_text(textwrap.dedent(WELL_BEHAVED), encoding="utf-8")
        (self.root / "bad.py").write_text(textwrap.dedent(BADLY_BEHAVED), encoding="utf-8")
        (self.root / "cache").mkdir()
        (self.root / "cache" / "obj.bin").write_bytes(b"data")

    def probe(
        self, *arguments: str, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
            env={**os.environ, **(env or {})},
        )

    def report(self, *arguments: str, env: dict[str, str] | None = None) -> dict[str, Any]:
        result = self.probe(*arguments, env=env)
        self.assertEqual(result.returncode, EXIT_OK, result.stderr)
        return json.loads(result.stdout)

    @staticmethod
    def find(report: dict[str, Any], args: list[str], mode: str) -> dict[str, Any]:
        return next(p for p in report["probes"] if p["args"] == args and p["mode"] == mode)

    def test_well_behaved_tool_separates_streams_and_colours_only_terminals(self) -> None:
        report = self.report(
            "--workdir",
            str(self.root),
            "--probe",
            "list",
            "--modes",
            "pipe,tty,tty-no-color,tty-dumb",
            "--",
            sys.executable,
            "good.py",
        )
        unknown = self.find(report, ["--probe-cli-unknown-flag"], "pipe")
        self.assertEqual(unknown["exit_code"], 2)
        self.assertEqual(unknown["stdout"]["text"], "")
        self.assertIn("unknown argument", unknown["stderr"]["text"])
        self.assertFalse(self.find(report, ["list"], "pipe")["stdout"]["ansi"])
        self.assertTrue(self.find(report, ["list"], "tty")["output"]["ansi"])
        self.assertFalse(self.find(report, ["list"], "tty-no-color")["output"]["ansi"])
        self.assertFalse(self.find(report, ["list"], "tty-dumb")["output"]["ansi"])

    def test_bad_tool_shows_colour_when_piped_and_errors_on_stdout(self) -> None:
        report = self.report(
            "--workdir", str(self.root), "--modes", "pipe", "--", sys.executable, "bad.py"
        )
        unknown = self.find(report, ["--probe-cli-unknown-flag"], "pipe")
        self.assertEqual(unknown["exit_code"], 0)
        self.assertTrue(unknown["stdout"]["ansi"])
        self.assertEqual(unknown["stderr"]["text"], "")

    def test_destructive_bare_run_is_recorded_and_confined_to_the_copy(self) -> None:
        report = self.report(
            "--workdir", str(self.root), "--modes", "pipe", "--", sys.executable, "bad.py"
        )
        bare = self.find(report, [], "pipe")
        self.assertEqual(bare["workdir_changes"]["deleted"], ["cache/obj.bin"])
        self.assertTrue((self.root / "cache" / "obj.bin").exists())

    def test_skip_bare_leaves_out_the_probe_without_arguments(self) -> None:
        report = self.report(
            "--workdir",
            str(self.root),
            "--modes",
            "pipe",
            "--skip-bare",
            "--",
            sys.executable,
            "bad.py",
        )
        self.assertNotIn([], [p["args"] for p in report["probes"]])

    def test_environment_is_built_from_scratch(self) -> None:
        report = self.report(
            "--workdir",
            str(self.root),
            "--no-default-probes",
            "--probe",
            "secret",
            "--modes",
            "pipe",
            "--",
            sys.executable,
            "bad.py",
            env={"PROBE_TEST_SECRET": "hunter2"},
        )
        self.assertEqual(report["probes"][0]["stdout"]["text"].strip(), "absent")

    def test_prompt_under_a_terminal_times_out_and_fails_fast_when_piped(self) -> None:
        report = self.report(
            "--workdir",
            str(self.root),
            "--no-default-probes",
            "--probe",
            "ask",
            "--timeout",
            "2",
            "--",
            sys.executable,
            "bad.py",
        )
        self.assertTrue(self.find(report, ["ask"], "tty")["timed_out"])
        piped = self.find(report, ["ask"], "pipe")
        self.assertFalse(piped["timed_out"])
        self.assertIn("EOFError", piped["stderr"]["text"])

    def test_missing_command_is_an_environment_error(self) -> None:
        result = self.probe("--", "probe-cli-test-no-such-command")
        self.assertEqual(result.returncode, EXIT_ENVIRONMENT)
        self.assertIn("command not found", result.stderr)

    def test_invalid_mode_is_a_usage_error(self) -> None:
        result = self.probe("--modes", "colourful", "--", sys.executable, "-c", "pass")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("unknown mode", result.stderr)

    def test_missing_command_argument_is_a_usage_error(self) -> None:
        result = self.probe("--modes", "pipe")
        self.assertEqual(result.returncode, EXIT_USAGE)

    def test_probe_values_may_start_with_a_dash(self) -> None:
        report = self.report(
            "--no-default-probes",
            "--probe",
            "-h",
            "--probe",
            "--version",
            "--modes",
            "pipe",
            "--",
            sys.executable,
            str(self.root / "good.py"),
        )
        self.assertEqual([p["args"] for p in report["probes"]], [["-h"], ["--version"]])
        self.assertEqual([p["exit_code"] for p in report["probes"]], [0, 0])

    def test_home_from_seeds_each_temporary_home(self) -> None:
        seed = self.root / "seed"
        (seed / ".local" / "lib").mkdir(parents=True)
        (seed / ".local" / "lib" / "plugin.txt").write_text("loaded", encoding="utf-8")
        script = "import os; print(open(os.path.expanduser('~/.local/lib/plugin.txt')).read())"
        report = self.report(
            "--home-from",
            str(seed),
            "--no-default-probes",
            "--probe",
            f"-c {shlex.quote(script)}",
            "--modes",
            "pipe",
            "--",
            sys.executable,
        )
        self.assertEqual(report["probes"][0]["stdout"]["text"].strip(), "loaded")
        self.assertTrue((seed / ".local" / "lib" / "plugin.txt").exists())

    def test_runtime_directory_is_sandboxed(self) -> None:
        report = self.report(
            "--no-default-probes",
            "--probe",
            "XDG_RUNTIME_DIR",
            "--modes",
            "pipe",
            "--",
            "printenv",
            env={"XDG_RUNTIME_DIR": "/run/user/0"},
        )
        runtime = report["probes"][0]["stdout"]["text"].strip()
        self.assertTrue(runtime.endswith("/run"), runtime)
        self.assertNotEqual(runtime, "/run/user/0")

    def test_home_from_must_be_a_directory(self) -> None:
        result = self.probe(
            "--home-from", str(self.root / "missing"), "--", sys.executable, "-c", "pass"
        )
        self.assertEqual(result.returncode, EXIT_ENVIRONMENT)


if __name__ == "__main__":
    unittest.main()
