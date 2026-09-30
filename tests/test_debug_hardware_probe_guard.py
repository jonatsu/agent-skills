"""Behavioral tests for debug-hardware's bundled probe guard hook."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest

from skill_locator import skill_directory

GUARD_SCRIPT = skill_directory("debug-hardware") / "scripts" / "probe_guard.py"

EXIT_ALLOW = 0
EXIT_DENY = 2

DESTRUCTIVE = (
    'openocd -f interface/cmsis-dap.cfg -f target/nrf52.cfg -c "init; nrf5 mass_erase; exit"',
    'openocd -f target/stm32f1x.cfg -c "init; reset halt; stm32f1x unlock 0; exit"',
    'openocd -f target/stm32l4x.cfg -c "stm32l4x option_write 0 0x20 0xAA"',
    'openocd -f target/stm32f1x.cfg -c "flash protect 0 0 last on"',
    'openocd -c "flash erase_sector 0 0 last"',
    "pyocd erase --chip -t nrf52840",
    "pyocd load -e chip app.hex",
    "pyocd load --erase=chip app.hex",
    "pyocd gdbserver -O auto_unlock=true",
    "uvx pyocd erase --mass",
    "python3 -m pyocd erase --chip",
    "probe-rs erase --chip RP2040",
    "probe-rs download --chip STM32F411RE --chip-erase app.elf",
    "cargo embed --allow-erase-all",
    "JLinkExe -device nRF52840_xxAA -if SWD -CommandFile unlock.jlink",
    'arm-none-eabi-gdb -batch -ex "target extended-remote :3333" -ex "monitor flash erase_sector 0 0 1" app.elf',
    'gdb-multiarch -ex "mon erase" app.elf',
    "nrfjprog --recover",
    "nrfjprog --program app.hex --chiperase",
    "nrfutil device recover",
    "esptool.py --chip esp32 erase_flash",
    "espefuse.py burn_efuse JTAG_DISABLE",
    "idf.py -p /dev/ttyUSB0 erase-flash",
    "STM32_Programmer_CLI -c port=SWD -ob RDP=0xBB",
    "st-flash erase",
    "sudo -E openocd -c 'nrf5 mass_erase'",
    "cd build && pyocd erase --chip",
    "bash -c 'probe-rs erase --chip RP2040'",
    "FOO=1 timeout 30 nrfjprog --eraseall",
)

ALLOWED = (
    'openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "program app.elf verify reset exit"',
    'openocd -c "init; flash write_image erase app.elf; reset run; exit"',
    'openocd -f target/stm32f4x.cfg -c "adapter speed 4000; init; reset halt"',
    "pyocd load app.hex -t nrf52840",
    "pyocd gdbserver -O auto_unlock=false",
    "probe-rs run --chip RP2040 target/app",
    "cargo flash --chip nRF52840_xxAA --release",
    "JLinkExe -device nRF52840_xxAA -if SWD",
    'gdb-multiarch -ex "target extended-remote :3333" -ex "monitor reset halt" -ex load app.elf',
    "nrfjprog --program app.hex --sectorerase --verify",
    "esptool.py --chip esp32 write_flash 0x1000 app.bin",
    "espefuse.py summary",
    "rg -n erase_flash docs/",
    "git commit -m 'document nrf5 mass_erase'",
    "echo pyocd erase",
)


def _run(payload: object, harness: str = "claude") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GUARD_SCRIPT), "--harness", harness],
        input=payload if isinstance(payload, str) else json.dumps(payload),
        check=False,
        capture_output=True,
        text=True,
    )


def _claude(command: str) -> dict[str, object]:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }


class ProbeGuardRuleTests(unittest.TestCase):
    """Each destructive form asks; each ordinary probe or unrelated command stays silent."""

    def test_destructive_commands_ask(self) -> None:
        for command in DESTRUCTIVE:
            with self.subTest(command=command):
                result = _run(_claude(command))
                self.assertEqual(result.returncode, EXIT_ALLOW, result.stderr)
                decision = json.loads(result.stdout)["hookSpecificOutput"]
                self.assertEqual(decision["permissionDecision"], "ask")
                self.assertIn("permission", decision["permissionDecisionReason"])

    def test_ordinary_commands_pass_silently(self) -> None:
        for command in ALLOWED:
            with self.subTest(command=command):
                result = _run(_claude(command))
                self.assertEqual(result.returncode, EXIT_ALLOW, result.stderr)
                self.assertEqual(result.stdout, "")


class ProbeGuardHarnessTests(unittest.TestCase):
    """Each harness gets its own answer shape, and payloads it cannot read pass."""

    def test_copilot_asks_in_flat_form_with_string_tool_args(self) -> None:
        payload = {"toolName": "bash", "toolArgs": json.dumps({"command": "pyocd erase --chip"})}
        result = _run(payload, "copilot")
        self.assertEqual(result.returncode, EXIT_ALLOW)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "ask")

    def test_copilot_accepts_object_tool_args(self) -> None:
        payload = {"toolName": "bash", "toolArgs": {"command": "nrfjprog --recover"}}
        self.assertEqual(json.loads(_run(payload, "copilot").stdout)["permissionDecision"], "ask")

    def test_codex_denies_with_exit_2_and_a_reason_on_stderr(self) -> None:
        payload = {"tool_name": "Bash", "tool_input": {"command": "probe-rs erase --chip RP2040"}}
        result = _run(payload, "codex")
        self.assertEqual(result.returncode, EXIT_DENY)
        self.assertEqual(result.stdout, "")
        self.assertIn("Codex hooks cannot ask", result.stderr)

    def test_other_tools_pass(self) -> None:
        payload = {"tool_name": "Write", "tool_input": {"command": "pyocd erase --chip"}}
        self.assertEqual(_run(payload).stdout, "")

    def test_unreadable_payload_passes(self) -> None:
        for payload in ("not json", "[]", json.dumps({"toolName": "bash", "toolArgs": "{broken"})):
            with self.subTest(payload=payload):
                result = _run(payload, "copilot")
                self.assertEqual(result.returncode, EXIT_ALLOW)
                self.assertEqual(result.stdout, "")

    def test_unbalanced_quotes_still_find_the_command(self) -> None:
        result = _run(_claude("pyocd erase --chip; echo 'oops"))
        self.assertEqual(
            json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "ask"
        )


if __name__ == "__main__":
    unittest.main()
