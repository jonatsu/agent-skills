"""`auditlog` command: print audit events from a JSON Lines file."""

import argparse
import json
import sys
from collections.abc import Iterable, Iterator


def read_events(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Yield one event per nonblank JSON line."""
    for line in lines:
        if line.strip():
            yield json.loads(line)


def main(argv: list[str] | None = None) -> int:
    """Print every event in the file as `timestamp actor action`."""
    parser = argparse.ArgumentParser(prog="auditlog")
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as handle:
        for event in read_events(handle):
            print(f"{event['timestamp']} {event['actor']} {event['action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
