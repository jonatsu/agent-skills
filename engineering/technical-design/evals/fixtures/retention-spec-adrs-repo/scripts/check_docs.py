"""Check that relative Markdown links resolve and that each ADR states its status."""

import re
import sys
from pathlib import Path

LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def check(root: Path) -> list[str]:
    problems = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            if "://" in target:
                continue
            if not (path.parent / target).exists():
                problems.append(f"{path}: broken link {target}")
        if path.parent.name == "adr" and not re.search(r"^Status: ", text, re.MULTILINE):
            problems.append(f"{path}: no Status line")
    return problems


def main(directory: str) -> int:
    problems = check(Path(directory))
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
