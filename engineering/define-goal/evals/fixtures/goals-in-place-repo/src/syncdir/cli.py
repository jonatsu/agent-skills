"""Command-line entry point for syncdir."""

import argparse
from pathlib import Path

from syncdir.sync import sync


def main() -> None:
    parser = argparse.ArgumentParser(prog="syncdir", description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()
    for path in sync(arguments.source, arguments.destination):
        print(f"copied {path}")


if __name__ == "__main__":
    main()
