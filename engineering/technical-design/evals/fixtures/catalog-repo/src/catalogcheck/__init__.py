"""Check product catalog files before they are published."""

import argparse
from collections.abc import Sequence

__version__ = "0.1.0"


def main(argv: Sequence[str] | None = None) -> int:
    """Parse the command line and return the process exit status."""
    parser = argparse.ArgumentParser(prog="catalogcheck")
    parser.add_argument("path", help="catalog file to check")
    parser.parse_args(argv)
    return 0
