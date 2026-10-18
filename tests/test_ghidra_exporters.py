"""Exercise exporter orchestration with a fake Ghidra host and real output files.

These tests do not validate Ghidra's engine, Java bindings, or recovered C semantics.
"""

from __future__ import annotations

import io
import runpy
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

from skill_locator import skill_directory

EXPORTER = skill_directory("ghidra-firmware-analysis") / "scripts" / "decompile_all.py"


class CancelledError(Exception):
    """Stand in for the host's cancellation exception."""


def _function(name: str, address: str) -> Mock:
    function = Mock()
    function.getName.return_value = name
    function.getEntryPoint.return_value = address
    return function


def _completed_result(code: str) -> Mock:
    result = Mock()
    result.decompileCompleted.return_value = True
    result.getDecompiledFunction.return_value.getC.return_value = code
    return result


class GhidraPythonExporterTests(unittest.TestCase):
    """Pin file preservation, diagnostics, cancellation, and engine ownership."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name) / "export.c"
        self.program = Mock()
        self.program.getName.return_value = "sample.bin"
        self.functions = [_function("first", "001000"), _function("last", "001020")]
        self.program.getFunctionManager.return_value.getFunctions.return_value = self.functions
        self.monitor = Mock()
        self.decompiler = Mock()
        self.decompiler.openProgram.return_value = True
        self.decompiler.decompileFunction.side_effect = [
            _completed_result("void first(void) {}"),
            _completed_result("void last(void) {}"),
        ]
        self.factory = Mock(return_value=self.decompiler)
        self.stdout = io.StringIO()

    def run_exporter(self, arguments: list[str] | None = None) -> None:
        """Supply only the script host boundary; execute the actual exporter."""
        modules = {
            name: ModuleType(name) for name in ("ghidra", "ghidra.app", "ghidra.app.decompiler")
        }
        modules["ghidra.app.decompiler"].DecompInterface = self.factory
        host = {
            "getScriptArgs": lambda: [str(self.output)] if arguments is None else arguments,
            "getCurrentProgram": lambda: self.program,
            "monitor": self.monitor,
        }
        with patch.dict(sys.modules, modules), redirect_stdout(self.stdout):
            runpy.run_path(str(EXPORTER), init_globals=host)

    def test_exports_each_function_and_disposes_engine(self) -> None:
        self.run_exporter()

        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "// decompiled from sample.bin\n\nvoid first(void) {}\nvoid last(void) {}\n",
        )
        self.assertIn("(2 functions attempted, 0 failed)", self.stdout.getvalue())
        self.decompiler.dispose.assert_called_once_with()

    def test_passes_timeout_and_script_monitor_for_every_function(self) -> None:
        self.run_exporter()

        self.assertEqual(self.decompiler.decompileFunction.call_count, 2)
        self.decompiler.decompileFunction.assert_any_call(self.functions[0], 60, self.monitor)
        self.decompiler.decompileFunction.assert_any_call(self.functions[1], 60, self.monitor)
        self.decompiler.openProgram.assert_called_once_with(self.program)

    def test_requires_exactly_one_output_argument_before_creating_engine(self) -> None:
        for arguments in ([], ["one.c", "two.c"]):
            with self.subTest(arguments=arguments), self.assertRaisesRegex(ValueError, "Usage"):
                self.run_exporter(arguments)
        self.factory.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_requires_a_loaded_program_before_creating_engine(self) -> None:
        self.program = None

        with self.assertRaisesRegex(ValueError, "loaded Ghidra program"):
            self.run_exporter()

        self.factory.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_refuses_to_overwrite_existing_evidence(self) -> None:
        self.output.write_text("preserved evidence", encoding="utf-8")

        with self.assertRaises(FileExistsError):
            self.run_exporter()

        self.assertEqual(self.output.read_text(encoding="utf-8"), "preserved evidence")
        self.decompiler.decompileFunction.assert_not_called()
        self.decompiler.dispose.assert_called_once_with()
        self.assertEqual(self.stdout.getvalue(), "")

    def test_refuses_symlink_to_existing_evidence(self) -> None:
        original = self.output.with_name("original.c")
        original.write_text("preserved evidence", encoding="utf-8")
        self.output.symlink_to(original)

        with self.assertRaises(FileExistsError):
            self.run_exporter()

        self.assertTrue(self.output.is_symlink())
        self.assertEqual(original.read_text(encoding="utf-8"), "preserved evidence")
        self.decompiler.dispose.assert_called_once_with()

    def test_records_failed_and_null_results_and_continues_export(self) -> None:
        failed = Mock()
        failed.decompileCompleted.return_value = False
        failed.getErrorMessage.return_value = "bad\nstate\rretry"
        self.functions.append(_function("third", "001040"))
        self.decompiler.decompileFunction.side_effect = [
            failed,
            None,
            _completed_result("void third(void) {}"),
        ]

        self.run_exporter()

        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "// decompiled from sample.bin\n\n"
            "// FAILED: first @ 001000: bad state retry\n\n"
            "// FAILED: last @ 001020: No result\n\n"
            "void third(void) {}\n",
        )
        self.assertIn("(3 functions attempted, 2 failed)", self.stdout.getvalue())
        self.decompiler.dispose.assert_called_once_with()

    def test_open_failure_reports_host_reason_and_disposes_without_output(self) -> None:
        self.decompiler.openProgram.return_value = False
        self.decompiler.getLastMessage.return_value = "unsupported language"

        with self.assertRaisesRegex(RuntimeError, "unsupported language"):
            self.run_exporter()

        self.assertFalse(self.output.exists())
        self.decompiler.decompileFunction.assert_not_called()
        self.decompiler.dispose.assert_called_once_with()

    def test_cancellation_before_first_function_never_calls_engine(self) -> None:
        self.monitor.checkCancelled.side_effect = CancelledError("cancelled")

        with self.assertRaises(CancelledError):
            self.run_exporter()

        self.decompiler.decompileFunction.assert_not_called()
        self.decompiler.dispose.assert_called_once_with()
        self.assertEqual(self.stdout.getvalue(), "")

    def test_cancellation_during_last_call_keeps_only_prior_output(self) -> None:
        self.monitor.checkCancelled.side_effect = [None, None, None, CancelledError("cancelled")]

        with self.assertRaises(CancelledError):
            self.run_exporter()

        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "// decompiled from sample.bin\n\nvoid first(void) {}\n",
        )
        self.decompiler.dispose.assert_called_once_with()
        self.assertEqual(self.stdout.getvalue(), "")

    def test_engine_exception_keeps_partial_evidence_and_disposes(self) -> None:
        self.decompiler.decompileFunction.side_effect = [
            _completed_result("void first(void) {}"),
            RuntimeError("engine disconnected"),
        ]

        with self.assertRaisesRegex(RuntimeError, "engine disconnected"):
            self.run_exporter()

        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "// decompiled from sample.bin\n\nvoid first(void) {}\n",
        )
        self.decompiler.dispose.assert_called_once_with()
        self.assertEqual(self.stdout.getvalue(), "")

    def test_output_open_failure_disposes_engine(self) -> None:
        self.output = self.output.parent / "missing-directory" / "export.c"

        with self.assertRaises(FileNotFoundError):
            self.run_exporter()

        self.decompiler.dispose.assert_called_once_with()
        self.decompiler.decompileFunction.assert_not_called()


if __name__ == "__main__":
    unittest.main()
