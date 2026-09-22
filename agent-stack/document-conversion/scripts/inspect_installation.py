#!/usr/bin/env python3
"""Report which document converters are usable, without loading plugins or using network.

Covers both converters this skill routes between: anydoc, an external CLI, and MarkItDown,
a Python package. Runs with neither installed and reports that rather than failing to start.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
from importlib.metadata import (
    PackageNotFoundError,
    entry_points,
    metadata,
    version,
)
from typing import Any

ANYDOC_TARGET_VERSION = "0.2.4"
MARKITDOWN_TARGET_VERSION = "0.1.7"

# Seconds to wait for `anydoc --version`. Generous for a local binary, but bounded:
# the fallback path resolves through npx, which can reach the network on a cold cache.
ANYDOC_VERSION_TIMEOUT = 30.0

OPTIONAL_DISTRIBUTIONS = (
    "markitdown-ocr",
    "markitdown-mcp",
    "firecrawl-anydoc",
    "openai",
    "azure-ai-documentintelligence",
    "azure-ai-contentunderstanding",
)


def distribution_version(name: str) -> str | None:
    """Return an installed distribution version without importing it."""
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def inspect_anydoc() -> dict[str, Any]:
    """Collect anydoc's executable path and reported version.

    Returns:
        A report with the resolved executable path, the version string anydoc printed,
        and an error description when the executable is absent or did not run. The npx
        fallback is reported but never invoked, because invoking it downloads a package.
    """
    executable = shutil.which("anydoc")
    if executable is None:
        return {
            "version": None,
            "executable": None,
            "npx_fallback": shutil.which("npx"),
            "error": "anydoc is not on PATH",
        }

    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell, bounded wait
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=ANYDOC_VERSION_TIMEOUT,
            check=False,
        )
    except OSError as exc:  # Report launch failures without hiding the cause.
        return {
            "version": None,
            "executable": executable,
            "npx_fallback": shutil.which("npx"),
            "error": f"{type(exc).__name__}: {exc}",
        }
    except subprocess.TimeoutExpired:
        return {
            "version": None,
            "executable": executable,
            "npx_fallback": shutil.which("npx"),
            "error": f"timed out after {ANYDOC_VERSION_TIMEOUT:g}s",
        }

    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit {completed.returncode}"
        return {
            "version": None,
            "executable": executable,
            "npx_fallback": shutil.which("npx"),
            "error": detail,
        }

    return {
        "version": completed.stdout.strip() or None,
        "executable": executable,
        "npx_fallback": shutil.which("npx"),
        "error": None,
    }


def inspect_markitdown() -> dict[str, Any]:
    """Collect MarkItDown's version, declared extras, and import health."""
    try:
        installed_version = version("markitdown")
        package_metadata = metadata("markitdown")
        extras = sorted(set(package_metadata.get_all("Provides-Extra") or []))
        import_error = None
        try:
            from markitdown import MarkItDown  # noqa: F401
        except Exception as exc:  # Report import health without hiding details.
            import_error = f"{type(exc).__name__}: {exc}"
    except PackageNotFoundError:
        installed_version = None
        extras = []
        import_error = "PackageNotFoundError: markitdown is not installed"

    return {
        "version": installed_version,
        "import_error": import_error,
        "declared_extras": extras,
    }


def discover_plugins() -> list[dict[str, Any]]:
    """List MarkItDown plugin entry points without importing any of them."""
    return sorted(
        (
            {
                "name": point.name,
                "module": point.value,
                "distribution": (
                    point.dist.name if getattr(point, "dist", None) is not None else None
                ),
            }
            for point in entry_points(group="markitdown.plugin")
        ),
        key=lambda item: (item["name"], item["module"]),
    )


def inspect_installation() -> dict[str, Any]:
    """Collect converter, extra, plugin, and executable metadata."""
    return {
        "target_versions": {
            "anydoc": ANYDOC_TARGET_VERSION,
            "markitdown": MARKITDOWN_TARGET_VERSION,
        },
        "python": platform.python_version(),
        "anydoc": inspect_anydoc(),
        "markitdown": inspect_markitdown(),
        "optional_distributions": {
            name: distribution_version(name) for name in OPTIONAL_DISTRIBUTIONS
        },
        "plugins": discover_plugins(),
        "executables": {
            "anydoc": shutil.which("anydoc"),
            "npx": shutil.which("npx"),
            "markitdown": shutil.which("markitdown"),
            "markitdown-mcp": shutil.which("markitdown-mcp"),
            "exiftool": shutil.which("exiftool"),
            "ffmpeg": shutil.which("ffmpeg"),
        },
    }


def print_human_readable(report: dict[str, Any]) -> None:
    """Write the report to stdout in the form a person reads first."""
    targets = report["target_versions"]
    anydoc = report["anydoc"]
    markitdown = report["markitdown"]

    print(f"Python: {report['python']}")

    print(f"anydoc: {anydoc['version'] or 'not usable'} (skill target: {targets['anydoc']})")
    if anydoc["error"]:
        print(f"  {anydoc['error']}")
        if anydoc["npx_fallback"]:
            print("  npx is available: `npx -y @firecrawl/anydoc` can stand in")

    print(
        "MarkItDown: "
        f"{markitdown['version'] or 'not installed'} "
        f"(skill target: {targets['markitdown']})"
    )
    print(f"  import health: {markitdown['import_error'] or 'OK'}")

    extras = markitdown["declared_extras"]
    print(f"  declared extras: {', '.join(extras) if extras else 'unavailable'}")

    print("Optional distributions:")
    for name, installed_version in report["optional_distributions"].items():
        print(f"  {name}: {installed_version or 'not installed'}")

    print("Discovered plugins (not loaded):")
    if report["plugins"]:
        for plugin in report["plugins"]:
            distribution = plugin["distribution"] or "unknown distribution"
            print(f"  {plugin['name']}: {plugin['module']} ({distribution})")
    else:
        print("  none")

    print("Executables:")
    for name, path in report["executables"].items():
        print(f"  {name}: {path or 'not found'}")


def usable_converters(report: dict[str, Any]) -> list[str]:
    """Name the converters this machine can actually run right now."""
    usable = []
    if report["anydoc"]["error"] is None:
        usable.append("anydoc")
    if report["markitdown"]["import_error"] is None:
        usable.append("markitdown")
    return usable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Report anydoc and MarkItDown versions, extras, plugin entry points, and "
            "optional executables without loading plugins."
        )
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON",
    )
    parser.add_argument(
        "--allow-version-mismatch",
        action="store_true",
        help="Exit successfully when an installed converter differs from the skill target",
    )
    return parser


def main() -> int:
    """Report the installation and exit nonzero when no converter is usable.

    A missing converter is not itself a failure: this skill routes between two, and
    either one alone satisfies most of its job. The version gate applies only to a
    converter that is actually installed.
    """
    args = build_parser().parse_args()
    report = inspect_installation()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_human_readable(report)

    usable = usable_converters(report)
    if not usable:
        print("No usable converter: install anydoc or MarkItDown.")
        return 1

    if args.allow_version_mismatch:
        return 0

    targets = report["target_versions"]
    mismatched = [name for name in usable if report[name]["version"] not in (None, targets[name])]
    if mismatched:
        print(
            f"Version mismatch for {', '.join(mismatched)}; "
            "pass --allow-version-mismatch to accept it."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
