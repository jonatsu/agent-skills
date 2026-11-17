"""Command-line entry point for `catalog-validate`."""

import sys


def main(argv: list[str] | None = None) -> int:
    """Validate a catalog file. Not implemented yet."""
    args = sys.argv[1:] if argv is None else argv
    print(f"catalog-validate: not implemented ({len(args)} argument(s) ignored)", file=sys.stderr)
    return 3
