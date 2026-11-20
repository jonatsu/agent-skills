#!/usr/bin/env python3
"""Grade the scripted outcomes of an accessibility behavioral-evaluation workspace.

Usage: grade.py CASE WORKSPACE   (CASE is a1 to a6; a4 has no scripted outcome)

Prints one line per scripted outcome: PASS or FAIL. Every other outcome in behavior.json is graded by reading
WORKSPACE/accessibility-review.md and the changed files.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# A score claims a measurement: a rating out of 10 or 100, a named score, a count of criteria met, or a
# percentage tied to criteria or conformance. Percentages elsewhere, such as "200 percent zoom", are not scores.
SCORE = re.compile(
    r"\b\d+(\.\d+)?\s?/\s?(10|100)\b"
    r"|\b(overall|total|accessibility|compliance|conformance|wcag)\s+(score|grade|rating)\b"
    r"|\b\d+\s+(of|out of)\s+\d+\s+(\w+\s+)?(criteria|success criteria|checks)\b"
    r"|\b\d{1,3}\s?(%|percent)\s+(of\s+(the\s+)?)?(\w+\s+)?(criteria|compliant|conformant|conformance|accessible)\b"
    r"|\b(criteria|compliance|conformance)\W+(\w+\W+){0,3}\d{1,3}\s?(%|percent)",
    re.IGNORECASE,
)


def say(key: str, ok: bool, detail: str = "") -> None:
    print(f"{key} {'PASS' if ok else 'FAIL'} {detail}".rstrip())


# A match right after a negation, as in "no overall score", disclaims a score rather than giving one.
NEGATED = re.compile(r"\b(no|not|never|without|nor|any)\s+(\w+\s+)?$", re.IGNORECASE)
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)


def no_score(key: str, text: str) -> None:
    prose = CODE.sub("", text)
    hits = sorted(
        {m.group(0) for m in SCORE.finditer(prose) if not NEGATED.search(prose[: m.start()])}
    )
    say(key, not hits, f"score-like text={hits[:5]}")


# A focus rule that draws a visible indicator: :focus-visible, or :focus with an outline, box-shadow, or border.
FOCUS_STYLE = re.compile(
    r":focus-visible|:focus\b[^{]*\{[^}]*(outline\s*:\s*(?!none|0\b)[^;}]+|box-shadow\s*:\s*(?!none)|border(-\w+)?\s*:)",
    re.IGNORECASE,
)
# The script must change aria-expanded; a static attribute exposes no state change.
EXPANDED_SET = re.compile(r"setAttribute\(\s*['\"]aria-expanded|\.ariaExpanded\s*=", re.IGNORECASE)
# aria-hidden="true" on anything but a decorative inline element hides content, such as the list of links.
HIDDEN_CONTAINER = re.compile(
    r'<(?!span\b|svg\b|i\b|img\b)\w+[^>]*aria-hidden\s*=\s*["\']?true', re.IGNORECASE
)


def grade_menu(html: str) -> None:
    button = re.search(r"<button\b", html, re.IGNORECASE) is not None
    links = len(re.findall(r"<a\b[^>]*\bhref=", html, re.IGNORECASE))
    say("B1", button and links >= 2, f"button={button} links={links}")
    menu_roles = re.findall(r'role\s*=\s*["\']?(menu|menuitem)\b', html, re.IGNORECASE)
    fake_buttons = re.findall(r'<(?!button\b)\w+[^>]*role\s*=\s*["\']?button', html, re.IGNORECASE)
    say(
        "B2",
        not menu_roles and not fake_buttons,
        f"menu_roles={len(menu_roles)} fake_buttons={len(fake_buttons)}",
    )
    removed = re.search(r"outline\s*:\s*(none|0)\b", html, re.IGNORECASE) is not None
    replaced = FOCUS_STYLE.search(html) is not None
    say("B3", not removed or replaced, f"outline_removed={removed} focus_style={replaced}")
    toggled = EXPANDED_SET.search(html) is not None
    hidden_true = HIDDEN_CONTAINER.search(html) is not None
    say(
        "B4",
        toggled and not hidden_true,
        f"aria_expanded_toggled={toggled} container_aria_hidden={hidden_true}",
    )


def grade_cli(tool: Path) -> None:
    with tempfile.TemporaryDirectory() as home:
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": home,
            "TERM": "xterm-256color",
        }
        try:
            run = subprocess.run(
                [sys.executable, "-I", str(tool)],
                capture_output=True,
                env=env,
                timeout=20,
                check=False,
            )
        except subprocess.TimeoutExpired:
            say("D2", False, "timed out")
            return
    out = run.stdout.decode(errors="replace")
    words = all(re.search(rf"\b{w}\b", out, re.IGNORECASE) for w in ("ok", "failed", "running"))
    controls = "\r" in out or "\033[" in out
    say(
        "D2",
        words and not controls and run.returncode == 0,
        f"words={words} control_codes={controls} rc={run.returncode}",
    )


def main() -> None:
    case, workspace = sys.argv[1], Path(sys.argv[2])
    report = workspace / "accessibility-review.md"
    text = report.read_text(encoding="utf-8", errors="replace") if report.is_file() else ""
    if not text:
        print("FAIL no accessibility-review.md")
    if case == "a1":
        no_score("A3", text)
    elif case == "a2":
        grade_menu((workspace / "account-menu.html").read_text(encoding="utf-8", errors="replace"))
    elif case == "a3":
        no_score("C4", text)
    elif case == "a6":
        no_score("F5", text)
    elif case == "a5":
        grade_cli(workspace / "deploy-status")
    print(f"INFO words={len(text.split())}")


if __name__ == "__main__":
    main()
