"""Validate every skill's `evals/*.json` case files.

The schema in `eval_cases.schema.json` fixes each file's shape; an evaluation harness validates the files against it
at a pinned commit. This check adds what a schema cannot state: the file's `skill_name` matches its package, case ids
are unique within the file, and each named fixture is a directory inside the package's `evals/fixtures/`.
Only files directly in a package's `evals/` count, so a fixture repository's own `evals/` is never read.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path
from typing import Any

import attrs
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

SCHEMA_RESOURCE = "eval_cases.schema.json"


@attrs.frozen
class EvalFinding:
    """One problem in one case file."""

    path: Path
    location: str
    message: str


def load_schema() -> dict[str, Any]:
    """Return the eval case schema bundled with this package."""
    text = files("skill_checks").joinpath(SCHEMA_RESOURCE).read_text(encoding="utf-8")
    schema: dict[str, Any] = json.loads(text)
    return schema


def eval_files(skill_directories: Iterable[Path]) -> tuple[Path, ...]:
    """Return the case files directly inside each skill's `evals/` directory."""
    return tuple(sorted(path for directory in skill_directories for path in (directory / "evals").glob("*.json")))


def check_eval_file(path: Path, skill_directory: Path, validator: Draft202012Validator) -> list[EvalFinding]:
    """Return every finding for one case file, or none when it is valid."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [EvalFinding(path, "", f"cannot read as JSON: {error}")]
    findings = [
        finding
        for error in sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))
        for finding in _schema_findings(path, error)
    ]
    if not isinstance(document, dict):
        return findings
    if document.get("skill_name") != skill_directory.name:
        findings.append(
            EvalFinding(
                path,
                "skill_name",
                f"names {document.get('skill_name')!r}, not {skill_directory.name!r}",
            )
        )
    cases = document.get("cases")
    if isinstance(cases, list):
        findings.extend(_case_findings(path, cases))
    return findings


def check_eval_cases(skill_directories: Iterable[Path]) -> list[EvalFinding]:
    """Return every finding across the case files of the given skills."""
    validator = Draft202012Validator(load_schema())
    findings: list[EvalFinding] = []
    for directory in skill_directories:
        for path in eval_files((directory,)):
            findings.extend(check_eval_file(path, directory, validator))
    return findings


def _case_findings(path: Path, cases: list[Any]) -> list[EvalFinding]:
    findings: list[EvalFinding] = []
    ids = Counter(case.get("id") for case in cases if isinstance(case, dict))
    for case_id, count in sorted(ids.items(), key=lambda item: str(item[0])):
        if case_id is not None and count > 1:
            findings.append(EvalFinding(path, "cases", f"id {case_id!r} is used {count} times"))
    fixtures_root = (path.parent / "fixtures").resolve()
    for index, case in enumerate(cases):
        fixture = case.get("fixture") if isinstance(case, dict) else None
        if not isinstance(fixture, str):
            continue
        target = (path.parent / fixture).resolve()
        if not target.is_relative_to(fixtures_root) or target == fixtures_root:
            findings.append(EvalFinding(path, f"cases/{index}/fixture", f"{fixture!r} leaves evals/fixtures/"))
        elif not target.is_dir():
            findings.append(EvalFinding(path, f"cases/{index}/fixture", f"{fixture!r} is not a directory"))
    return findings


# The three case shapes in the schema's `oneOf`, in order, each named by a field only it has.
CASE_SHAPE_KEYS = ("outcomes", "assertions", "should_trigger")


def _schema_findings(path: Path, error: ValidationError) -> list[EvalFinding]:
    # A case matching no shape reports only "not valid under any of the given schemas". Report the errors of
    # the shape its own fields name instead, so the message says what to fix.
    if error.validator == "oneOf" and isinstance(error.instance, dict):
        shape = next((index for index, key in enumerate(CASE_SHAPE_KEYS) if key in error.instance), None)
        branch = [inner for inner in error.context or [] if inner.relative_schema_path[0] == shape]
        if branch:
            return [EvalFinding(path, _location(inner.absolute_path), inner.message) for inner in branch]
        return [
            EvalFinding(
                path,
                _location(error.absolute_path),
                "matches no case shape: needs outcomes, assertions, or should_trigger",
            )
        ]
    return [EvalFinding(path, _location(error.absolute_path), error.message)]


def _location(parts: Iterable[str | int]) -> str:
    return "/".join(str(part) for part in parts)
