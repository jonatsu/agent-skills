"""Build, lint, and run the Rust code examples in skill packages.

A fenced block whose info string starts with `rust` is a Rust example, and its labels say what it must prove:

- `rust`: it builds, and clippy passes with warnings denied, with and without `cfg(test)`.
- `rust,run`: it also passes its own tests, and its `main`, when it has one, exits 0.
- `rust,compile_fail,E0277`: it fails to build with that error code and no other error.

A `toml,manifest` block is a `Cargo.toml` fragment that cargo and clippy must accept, and a `toml,clippy-config`
block is a `clippy.toml` that clippy must accept. Any other label in either family is a finding, and so are a
misspelled language such as `rs` and, in a package with Rust examples, an unlabelled `toml` block. A typo
therefore cannot silently skip a block. Write a snippet that should not be checked as `text`.

An example with a `main` becomes a binary target of a host package copied from `checks/rust_examples`, which
pins the dependencies examples may use; any other example becomes the host's library, so library lints apply.
An example that passed is recorded by a hash of everything that decides its result, including this module, so
only changed examples are built again.
"""

from __future__ import annotations

import contextlib
import hashlib
import os
import re
import shutil
import signal
import subprocess
import tempfile
from collections.abc import Iterable, Sequence
from pathlib import Path

import attrs

from skill_checks.skill_tree import package_files

RUST_LABELS = frozenset({"run", "compile_fail"})
TOML_LABELS = frozenset({"manifest", "clippy-config"})
ERROR_CODE_RE = re.compile(r"^E\d{4}$")
# A fence may sit inside block quotes and be indented with spaces or tabs, as in a list item.
FENCE_RE = re.compile(
    r"^(?P<quote>(?:[ \t]*>)*)(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})(?P<info>.*)$"
)
QUOTE_MARKER_RE = re.compile(r"^[ \t]*> ?")
MAIN_RE = re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+main\s*\(", re.MULTILINE)
COMPILER_ERROR_CODE_RE = re.compile(r"error\[(E\d{4})\]")
# An error line without a code, except the summary cargo prints after any failed build.
UNCODED_ERROR_RE = re.compile(r"^error(?!\[)(?!: could not compile )", re.MULTILINE)
# Variables that change what cargo or clippy does without changing the example; the check sets its own.
SCRUBBED_VARIABLES = (
    "RUSTFLAGS",
    "CARGO_ENCODED_RUSTFLAGS",
    "CARGO_BUILD_RUSTFLAGS",
    "RUSTDOCFLAGS",
    "CLIPPY_CONF_DIR",
    "CARGO_TARGET_DIR",
    "CARGO_BUILD_TARGET_DIR",
)
COMMAND_TIMEOUT_SECONDS = 600
RUN_TIMEOUT_SECONDS = 60
DRAIN_TIMEOUT_SECONDS = 10
OUTPUT_LINES_SHOWN = 40
MANIFEST_PACKAGE = (
    '[package]\nname = "manifest-example"\nversion = "0.0.0"\nedition = "2024"\npublish = false\n\n'
)


class RustToolchainMissing(Exception):
    """Cargo is not on PATH, so no example can be checked."""


@attrs.frozen
class Example:
    """One fenced code block the check proves."""

    path: Path
    line: int
    language: str
    labels: tuple[str, ...]
    code: str

    @property
    def expected_error(self) -> str | None:
        codes = [label for label in self.labels if ERROR_CODE_RE.match(label)]
        return codes[0] if codes else None

    @property
    def is_binary(self) -> bool:
        return MAIN_RE.search(self.code) is not None


@attrs.frozen
class ExampleFinding:
    """One example that failed, or a block whose labels are wrong."""

    example: Example
    message: str
    output: str = ""


@attrs.frozen
class ExampleReport:
    """The result of one check run."""

    checked: int
    skipped_unchanged: int
    findings: tuple[ExampleFinding, ...]


def collect_package_examples(packages: Iterable[Path]) -> tuple[Example, ...]:
    """Return the examples of every package, adding its unlabelled TOML blocks when it has Rust examples."""
    examples: list[Example] = []
    for package in packages:
        files = sorted(path for path in package_files(package) if path.suffix == ".md")
        found = collect_examples(files, include_plain_toml=True)
        if any(example.language != "toml" for example in found):
            examples.extend(found)
        else:
            examples.extend(example for example in found if example.labels)
    return tuple(examples)


def collect_examples(
    markdown_files: Iterable[Path], *, include_plain_toml: bool = False
) -> tuple[Example, ...]:
    """Return every Rust and checked TOML block in the files, in file and line order."""
    examples: list[Example] = []
    for path in markdown_files:
        for example in _examples_in(path, path.read_text(encoding="utf-8")):
            if example.language == "toml" and not example.labels and not include_plain_toml:
                continue
            examples.append(example)
    return tuple(examples)


def _examples_in(path: Path, text: str) -> Iterable[Example]:
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        opening = FENCE_RE.match(lines[index])
        if opening is None:
            index += 1
            continue
        opening_line = index + 1
        fence = opening["fence"]
        depth = opening["quote"].count(">")
        indent = len(opening["indent"])
        body: list[str] = []
        index += 1
        while index < len(lines):
            line = _dedent(_unquote(lines[index], depth), indent)
            if _closes(line, fence):
                break
            body.append(line)
            index += 1
        index += 1
        example = _example_from(path, opening_line, opening["info"].strip(), body)
        if example is not None:
            yield example


def _unquote(line: str, depth: int) -> str:
    for _ in range(depth):
        line = QUOTE_MARKER_RE.sub("", line, count=1)
    return line


def _closes(line: str, fence: str) -> bool:
    stripped = line.strip()
    return len(stripped) >= len(fence) and set(stripped) == {fence[0]}


def _dedent(line: str, indent: int) -> str:
    removable = len(line) - len(line.lstrip(" \t"))
    return line[min(indent, removable) :]


def _example_from(path: Path, line: int, info: str, body: list[str]) -> Example | None:
    words = info.split()
    if not words:
        return None
    language, *labels = [part.strip() for part in words[0].split(",")]
    if language.lower() in {"rust", "rs"} or language == "toml":
        return Example(path, line, language, tuple(labels), "\n".join(body) + "\n")
    return None


def label_problem(example: Example) -> str | None:
    """Return why an example's labels are invalid, or None when they are valid."""
    if example.language == "toml":
        if len(example.labels) != 1 or example.labels[0] not in TOML_LABELS:
            return (
                f"a TOML block in a Rust skill takes exactly one of {sorted(TOML_LABELS)}; "
                "use `text` for one that is not checked"
            )
        return None
    if example.language != "rust":
        return f"write the language as `rust`, not `{example.language}`, so the block is checked"
    unknown = [
        label
        for label in example.labels
        if label not in RUST_LABELS and not ERROR_CODE_RE.match(label)
    ]
    if unknown:
        return f"unknown label {', '.join(unknown)}; use `text` for a block that is not checked"
    codes = [label for label in example.labels if ERROR_CODE_RE.match(label)]
    if "compile_fail" in example.labels:
        if "run" in example.labels:
            return "compile_fail and run exclude each other"
        if len(codes) != 1:
            return "compile_fail needs exactly one error code, such as compile_fail,E0277"
    elif codes:
        return "an error code needs compile_fail"
    return None


@attrs.frozen
class Workspace:
    """Where the check builds: a host package for Rust examples and crates for TOML ones."""

    template: Path
    root: Path

    @property
    def host(self) -> Path:
        return self.root.resolve() / "host"

    @property
    def host_target(self) -> Path:
        return self.host / "target"

    @property
    def record(self) -> Path:
        return self.root / "passed.txt"


def check_examples(
    examples: Sequence[Example], workspace: Workspace, *, use_record: bool = True
) -> ExampleReport:
    """Prove every example, skipping those recorded as passed under the same inputs.

    Raises:
        RustToolchainMissing: If cargo is not on PATH.
    """
    if shutil.which("cargo") is None:
        raise RustToolchainMissing("cargo is not on PATH; install the toolchain mise.toml pins")
    _prepare_host(workspace)
    toolchain = (
        _run(["cargo", "clippy", "--version"], workspace.host).output
        + _run(["rustc", "--version", "--verbose"], workspace.host).output
    )
    passed = _read_record(workspace) if use_record else set[str]()
    findings: list[ExampleFinding] = []
    skipped = 0
    for example in examples:
        problem = label_problem(example)
        if problem is not None:
            findings.append(ExampleFinding(example, problem))
            continue
        key = _record_key(example, workspace, toolchain)
        if key in passed:
            skipped += 1
            continue
        finding = _prove(example, workspace, key)
        if finding is None:
            passed.add(key)
            _append_record(workspace, key)
        else:
            findings.append(finding)
    return ExampleReport(len(examples), skipped, tuple(findings))


def _prepare_host(workspace: Workspace) -> None:
    workspace.host.mkdir(parents=True, exist_ok=True)
    for name in ("Cargo.toml", "Cargo.lock"):
        shutil.copyfile(workspace.template / name, workspace.host / name)
    # An empty clippy.toml stops clippy from reading one in a parent directory.
    (workspace.host / "clippy.toml").write_text("", encoding="utf-8")
    _restore_library(workspace)
    bins = workspace.host / "src" / "bin"
    shutil.rmtree(bins, ignore_errors=True)
    bins.mkdir()


def _restore_library(workspace: Workspace) -> None:
    (workspace.host / "src").mkdir(exist_ok=True)
    shutil.copyfile(workspace.template / "src" / "lib.rs", workspace.host / "src" / "lib.rs")


def _record_key(example: Example, workspace: Workspace, toolchain: str) -> str:
    digest = hashlib.sha256()
    for part in (
        Path(__file__).read_text(encoding="utf-8"),
        toolchain,
        (workspace.template / "Cargo.toml").read_text(encoding="utf-8"),
        (workspace.template / "Cargo.lock").read_text(encoding="utf-8"),
        (workspace.template / "src" / "lib.rs").read_text(encoding="utf-8"),
        example.language,
        ",".join(example.labels),
        example.code,
    ):
        digest.update(part.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def _read_record(workspace: Workspace) -> set[str]:
    if not workspace.record.exists():
        return set()
    return set(workspace.record.read_text(encoding="utf-8").split())


def _append_record(workspace: Workspace, key: str) -> None:
    with workspace.record.open("a", encoding="utf-8") as record:
        record.write(key + "\n")


def _prove(example: Example, workspace: Workspace, key: str) -> ExampleFinding | None:
    if example.language == "toml":
        return _prove_toml(example, workspace, key)
    if example.is_binary:
        name = f"example_{key[:12]}"
        source = workspace.host / "src" / "bin" / f"{name}.rs"
        selector = ["--bin", name]
    else:
        source = workspace.host / "src" / "lib.rs"
        selector = ["--lib"]
    source.write_text(example.code, encoding="utf-8")
    try:
        if "compile_fail" in example.labels:
            return _prove_compile_fail(example, workspace, selector)
        return _prove_builds(example, workspace, selector)
    finally:
        if example.is_binary:
            source.unlink()
        else:
            _restore_library(workspace)


def _prove_builds(
    example: Example, workspace: Workspace, selector: list[str]
) -> ExampleFinding | None:
    lint = ["cargo", "clippy", "--locked", "--quiet", *selector]
    for extra, what in (([], "clippy"), (["--profile", "test"], "clippy under cfg(test)")):
        result = _run([*lint, *extra, "--", "-D", "warnings"], workspace.host, _target(workspace))
        if result.status != 0:
            return ExampleFinding(example, f"{what} failed", result.output)
    if "run" not in example.labels:
        return None
    tests = _run(
        ["cargo", "test", "--locked", "--quiet", *selector], workspace.host, _target(workspace)
    )
    if tests.status != 0:
        return ExampleFinding(example, _status_message("its tests", tests), tests.output)
    if not example.is_binary:
        return None
    build = _run(
        ["cargo", "build", "--locked", "--quiet", *selector], workspace.host, _target(workspace)
    )
    if build.status != 0:
        return ExampleFinding(example, "build before running failed", build.output)
    binary = workspace.host_target / "debug" / selector[1]
    ran = _run([str(binary)], workspace.host, timeout=RUN_TIMEOUT_SECONDS)
    if ran.status != 0:
        return ExampleFinding(example, _status_message("running it", ran), ran.output)
    return None


def _prove_compile_fail(
    example: Example, workspace: Workspace, selector: list[str]
) -> ExampleFinding | None:
    result = _run(
        ["cargo", "build", "--locked", "--quiet", *selector], workspace.host, _target(workspace)
    )
    expected = example.expected_error
    if result.status == 0:
        return ExampleFinding(example, f"expected error {expected}, but it builds")
    codes = set(COMPILER_ERROR_CODE_RE.findall(result.output))
    if codes != {expected} or UNCODED_ERROR_RE.search(result.output):
        found = ", ".join(sorted(codes)) or "errors without a code"
        return ExampleFinding(example, f"expected only {expected}, found {found}", result.output)
    return None


def _prove_toml(example: Example, workspace: Workspace, key: str) -> ExampleFinding | None:
    crate = workspace.root.resolve() / "toml" / key[:12]
    shutil.rmtree(crate, ignore_errors=True)
    (crate / "src").mkdir(parents=True)
    (crate / "src" / "lib.rs").write_text("//! A crate for one TOML example.\n", encoding="utf-8")
    if example.labels == ("manifest",):
        manifest = example.code if "[package]" in example.code else MANIFEST_PACKAGE + example.code
        if "[workspace]" not in manifest:
            manifest += "\n[workspace]\n"
        (crate / "Cargo.toml").write_text(manifest, encoding="utf-8")
        (crate / "clippy.toml").write_text("", encoding="utf-8")
    else:
        (crate / "Cargo.toml").write_text(MANIFEST_PACKAGE + "[workspace]\n", encoding="utf-8")
        (crate / "clippy.toml").write_text(example.code, encoding="utf-8")
    environment = {"CARGO_TARGET_DIR": str(workspace.root.resolve() / "toml-target")}
    try:
        result = _run(
            ["cargo", "clippy", "--quiet", "--offline", "--", "-D", "warnings"], crate, environment
        )
    finally:
        shutil.rmtree(crate, ignore_errors=True)
    if result.status != 0:
        return ExampleFinding(example, "cargo or clippy rejected it", result.output)
    return None


def _target(workspace: Workspace) -> dict[str, str]:
    return {"CARGO_TARGET_DIR": str(workspace.host_target)}


@attrs.frozen
class _Result:
    status: int
    output: str
    timed_out: bool = False


def _status_message(what: str, result: _Result) -> str:
    if result.timed_out:
        return f"{what} timed out"
    return f"{what} exited {result.status}"


def _run(
    command: list[str],
    directory: Path,
    environment: dict[str, str] | None = None,
    *,
    timeout: int = COMMAND_TIMEOUT_SECONDS,
) -> _Result:
    """Run a command in its own process group, and kill the group however the run ends.

    Output goes to a file rather than a pipe, so a descendant that outlives the group cannot hold the check open.
    """
    env = {name: value for name, value in os.environ.items() if name not in SCRUBBED_VARIABLES}
    env.update({"CARGO_TERM_COLOR": "never", **(environment or {})})
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace") as output:
        process = subprocess.Popen(
            command,
            cwd=directory,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        timed_out = False
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            _kill_group(process.pid)
            process.wait(timeout=DRAIN_TIMEOUT_SECONDS)
        output.seek(0)
        text = output.read()
    if timed_out:
        return _Result(-1, text, timed_out=True)
    return _Result(process.returncode, text)


def _kill_group(group: int) -> None:
    with contextlib.suppress(ProcessLookupError):
        os.killpg(group, signal.SIGKILL)


def format_report(report: ExampleReport, root: Path) -> str:
    """Render findings with a bounded excerpt of the compiler output, then a summary line."""
    lines: list[str] = []
    for finding in report.findings:
        example = finding.example
        labels = ",".join((example.language, *example.labels))
        lines.append(
            f"FAIL  {example.path.relative_to(root)}:{example.line} [{labels}]: {finding.message}"
        )
        excerpt = finding.output.strip().splitlines()[:OUTPUT_LINES_SHOWN]
        lines.extend(f"      {line}" for line in excerpt)
    lines.append(
        f"rust-examples: {report.checked} example(s), {report.skipped_unchanged} unchanged since they passed, "
        f"{len(report.findings)} failure(s)"
    )
    return "\n".join(lines) + "\n"
