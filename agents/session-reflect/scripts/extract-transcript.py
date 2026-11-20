"""Print a compact view of a Claude Code transcript for a lesson sweep.

Keeps every user turn a person typed, with the tail of the assistant text before it, and every denied or blocked
tool call. Drops tool output, compaction summaries, and injected meta turns, which usually cuts a transcript to a
few percent of its size.

Usage: python3 extract-transcript.py <transcript.jsonl>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

USAGE = "usage: python3 extract-transcript.py <transcript.jsonl>"
CONTEXT_CHARS = 600
DENIAL_MARKERS = ("denied", "blocked by", "BLOCKED", "permission to use")


def text_of(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(p for p in parts if p)
    return ""


def tool_result_text(content: object) -> str:
    if not isinstance(content, list):
        return ""
    out = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_result":
            inner = block.get("content")
            out.append(inner if isinstance(inner, str) else text_of(inner))
    return "\n".join(out)


def extract(path: Path) -> None:
    last_assistant = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = rec.get("type")
        msg = rec.get("message") or {}
        if kind == "assistant":
            text = text_of(msg.get("content"))
            if text:
                last_assistant = text
            continue
        if kind != "user" or rec.get("isMeta") or rec.get("isCompactSummary"):
            continue
        content = msg.get("content")
        denial = tool_result_text(content)
        if denial and any(m in denial for m in DENIAL_MARKERS):
            print(f"--- DENIED {rec.get('timestamp', '')}\n{denial[:400]}\n")
            continue
        human = text_of(content).strip()
        if not human or human.startswith("<local-command") or human.startswith("<command-name>/clear"):
            continue
        print(f"=== USER {rec.get('timestamp', '')}")
        if last_assistant:
            print(f"[assistant before] ...{last_assistant[-CONTEXT_CHARS:]}")
        print(f"[user] {human[:4000]}\n")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"extract-transcript: no such file: {path}", file=sys.stderr)
        return 1
    extract(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
