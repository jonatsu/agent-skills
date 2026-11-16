#!/usr/bin/env python3
"""Run a command-line tool through a matrix of probes inside a throwaway sandbox and report JSON.

Usage:
    probe_cli.py [options] -- COMMAND [ARGS...]

COMMAND and ARGS form the invocation prefix, such as `./bin/mytool` or `python3 tool.py`. Each probe appends
its own arguments to that prefix and runs in a fresh sandbox: a copy of `--workdir` (or an empty directory) as
the working directory, a temporary HOME (seeded from `--home-from` when given), XDG directories including an
empty XDG_RUNTIME_DIR, TMPDIR, an environment built from scratch (only PATH, LANG, TERM, and what `--env` or
`--keep-env` add, so credential variables are never inherited), a timeout, and its own process group, which is
killed when the probe ends. The empty runtime directory keeps a tool from finding a real per-user socket, such
as a systemd user service's, under /run/user.

Each probe runs in each requested mode:
    pipe          stdin from /dev/null, stdout and stderr captured separately
    tty           stdin, stdout and stderr on one pseudo-terminal (output arrives combined)
    tty-no-color  tty with NO_COLOR=1
    tty-dumb      tty with TERM=dumb

A tty probe that times out was most likely waiting for input: that is the hang an agent harness with a
pseudo-terminal would see.

The sandbox confines relative paths, HOME, XDG locations, and the runtime directory only. A tool that writes to an absolute path, a
system file, a service, a device, or the network is not contained; classify the tool's commands before
probing it. `--isolate-network` runs every probe under `unshare --user --net` when that is available.

Exit status: 0 when every probe ran (whatever the tool itself returned), 2 for invalid usage, 3 when the
environment cannot provide what was asked (missing command, unshare unavailable, working directory too large).

Standard library only; Python 3.9 or later; pseudo-terminal modes need a POSIX system.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import select
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_ENVIRONMENT = 3

MODES = ("pipe", "tty", "tty-no-color", "tty-dumb")
DEFAULT_MODES = ("pipe", "tty")
DEFAULT_PROBES: tuple[tuple[str, ...], ...] = (
    (),
    ("--help",),
    ("-h",),
    ("help",),
    ("--version",),
    ("--probe-cli-unknown-flag",),
    ("probe-cli-unknown-command",),
)
ANSI = re.compile(rb"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
CAPTURE_LIMIT = 64 * 1024
HASH_LIMIT = 4 * 1024 * 1024
KILL_GRACE_SECONDS = 2.0


class ProbeEnvironmentError(Exception):
    """The environment cannot provide what the caller asked for."""


@dataclass(frozen=True)
class Capture:
    text: str
    truncated: bool
    ansi: bool


@dataclass(frozen=True)
class FileChanges:
    created: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RunOutcome:
    returncode: int | None
    timed_out: bool
    stdout: Capture | None
    stderr: Capture | None
    output: Capture | None


@dataclass(frozen=True)
class ProbeResult:
    args: list[str]
    mode: str
    exit_code: int | None
    signal: str | None
    timed_out: bool
    duration_s: float
    stdout: Capture | None
    stderr: Capture | None
    output: Capture | None
    workdir_changes: FileChanges
    home_changes: FileChanges


def capture(data: bytes) -> Capture:
    """Decode captured bytes, keeping at most CAPTURE_LIMIT and noting ANSI escapes anywhere in them."""
    return Capture(
        text=data[:CAPTURE_LIMIT].decode("utf-8", errors="replace"),
        truncated=len(data) > CAPTURE_LIMIT,
        ansi=bool(ANSI.search(data)),
    )


def snapshot(root: Path) -> dict[str, str]:
    """Map each file under root to a fingerprint: a content hash for small files, size and mtime otherwise."""
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            result[str(path.relative_to(root))] = "link:" + os.readlink(path)
        elif path.is_file():
            stat = path.stat()
            if stat.st_size <= HASH_LIMIT:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                result[str(path.relative_to(root))] = "sha256:" + digest
            else:
                result[str(path.relative_to(root))] = (
                    f"size:{stat.st_size}:mtime:{stat.st_mtime_ns}"
                )
    return result


def compare(before: dict[str, str], after: dict[str, str]) -> FileChanges:
    return FileChanges(
        created=sorted(set(after) - set(before)),
        deleted=sorted(set(before) - set(after)),
        modified=sorted(path for path in set(before) & set(after) if before[path] != after[path]),
    )


def directory_size(root: Path) -> int:
    return sum(
        path.stat().st_size for path in root.rglob("*") if path.is_file() and not path.is_symlink()
    )


@dataclass(frozen=True)
class Sandbox:
    root: Path
    workdir: Path
    home: Path

    @classmethod
    def create(cls, source: Path | None, home_source: Path | None = None) -> Sandbox:
        root = Path(tempfile.mkdtemp(prefix="probe-cli-"))
        workdir = root / "work"
        if source is None:
            workdir.mkdir()
        else:
            shutil.copytree(source, workdir, symlinks=True)
        home = root / "home"
        if home_source is not None:
            shutil.copytree(home_source, home, symlinks=True)
        for sub in ("config", "data", "cache", "state"):
            (home / sub).mkdir(parents=True, exist_ok=True)
        (root / "tmp").mkdir()
        (root / "run").mkdir(mode=0o700)
        return cls(root=root, workdir=workdir, home=home)

    def environment(self, extra: dict[str, str]) -> dict[str, str]:
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "LANG": "C.UTF-8",
            "HOME": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / "config"),
            "XDG_DATA_HOME": str(self.home / "data"),
            "XDG_CACHE_HOME": str(self.home / "cache"),
            "XDG_STATE_HOME": str(self.home / "state"),
            "XDG_RUNTIME_DIR": str(self.root / "run"),
            "TMPDIR": str(self.root / "tmp"),
        }
        env.update(extra)
        return env

    def remove(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def kill_group(process: subprocess.Popen[bytes]) -> None:
    """Stop the probe's whole process group: SIGTERM, then SIGKILL after a grace period."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=KILL_GRACE_SECONDS)
            return
        except subprocess.TimeoutExpired:
            continue


def status_fields(returncode: int | None) -> tuple[int | None, str | None]:
    """Split a Popen return code into an exit code and the name of a terminating signal."""
    if returncode is None:
        return None, None
    if returncode < 0:
        return 128 - returncode, signal.Signals(-returncode).name
    return returncode, None


def run_pipe(argv: list[str], cwd: Path, env: dict[str, str], timeout: float) -> RunOutcome:
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    timed_out = False
    try:
        out, err = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_group(process)
        out, err = process.communicate()
    else:
        kill_group(process)  # reap anything the tool left running in its group
    return RunOutcome(process.returncode, timed_out, capture(out), capture(err), None)


def run_tty(argv: list[str], cwd: Path, env: dict[str, str], timeout: float) -> RunOutcome:
    import pty  # POSIX only; imported here so pipe mode works everywhere

    master, slave = pty.openpty()
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=env,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            start_new_session=True,
        )
    finally:
        os.close(slave)
    chunks: list[bytes] = []
    deadline = time.monotonic() + timeout
    timed_out = False
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = process.poll() is None
                break
            ready, _, _ = select.select([master], [], [], min(remaining, 0.1))
            if ready:
                try:
                    chunk = os.read(master, 4096)
                except OSError:  # EIO: every writer closed the terminal
                    chunk = b""
                if not chunk:
                    break
                chunks.append(chunk)
            elif process.poll() is not None:
                break
    finally:
        kill_group(process)
        process.wait()
        os.close(master)
    return RunOutcome(process.returncode, timed_out, None, None, capture(b"".join(chunks)))


def run_probe(
    prefix: list[str],
    args: tuple[str, ...],
    mode: str,
    source: Path | None,
    options: argparse.Namespace,
) -> ProbeResult:
    sandbox = Sandbox.create(source, options.home_from)
    try:
        extra = dict(options.env)
        for name in options.keep_env:
            if name in os.environ:
                extra[name] = os.environ[name]
        if mode == "tty-dumb":
            extra["TERM"] = "dumb"
        elif mode.startswith("tty"):
            extra.setdefault("TERM", "xterm-256color")
        if mode == "tty-no-color":
            extra["NO_COLOR"] = "1"
        env = sandbox.environment(extra)
        argv = [*options.wrapper, *prefix, *args]
        work_before, home_before = snapshot(sandbox.workdir), snapshot(sandbox.home)
        runner = run_pipe if mode == "pipe" else run_tty
        started = time.monotonic()
        outcome = runner(argv, sandbox.workdir, env, options.timeout)
        duration = round(time.monotonic() - started, 3)
        exit_code, signal_name = status_fields(outcome.returncode)
        return ProbeResult(
            args=list(args),
            mode=mode,
            exit_code=exit_code,
            signal=signal_name,
            timed_out=outcome.timed_out,
            duration_s=duration,
            stdout=outcome.stdout,
            stderr=outcome.stderr,
            output=outcome.output,
            workdir_changes=compare(work_before, snapshot(sandbox.workdir)),
            home_changes=compare(home_before, snapshot(sandbox.home)),
        )
    finally:
        sandbox.remove()


def resolve_prefix(command: list[str], source: Path | None) -> list[str]:
    """Make a path-like command absolute unless it will resolve inside the copied working directory."""
    first = command[0]
    if "/" in first:
        if source is not None and (source / first).exists() and not os.path.isabs(first):
            return command
        path = Path(first).resolve()
        if not path.exists():
            raise ProbeEnvironmentError(f"command not found: {first}")
        return [str(path), *command[1:]]
    if shutil.which(first) is None:
        raise ProbeEnvironmentError(f"command not found on PATH: {first}")
    return command


def network_wrapper(requested: bool) -> list[str]:
    if not requested:
        return []
    unshare = shutil.which("unshare")
    if unshare is None:
        raise ProbeEnvironmentError("--isolate-network needs unshare, which is not installed")
    check = subprocess.run([unshare, "--user", "--net", "true"], capture_output=True, check=False)
    if check.returncode != 0:
        detail = check.stderr.decode(errors="replace").strip()
        raise ProbeEnvironmentError(f"--isolate-network: unshare --user --net failed: {detail}")
    return [unshare, "--user", "--net", "--"]


def parse_env(values: list[str]) -> dict[str, str]:
    env: dict[str, str] = {}
    for value in values:
        name, sep, content = value.partition("=")
        if not sep or not name:
            raise argparse.ArgumentTypeError(f"--env expects NAME=VALUE, got {value!r}")
        env[name] = content
    return env


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="probe_cli.py",
        description="Probe a command-line tool in a throwaway sandbox and print the results as JSON.",
        epilog="example: probe_cli.py --workdir . --help-for deploy --modes pipe,tty -- ./bin/mytool",
    )
    parser.add_argument(
        "--workdir", type=Path, help="directory copied into each sandbox as the working directory"
    )
    parser.add_argument(
        "--probe",
        action="append",
        default=[],
        metavar="ARGS",
        help="extra probe, as one shell-quoted string of arguments (repeatable)",
    )
    parser.add_argument(
        "--help-for",
        action="append",
        default=[],
        metavar="SUBCOMMAND",
        help="add a 'SUBCOMMAND --help' probe (repeatable)",
    )
    parser.add_argument(
        "--no-default-probes",
        action="store_true",
        help="run only the probes given with --probe and --help-for",
    )
    parser.add_argument(
        "--skip-bare",
        action="store_true",
        help="leave out the probe with no arguments (for tools whose bare form acts)",
    )
    parser.add_argument(
        "--modes",
        default=",".join(DEFAULT_MODES),
        help=f"comma-separated modes from {', '.join(MODES)} (default: %(default)s)",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, help="seconds per probe (default: %(default)s)"
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="set a variable in every probe (repeatable)",
    )
    parser.add_argument(
        "--keep-env",
        action="append",
        default=[],
        metavar="NAME",
        help="pass one variable through from this environment (repeatable)",
    )
    parser.add_argument(
        "--isolate-network",
        action="store_true",
        help="run every probe without network access; fails if that is unavailable",
    )
    parser.add_argument(
        "--max-workdir-mb",
        type=float,
        default=200.0,
        help="refuse to copy a larger working directory (default: %(default)s)",
    )
    parser.add_argument(
        "--home-from",
        type=Path,
        help="directory copied into each sandbox as the temporary HOME, for tools that load files from HOME",
    )
    parser.add_argument("--output", type=Path, help="write the JSON report here instead of stdout")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- COMMAND [ARGS...]")
    return parser


def join_dash_probes(argv: list[str]) -> list[str]:
    """Rewrite `--probe -h` as `--probe=-h`, which argparse would otherwise read as a missing value."""
    joined: list[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token == "--":
            joined.extend(argv[index:])
            break
        if token == "--probe" and index + 1 < len(argv) and argv[index + 1].startswith("-"):
            joined.append(f"--probe={argv[index + 1]}")
            index += 2
            continue
        joined.append(token)
        index += 1
    return joined


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(join_dash_probes(sys.argv[1:] if argv is None else argv))
    command = options.command[1:] if options.command[:1] == ["--"] else options.command
    if not command:
        parser.error("give the command to probe after --")
    modes = [mode.strip() for mode in options.modes.split(",") if mode.strip()]
    unknown = [mode for mode in modes if mode not in MODES]
    if unknown or not modes:
        parser.error(
            f"unknown mode {', '.join(unknown) or '(none)'}; choose from {', '.join(MODES)}"
        )
    if options.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        options.env = parse_env(options.env)
        extra_probes = [tuple(shlex.split(probe)) for probe in options.probe]
    except (argparse.ArgumentTypeError, ValueError) as error:
        parser.error(str(error))

    probes: list[tuple[str, ...]] = []
    if not options.no_default_probes:
        probes.extend(p for p in DEFAULT_PROBES if p or not options.skip_bare)
    probes.extend((name, "--help") for name in options.help_for)
    probes.extend(extra_probes)
    if not probes:
        parser.error("no probes left to run")

    source: Path | None = None
    try:
        if options.workdir is not None:
            resolved: Path = options.workdir.resolve()
            if not resolved.is_dir():
                raise ProbeEnvironmentError(f"--workdir is not a directory: {options.workdir}")
            size_mb = directory_size(resolved) / (1024 * 1024)
            if size_mb > options.max_workdir_mb:
                raise ProbeEnvironmentError(
                    f"--workdir holds {size_mb:.0f} MB, over --max-workdir-mb {options.max_workdir_mb:.0f}"
                )
            source = resolved
        if options.home_from is not None:
            options.home_from = options.home_from.resolve()
            if not options.home_from.is_dir():
                raise ProbeEnvironmentError(f"--home-from is not a directory: {options.home_from}")
        prefix = resolve_prefix(command, source)
        options.wrapper = network_wrapper(options.isolate_network)
    except ProbeEnvironmentError as error:
        print(f"probe_cli.py: error: {error}", file=sys.stderr)
        return EXIT_ENVIRONMENT

    results = [
        asdict(run_probe(prefix, probe, mode, source, options))
        for probe in probes
        for mode in modes
    ]
    report = {
        "command": prefix,
        "workdir": str(source) if source else None,
        "modes": modes,
        "timeout_s": options.timeout,
        "network_isolated": bool(options.wrapper),
        "containment": "relative paths, HOME, XDG, the runtime directory and TMPDIR only; absolute paths "
        "and the network are not "
        "contained" + ("" if options.wrapper else "; network access was available"),
        "probes": results,
    }
    text = json.dumps(report, indent=2) + "\n"
    if options.output is not None:
        options.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
