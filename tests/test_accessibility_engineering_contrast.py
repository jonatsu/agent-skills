"""Behavioral tests for the accessibility-engineering skill's contrast.py, run as the command agents call."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skill_locator import skill_directory

SCRIPT = skill_directory("accessibility-engineering") / "scripts" / "contrast.py"

EXIT_OK = 0
EXIT_USAGE = 2


def run(*arguments: str, script: Path = SCRIPT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(script), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def report(*arguments: str) -> dict[str, object]:
    result = run("--json", *arguments)
    assert result.returncode == EXIT_OK, result.stderr
    loaded: dict[str, object] = json.loads(result.stdout)
    return loaded


def worst_ratio(*arguments: str) -> float:
    worst = report(*arguments)["worst"]
    assert isinstance(worst, dict)
    return float(worst["ratio"])


def passes(*arguments: str) -> dict[str, bool]:
    verdicts = report(*arguments)["verdicts"]
    assert isinstance(verdicts, list)
    return {str(verdict["use"]): bool(verdict["passes"]) for verdict in verdicts}


class ComputesWcagRatios(unittest.TestCase):
    def test_black_on_white_is_the_maximum(self) -> None:
        self.assertAlmostEqual(worst_ratio("000", "fff"), 21.0, places=6)

    def test_order_of_colours_does_not_change_the_ratio(self) -> None:
        self.assertAlmostEqual(
            worst_ratio("#777777", "#ffffff"), worst_ratio("#ffffff", "#777777"), places=9
        )

    def test_grey_777_on_white_fails_normal_text_and_passes_large(self) -> None:
        self.assertAlmostEqual(worst_ratio("777777", "ffffff"), 4.478, places=3)
        verdicts = passes("777777", "ffffff")
        self.assertFalse(verdicts["normal text"])
        self.assertTrue(verdicts["large text"])
        self.assertTrue(verdicts["controls and graphics"])

    def test_grey_767676_on_white_is_the_lightest_grey_that_passes(self) -> None:
        self.assertTrue(passes("767676", "ffffff")["normal text"])
        self.assertFalse(passes("777777", "ffffff")["normal text"])

    def test_three_digit_and_six_digit_forms_agree(self) -> None:
        self.assertAlmostEqual(
            worst_ratio("#777", "#fff"), worst_ratio("#777777", "#ffffff"), places=9
        )


class NeverRoundsAcrossAThreshold(unittest.TestCase):
    def test_a_failing_ratio_just_under_four_point_five_prints_below_it(self) -> None:
        result = report("777777", "070707")
        worst = result["worst"]
        assert isinstance(worst, dict)
        self.assertLess(float(worst["ratio"]), 4.5)
        self.assertEqual(worst["ratio_display"], "4.49")
        self.assertFalse(passes("777777", "070707")["normal text"])


class JudgesTheWorstBackground(unittest.TestCase):
    def test_verdicts_follow_the_lowest_ratio_among_backgrounds(self) -> None:
        result = report("ffffff", "000000", "888888")
        worst = result["worst"]
        assert isinstance(worst, dict)
        self.assertEqual(worst["background"], "#888888")
        self.assertFalse(passes("ffffff", "000000", "888888")["normal text"])

    def test_text_output_names_the_worst_background(self) -> None:
        result = run("ffffff", "000000", "888888")
        self.assertEqual(result.returncode, EXIT_OK)
        self.assertIn("worst: 3.54:1 on #888888", result.stdout)
        self.assertIn("FAIL  normal text", result.stdout)


class CompositesTranslucentForegrounds(unittest.TestCase):
    def test_half_transparent_black_on_white_is_painted_mid_grey(self) -> None:
        worst = report("00000080", "ffffff")["worst"]
        assert isinstance(worst, dict)
        self.assertEqual(worst["painted_foreground"], "#7F7F7F")
        self.assertAlmostEqual(float(worst["ratio"]), 4.0, places=2)

    def test_opaque_alpha_matches_the_plain_colour(self) -> None:
        self.assertAlmostEqual(
            worst_ratio("777777ff", "ffffff"), worst_ratio("777777", "ffffff"), places=9
        )


class RejectsWhatItCannotMeasure(unittest.TestCase):
    def test_unreadable_colour_exits_with_usage_status_and_names_it(self) -> None:
        result = run("#zzz", "fff")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("'#zzz'", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_translucent_background_is_refused(self) -> None:
        result = run("000", "ffffff80")
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("translucent", result.stderr)

    def test_missing_background_is_a_usage_error(self) -> None:
        self.assertEqual(run("000").returncode, EXIT_USAGE)


class RunsStandalone(unittest.TestCase):
    def test_a_copy_outside_the_repository_runs_with_nothing_beside_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "contrast.py"
            shutil.copyfile(SCRIPT, copy)
            result = run("000", "fff", script=copy)
        self.assertEqual(result.returncode, EXIT_OK, result.stderr)
        self.assertIn("21.00:1", result.stdout)


if __name__ == "__main__":
    unittest.main()
