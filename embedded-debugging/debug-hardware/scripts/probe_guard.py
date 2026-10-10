#!/usr/bin/env python3
"""Pre-tool-use hook that stops destructive debug-probe commands until the user approves them.

A project installs this in its own repository and registers it for shell-tool calls. It reads the hook payload
on stdin, finds every command on the shell line, and flags erase, unlock, recover, protection, option-byte, and
fuse operations for the common probe and flashing tools. Plain flashing passes, because agreeing to the task
authorizes it. Uses only the Python standard library.

    probe_guard.py --harness claude     answer "ask" in Claude Code's hookSpecificOutput form
    probe_guard.py --harness copilot    answer "ask" in Copilot CLI's flat form
    probe_guard.py --harness codex      deny with exit 2 and a reason, since Codex hooks cannot ask

The check reads command text, so it is best effort: an operation hidden in a script, a recipe, an OpenOCD `.cfg`
file, or a J-Link command file's contents passes unseen. An unreadable payload passes silently rather than
blocking every shell call in the project.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from collections.abc import Callable, Iterator, Sequence
from pathlib import PurePath

EXIT_ALLOW = 0
EXIT_DENY = 2
SHELL_TOOL_NAMES = frozenset({"bash", "shell", "exec_command"})
SEPARATORS = frozenset({";", "&", "&&", "|", "||", "|&", "(", ")", "\n"})
SHELLS = frozenset({"bash", "sh", "zsh", "dash"})
# Wrappers that run the following word as the command, after their own dash options.
PREFIX_WRAPPERS = frozenset({"sudo", "env", "exec", "nohup", "time", "command", "uvx", "pipx"})
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

OPENOCD_DESTRUCTIVE = re.compile(
    r"\w*erase\w*|\b(?:\w+_)?(?:un)?lock\b|\w*protect\w*|\boption_(?:write|load)\b|\w*recover\w*",
    re.IGNORECASE,
)
# `flash write_image erase` erases only the sectors it rewrites: ordinary flashing.
OPENOCD_FLASHING_ERASE = re.compile(r"\bwrite_image\s+erase\b", re.IGNORECASE)
GDB_MONITOR_DESTRUCTIVE = re.compile(
    r"\bmon(?:itor)?\b.*(?:erase|\b(?:un)?lock\b|recover|option_write)", re.IGNORECASE
)
ESPTOOL_ERASE = frozenset({"erase_flash", "erase-flash", "erase_region", "erase-region"})
ESPEFUSE_WRITES = re.compile(r"^(?:burn|write[_-]protect|read[_-]protect)", re.IGNORECASE)

REASON = (
    "{tool}: {operation} can erase or permanently lock the target, so it needs the user's permission for this "
    "operation. State the command and what it changes, and wait for the user's approval."
)
CODEX_SUFFIX = " Codex hooks cannot ask, so give the user the exact command to run themselves."

Finding = tuple[str, str]
Rule = Callable[[str, list[str]], str | None]


def parse_commands(line: str, depth: int = 0) -> Iterator[list[str]]:
    """Yield each simple command on a shell line as its words, following `sh -c` strings one level deep."""
    for words in _split_segments(line):
        words = _strip_prefix(words)
        if not words:
            continue
        yield words
        if depth == 0 and PurePath(words[0]).name in SHELLS and "-c" in words[1:]:
            script_index = words.index("-c") + 1
            if script_index < len(words):
                yield from parse_commands(words[script_index], depth + 1)


def _split_segments(line: str) -> Iterator[list[str]]:
    try:
        lexer = shlex.shlex(line, posix=True, punctuation_chars=";&|()\n")
        lexer.whitespace_split = True
        lexer.whitespace = " \t\r"
        tokens = list(lexer)
    except ValueError:
        # Unbalanced quotes: split on every separator character, which sees more commands, never fewer.
        for piece in re.split(r"[;&|()\n]", line):
            yield piece.split()
        return
    segment: list[str] = []
    for token in tokens:
        if token in SEPARATORS or set(token) <= set(";&|()\n"):
            yield segment
            segment = []
        else:
            segment.append(token.strip("`"))
    yield segment


def _strip_prefix(words: list[str]) -> list[str]:
    """Drop variable assignments and wrapper commands so the real command word comes first."""
    index = 0
    while index < len(words):
        word = words[index]
        name = PurePath(word).name
        if ASSIGNMENT.match(word):
            index += 1
        elif name in PREFIX_WRAPPERS:
            index += 1
            if name == "pipx" and words[index : index + 1] == ["run"]:
                index += 1
            while index < len(words) and words[index].startswith("-"):
                index += 1
        elif (
            name == "timeout"
            or name == "uv"
            and words[index + 1 : index + 2] == ["run"]
            or re.fullmatch(r"python[0-9.]*", name)
            and words[index + 1 : index + 2] == ["-m"]
        ):
            index += 2
        else:
            break
    return words[index:]


def _any_arg(args: Sequence[str], *names: str) -> str | None:
    lowered = {name.lower() for name in names}
    for arg in args:
        flag = arg.split("=", 1)[0].lower()
        if flag in lowered:
            return arg
    return None


def check_openocd(word: str, args: list[str]) -> str | None:
    if word != "openocd":
        return None
    for arg in args:
        match = OPENOCD_DESTRUCTIVE.search(OPENOCD_FLASHING_ERASE.sub("", arg))
        if match:
            return f"the command `{match.group(0)}`"
    return None


def check_pyocd(word: str, args: list[str]) -> str | None:
    if word != "pyocd":
        return None
    if args[:1] == ["erase"]:
        return "`pyocd erase`"
    for index, arg in enumerate(args):
        if arg.lower() in {"--erase=chip", "-echip"} or (
            arg in {"-e", "--erase"} and args[index + 1 : index + 2] == ["chip"]
        ):
            return "a chip erase"
        if re.search(r"auto_unlock\s*=\s*(?:true|1|yes|on)", arg, re.IGNORECASE):
            return "auto_unlock, which mass-erases a locked part on connect"
    return None


def check_probe_rs(word: str, args: list[str]) -> str | None:
    is_cargo_plugin = word in {"cargo-embed", "cargo-flash"} or (
        word == "cargo" and args[:1] in (["embed"], ["flash"])
    )
    if word != "probe-rs" and not is_cargo_plugin:
        return None
    if word == "probe-rs" and args[:1] == ["erase"]:
        return "`probe-rs erase`"
    flag = _any_arg(args, "--allow-erase-all", "--chip-erase")
    return f"`{flag}`" if flag else None


def check_jlink(word: str, args: list[str]) -> str | None:
    if word.lower() not in {"jlinkexe", "jlink.exe", "jlink"}:
        return None
    if _any_arg(args, "-commandfile"):
        return "a J-Link command file, whose contents the guard cannot inspect"
    return None


def check_gdb(word: str, args: list[str]) -> str | None:
    if not (word == "gdb" or word.endswith("-gdb") or word.startswith("gdb-")):
        return None
    for arg in args:
        match = GDB_MONITOR_DESTRUCTIVE.search(arg)
        if match:
            return f"`{arg}`"
    return None


def check_nordic(word: str, args: list[str]) -> str | None:
    if word == "nrfjprog":
        flag = _any_arg(
            args,
            "--eraseall",
            "--erasepage",
            "--eraseuicr",
            "--qspieraseall",
            "--recover",
            "--chiperase",
        )
        return f"`{flag}`" if flag else None
    if word == "nrfutil" and args[:1] == ["device"]:
        if args[1:2] in (["erase"], ["recover"]):
            return f"`nrfutil device {args[1]}`"
        if any("ERASE_ALL" in arg.upper() for arg in args):
            return "an erase-all program option"
    return None


def check_espressif(word: str, args: list[str]) -> str | None:
    name = word.removesuffix(".py")
    if name == "esptool":
        erase = next((arg for arg in args if arg in ESPTOOL_ERASE), None)
        if erase:
            return f"`{erase}`"
        flag = _any_arg(args, "--erase-all", "-e")
        return f"`write_flash {flag}`" if flag else None
    if name == "espefuse":
        write = next((arg for arg in args if ESPEFUSE_WRITES.match(arg)), None)
        return f"the eFuse write `{write}`, which is permanent" if write else None
    if word == "idf.py":
        action = next(
            (arg for arg in args if arg in ESPTOOL_ERASE or arg.startswith("efuse-burn")), None
        )
        return f"`idf.py {action}`" if action else None
    return None


def check_stm32(word: str, args: list[str]) -> str | None:
    if word.lower() in {"stm32_programmer_cli", "stm32_programmer_cli.exe"}:
        flag = _any_arg(args, "-e", "--erase", "-ob", "--optionbytes")
        return f"`{flag}`" if flag else None
    if word == "st-flash" and args[:1] == ["erase"]:
        return "`st-flash erase`"
    return None


RULES: tuple[Rule, ...] = (
    check_openocd,
    check_pyocd,
    check_probe_rs,
    check_jlink,
    check_gdb,
    check_nordic,
    check_espressif,
    check_stm32,
)


def find_destructive(line: str) -> Finding | None:
    """Return the tool and operation of the first destructive probe command on `line`, or None."""
    for words in parse_commands(line):
        word = PurePath(words[0]).name
        for rule in RULES:
            operation = rule(word, words[1:])
            if operation:
                return word, operation
    return None


def shell_command(payload: object, harness: str) -> str | None:
    """Return the shell command string from a harness's pre-tool-use payload, or None for another tool."""
    if not isinstance(payload, dict):
        return None
    if harness == "copilot":
        tool_name, tool_input = payload.get("toolName"), payload.get("toolArgs")
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                return None
    else:
        tool_name, tool_input = payload.get("tool_name"), payload.get("tool_input")
    if not isinstance(tool_name, str) or tool_name.lower() not in SHELL_TOOL_NAMES:
        return None
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if isinstance(command, list):
        command = shlex.join(str(part) for part in command)
    return command if isinstance(command, str) else None


def respond(harness: str, reason: str) -> int:
    """Write the harness's ask or deny answer and return the exit status."""
    if harness == "codex":
        print(reason + CODEX_SUFFIX, file=sys.stderr)
        return EXIT_DENY
    if harness == "claude":
        answer: dict[str, object] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        }
    else:
        answer = {"permissionDecision": "ask", "permissionDecisionReason": reason}
    print(json.dumps(answer))
    return EXIT_ALLOW


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ask before destructive debug-probe shell commands."
    )
    parser.add_argument("--harness", required=True, choices=("claude", "codex", "copilot"))
    harness = parser.parse_args(argv).harness
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return EXIT_ALLOW
    command = shell_command(payload, harness)
    finding = find_destructive(command) if command else None
    if finding is None:
        return EXIT_ALLOW
    tool, operation = finding
    return respond(harness, REASON.format(tool=tool, operation=operation))


if __name__ == "__main__":
    sys.exit(main())
