"""Tests for the Rust example check: label parsing without cargo, and each proof against a planted failure."""

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from skill_checks.rust_examples import (
    Example,
    ExampleReport,
    Workspace,
    check_examples,
    collect_examples,
    collect_package_examples,
    label_problem,
)

FENCE = "```"


def _markdown(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "SKILL.md"
    path.write_text(body, encoding="utf-8")
    return path


def _example(info: str, code: str) -> Example:
    language, *labels = info.split(",")
    return Example(Path("SKILL.md"), 1, language, tuple(labels), code)


def test_collects_rust_and_checked_toml_blocks_only(tmp_path: Path) -> None:
    path = _markdown(
        tmp_path,
        f"{FENCE}rust\nfn a() {{}}\n{FENCE}\n\n{FENCE}toml\n[x]\n{FENCE}\n\n"
        f"{FENCE}toml,manifest\n[lints.rust]\n{FENCE}\n\n{FENCE}text\nnot checked\n{FENCE}\n",
    )
    examples = collect_examples([path])
    assert [(example.language, example.labels, example.line) for example in examples] == [
        ("rust", (), 1),
        ("toml", ("manifest",), 9),
    ]


def test_dedents_a_block_inside_a_list_item(tmp_path: Path) -> None:
    path = _markdown(tmp_path, f"1. Item:\n\n   {FENCE}rust\n   fn a() {{}}\n   {FENCE}\n")
    (example,) = collect_examples([path])
    assert example.code == "fn a() {}\n"


def test_a_longer_fence_hides_the_blocks_it_contains(tmp_path: Path) -> None:
    path = _markdown(tmp_path, f"````markdown\n{FENCE}rust\nnot real\n{FENCE}\n````\n")
    assert collect_examples([path]) == ()


def test_reads_quoted_tab_indented_and_tilde_fences(tmp_path: Path) -> None:
    path = _markdown(
        tmp_path,
        f"> {FENCE}rust\n> fn a() {{}}\n> {FENCE}\n\n\t~~~rust\n\tfn b() {{}}\n\t~~~\n\n{FENCE}rust\nfn c() {{}}\n",
    )
    assert [example.code for example in collect_examples([path])] == [
        "fn a() {}\n",
        "fn b() {}\n",
        "fn c() {}\n",
    ]


def test_a_misspelled_language_is_a_finding(tmp_path: Path) -> None:
    path = _markdown(tmp_path, f"{FENCE}rs\nfn a() {{}}\n{FENCE}\n")
    (example,) = collect_examples([path])
    problem = label_problem(example)
    assert problem is not None and "not `rs`" in problem


def test_plain_toml_counts_only_in_a_package_with_rust_examples(
    write_skill: Callable[[str], Path],
) -> None:
    rust = write_skill("development/rust-x")
    (rust / "SKILL.md").write_text(
        f"{FENCE}rust\nfn a() {{}}\n{FENCE}\n{FENCE}toml\n[lints]\n{FENCE}\n"
    )
    other = write_skill("development/python-x")
    (other / "SKILL.md").write_text(f"{FENCE}toml\n[project]\n{FENCE}\n")
    subprocess.run(["git", "init", "-q"], cwd=rust.parent.parent, check=True)
    subprocess.run(["git", "add", "."], cwd=rust.parent.parent, check=True)
    examples = collect_package_examples([rust, other])
    assert [(example.path.parent.name, example.language) for example in examples] == [
        ("rust-x", "rust"),
        ("rust-x", "toml"),
    ]
    assert label_problem(examples[1]) is not None


@pytest.mark.parametrize(
    ("info", "problem"),
    [
        ("rust", None),
        ("rust,run", None),
        ("rust,compile_fail,E0277", None),
        ("toml,manifest", None),
        ("toml,clippy-config", None),
        ("rust,ignore", "unknown label ignore"),
        ("rust,compile_fail", "needs an error code"),
        ("rust,compile_fail,E0277,E0308", "at most one error code"),
        ("rust,compile_fail,E0277,run", "exclude each other"),
        ("rust,E0277", "needs compile_fail"),
        ("toml,cargo", "exactly one of"),
    ],
)
def test_label_rules(info: str, problem: str | None) -> None:
    found = label_problem(_example(info, ""))
    if problem is None:
        assert found is None
    else:
        assert found is not None and problem in found


@pytest.fixture(scope="module")
def template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A host package with no dependencies, so the proofs build in seconds and offline."""
    directory = tmp_path_factory.mktemp("template")
    (directory / "src").mkdir()
    (directory / "src" / "lib.rs").write_text("//! Host.\n", encoding="utf-8")
    (directory / "Cargo.toml").write_text(
        '[package]\nname = "host"\nversion = "0.0.0"\nedition = "2024"\npublish = false\n\n[workspace]\n',
        encoding="utf-8",
    )
    subprocess.run(["cargo", "generate-lockfile", "--offline"], cwd=directory, check=True)
    return directory


@pytest.fixture(scope="module")
def workspace(template: Path, tmp_path_factory: pytest.TempPathFactory) -> Workspace:
    return Workspace(template, tmp_path_factory.mktemp("work"))


def _check(workspace: Workspace, info: str, code: str) -> ExampleReport:
    return check_examples([_example(info, code)], workspace, use_record=False)


def _message(report: ExampleReport) -> str:
    assert len(report.findings) == 1, report
    return report.findings[0].message


@pytest.mark.parametrize(
    ("info", "code"),
    [
        ("rust", "pub fn double(value: u32) -> u32 {\n    value * 2\n}\n"),
        ("rust,run", 'fn main() {\n    assert_eq!("ab".repeat(2), "abab");\n}\n'),
        (
            "rust,run",
            "pub fn double(value: u32) -> u32 {\n    value * 2\n}\n\n#[cfg(test)]\nmod tests {\n"
            "    #[test]\n    fn doubles() {\n        assert_eq!(super::double(2), 4);\n    }\n}\n",
        ),
        ("rust,compile_fail,E0308", 'fn main() {\n    let _count: u32 = "one";\n}\n'),
        (
            "rust,compile_fail",
            "// error: future cannot be sent between threads safely\n"
            "fn require_send<T: Send>(_: T) {}\n\nfn main() {\n"
            "    require_send(async {\n        let rc = std::rc::Rc::new(1);\n"
            "        std::future::ready(()).await;\n        drop(rc);\n    });\n}\n",
        ),
        ("toml,manifest", '[lints.clippy]\npedantic = { level = "warn", priority = -1 }\n'),
        ("toml,clippy-config", 'msrv = "1.85"\n'),
    ],
)
def test_a_correct_example_passes(workspace: Workspace, info: str, code: str) -> None:
    assert _check(workspace, info, code).findings == ()


@pytest.mark.parametrize(
    ("info", "code", "message"),
    [
        ("rust", 'fn main() {\n    let count: u32 = "one";\n}\n', "clippy failed"),
        (
            "rust",
            "fn main() {\n    let items = vec![1];\n    let _ = items.len() == 0;\n}\n",
            "clippy failed",
        ),
        (
            "rust",
            "#[cfg(test)]\nmod tests {\n    #[test]\n    fn t() {\n        let v = vec![1];\n"
            "        assert!(v.len() > 0);\n    }\n}\n",
            "clippy under cfg(test) failed",
        ),
        ("rust,run", "fn main() {\n    std::process::exit(3);\n}\n", "running it exited 3"),
        (
            "rust,run",
            "#[cfg(test)]\nmod tests {\n    #[test]\n    fn t() {\n        assert_eq!(1, 2);\n    }\n}\n",
            "its tests exited",
        ),
        ("rust,compile_fail,E0308", "fn main() {}\n", "but it builds"),
        (
            "rust,compile_fail,E0277",
            'fn main() {\n    let _count: u32 = "one";\n}\n',
            "expected only E0277, found E0308",
        ),
        (
            "toml,manifest",
            '[lints.clippy]\npedantic = "warn"\nmust_use_candidate = "allow"\n',
            "rejected",
        ),
        ("toml,clippy-config", 'warn = ["x"]\n', "rejected"),
        (
            "rust,compile_fail,E0308",
            'fn main() {\n    let _count: u32 = "one";\n    undefined_name();\n}\n',
            "expected only E0308, found E0308, E0425",
        ),
        ("rust", "fn unused_helper() {}\n\npub fn api() {}\n", "clippy failed"),
        (
            "rust,compile_fail",
            "// error: future cannot be sent between threads safely\nfn main() {\n    undefined_name();\n}\n",
            "found E0425",
        ),
        (
            "rust,compile_fail",
            "// error: future cannot be sent between threads safely\nfn main() {}\n",
            "but it builds",
        ),
    ],
)
def test_a_planted_failure_is_caught(
    workspace: Workspace, info: str, code: str, message: str
) -> None:
    assert message in _message(_check(workspace, info, code))


def test_a_library_example_keeps_its_inner_attributes_first(workspace: Workspace) -> None:
    code = "//! Docs.\n#![forbid(unsafe_code)]\n\npub fn one() -> u32 {\n    1\n}\n"
    assert _check(workspace, "rust", code).findings == ()


def test_a_failed_example_is_not_recorded(template: Path, tmp_path: Path) -> None:
    workspace = Workspace(template, tmp_path / "work")
    example = _example("rust", "fn main() {\n    let count: u32 = 1;\n}\n")
    assert check_examples([example], workspace).findings
    assert check_examples([example], workspace).skipped_unchanged == 0


def test_an_unchanged_example_is_skipped_after_it_passes(template: Path, tmp_path: Path) -> None:
    workspace = Workspace(template, tmp_path / "work")
    example = _example("rust", "pub fn one() -> u32 {\n    1\n}\n")
    assert check_examples([example], workspace).skipped_unchanged == 0
    assert check_examples([example], workspace).skipped_unchanged == 1
    changed = _example("rust", "pub fn two() -> u32 {\n    2\n}\n")
    assert check_examples([changed], workspace).skipped_unchanged == 0


def test_a_hanging_example_times_out(workspace: Workspace, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("skill_checks.rust_examples.RUN_TIMEOUT_SECONDS", 2)
    code = "fn main() {\n    loop {\n        std::thread::park();\n    }\n}\n"
    assert _message(_check(workspace, "rust,run", code)) == "running it timed out"
