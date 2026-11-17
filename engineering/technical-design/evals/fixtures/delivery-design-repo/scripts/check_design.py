"""Fail when a design document's second-level headings differ from the required layout."""

import sys
from pathlib import Path

REQUIRED = ["Purpose", "Current behavior", "Proposed behavior", "Decisions", "Open questions"]


def headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def main(directory: str) -> int:
    failures = 0
    for path in sorted(Path(directory).glob("*.md")):
        found = headings(path.read_text(encoding="utf-8"))
        if found != REQUIRED:
            print(f"{path}: expected {REQUIRED}, found {found}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
