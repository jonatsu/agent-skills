"""Planted case files that the eval case check must reject or accept."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from skill_checks.eval_cases import check_eval_cases

BEHAVIOR_CASE: dict[str, Any] = {
    "id": "01-plan-small-change",
    "prompt": "Plan the change.",
    "behavior": "Plans proportionately.",
    "outcomes": ["Names the affected files."],
}
REVIEW_CASE: dict[str, Any] = {
    "id": "harness-failure",
    "prompt": "Count the run.",
    "assertions": ["Treats the failure as a harness failure."],
}
ACTIVATION_CASE: dict[str, Any] = {
    "id": "create-from-work",
    "prompt": "Turn this into a skill.",
    "should_trigger": True,
    "reason": "The user asks to create a skill.",
}
WORKSPACE: dict[str, Any] = {
    "setup": "Copy the fixture.",
    "working_directory": ".",
    "allowed_writes": [],
    "cleanup": "Delete it.",
}


def write_cases(skill: Path, cases: list[dict[str, Any]], **top: Any) -> Path:
    document: dict[str, Any] = {
        "skill_name": skill.name,
        "mode": "explicit behavioral evaluation",
        "run_contract": {"supply_candidate_skill_path": True},
        "cases": cases,
    }
    document.update(top)
    path = skill / "evals" / "behavior.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def messages(skill: Path) -> list[str]:
    return [f"{finding.location}: {finding.message}" for finding in check_eval_cases([skill])]


def test_accepts_every_case_shape(write_skill: Callable[[str], Path]) -> None:
    skill = write_skill("group/planner")
    (skill / "evals" / "fixtures" / "repo").mkdir(parents=True)
    behavior = {
        **BEHAVIOR_CASE,
        "fixture": "fixtures/repo",
        "workspace": WORKSPACE,
        "conversation": ["The user chose the queue."],
    }
    scripted = {
        **BEHAVIOR_CASE,
        "id": "02-mixed",
        "conversation": [{"turn": 1, "user": "Design it.", "expected": "Stops before planning."}],
    }
    write_cases(skill, [behavior, scripted, REVIEW_CASE, ACTIVATION_CASE])
    assert messages(skill) == []


def test_ignores_a_fixture_repositorys_own_evals(write_skill: Callable[[str], Path]) -> None:
    skill = write_skill("group/planner")
    nested = skill / "evals" / "fixtures" / "repo" / "evals"
    nested.mkdir(parents=True)
    (nested / "behavior.json").write_text("not json", encoding="utf-8")
    write_cases(skill, [BEHAVIOR_CASE])
    assert messages(skill) == []


@pytest.mark.parametrize(
    ("cases", "top", "expected"),
    [
        ([{**BEHAVIOR_CASE, "outcomes": []}], {}, "cases/0/outcomes: [] should be non-empty"),
        ([{**BEHAVIOR_CASE, "extra": 1}], {}, "cases/0: Additional properties are not allowed"),
        ([{**BEHAVIOR_CASE, "id": "Bad_Id"}], {}, "cases/0/id: 'Bad_Id' does not match"),
        (
            [{**ACTIVATION_CASE, "should_trigger": "yes"}],
            {},
            "cases/0/should_trigger: 'yes' is not of type",
        ),
        ([{"id": "x", "prompt": "Do it."}], {}, "cases/0: matches no case shape"),
        ([BEHAVIOR_CASE, BEHAVIOR_CASE], {}, "cases: id '01-plan-small-change' is used 2 times"),
        (
            [BEHAVIOR_CASE],
            {"run_contract": {"supply_skill_path": True}},
            "run_contract: 'supply_candidate",
        ),
        ([BEHAVIOR_CASE], {"skill_name": "other"}, "skill_name: names 'other', not 'planner'"),
        ([{**BEHAVIOR_CASE, "fixture": "fixtures/absent"}], {}, "is not a directory"),
        ([{**BEHAVIOR_CASE, "fixture": "fixtures/../../SKILL.md"}], {}, "leaves evals/fixtures/"),
        (
            [{**BEHAVIOR_CASE, "workspace": WORKSPACE}],
            {},
            "'fixture' is a dependency of 'workspace'",
        ),
    ],
)
def test_rejects_planted_defects(
    write_skill: Callable[[str], Path],
    cases: list[dict[str, Any]],
    top: dict[str, Any],
    expected: str,
) -> None:
    skill = write_skill("group/planner")
    write_cases(skill, cases, **top)
    found = messages(skill)
    assert any(expected in message for message in found), found


def test_reports_unreadable_json(write_skill: Callable[[str], Path]) -> None:
    skill = write_skill("group/planner")
    path = skill / "evals" / "behavior.json"
    path.parent.mkdir(parents=True)
    path.write_text("{", encoding="utf-8")
    assert messages(skill)[0].startswith(": cannot read as JSON")
