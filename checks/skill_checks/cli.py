"""Read-only checks for this repository's skill packages."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from skill_checks.catalog import (
    InvalidSkillDirectories,
    SkillCatalogError,
    discover_skill_sources,
    find_skill_source,
)
from skill_checks.descriptions import check_descriptions, format_description_report
from skill_checks.identity import IdentityError, wrong_identities
from skill_checks.names import duplicate_names
from skill_checks.outside_references import check_packages
from skill_checks.validators import (
    ValidationReport,
    ValidatorKind,
    format_validation_report,
    run_validator,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the command parser without inspecting the repository."""
    parser = argparse.ArgumentParser(prog="skill-checks", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("spec", "policy"):
        validator = commands.add_parser(command, help=f"run the {command} validator")
        validator.add_argument("skill_directories", nargs="*", type=Path)
    validate = commands.add_parser("validate", help="run specification then policy validation")
    validate.add_argument("skill_directory", type=Path)
    commands.add_parser("descriptions", help="check description form and length")
    commands.add_parser("names", help="fail when two deployable skills share a name")
    commands.add_parser("references", help="fail on a reference out of a skill package")
    commands.add_parser("identity", help="fail unless Git would commit as the noreply address")
    locate = commands.add_parser("locate", help="print one skill's directory by name")
    locate.add_argument("name")
    return parser


def find_repository_root() -> Path:
    """Return the Git root of the current directory.

    Raises:
        SkillCatalogError: If the current directory is not inside a Git checkout.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise SkillCatalogError(f"cannot find repository root: {result.stderr.strip()}")
    return Path(result.stdout.strip()).resolve()


def main(argv: Sequence[str] | None = None) -> int:
    """Run the selected check; 0 passes, 1 reports findings, 2 means the check could not run."""
    arguments = build_parser().parse_args(argv)
    if arguments.command == "identity":
        return _run_identity()
    try:
        root = find_repository_root()
    except SkillCatalogError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    if arguments.command in {"spec", "policy"}:
        kind = ValidatorKind(arguments.command)
        return _run_validator(kind, tuple(arguments.skill_directories), root)
    if arguments.command == "validate":
        statuses = [
            _run_validator(kind, (arguments.skill_directory,), root)
            for kind in (ValidatorKind.SPECIFICATION, ValidatorKind.POLICY)
        ]
        return 0 if statuses == [0, 0] else 1
    if arguments.command == "descriptions":
        return _run_descriptions(root)
    if arguments.command == "names":
        return _run_names(root)
    if arguments.command == "references":
        return _run_references(root)
    if arguments.command == "locate":
        return _run_locate(root, arguments.name)
    raise AssertionError(f"unhandled command: {arguments.command}")


def _run_validator(kind: ValidatorKind, named: tuple[Path, ...], root: Path) -> int:
    try:
        sources = discover_skill_sources(root, named, working_directory=Path.cwd())
    except InvalidSkillDirectories as error:
        for skill_md in error.missing_skill_files:
            print(f"FAIL  not a skill directory: {skill_md.parent}", file=sys.stderr)
        return 2
    except SkillCatalogError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    report = run_validator(kind, sources, root)
    stdout, stderr = format_validation_report(report, root)
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return _validator_status(report)


def _validator_status(report: ValidationReport) -> int:
    if report.fatal_error is not None:
        return 2
    return 1 if report.failures else 0


def _run_descriptions(root: Path) -> int:
    try:
        sources = discover_skill_sources(root)
    except SkillCatalogError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    report = check_descriptions(sources)
    sys.stdout.write(format_description_report(report, root))
    return 1 if report.failures else 0


def _run_names(root: Path) -> int:
    try:
        sources = discover_skill_sources(root)
    except SkillCatalogError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    duplicates = duplicate_names(sources)
    for name, directories in duplicates.items():
        locations = ", ".join(str(directory.relative_to(root)) for directory in directories)
        print(f"FAIL  {name} is used by {locations}")
    print(f"names: {len(sources)} skill(s) checked, {len(duplicates)} duplicate name(s)")
    return 1 if duplicates else 0


def _run_references(root: Path) -> int:
    violations = check_packages((root,))
    for violation in violations:
        location = f"{violation.path.relative_to(root)}:{violation.line}"
        print(f"FAIL  {location}: {violation.reason}: {violation.reference}")
    print(f"references: {len(violations)} reference(s) out of their package")
    return 1 if violations else 0


def _run_identity() -> int:
    try:
        problems = wrong_identities()
    except IdentityError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    for problem in problems:
        print(f"FAIL  {problem}", file=sys.stderr)
    if problems:
        print("      set it with: git config user.email <the noreply address>", file=sys.stderr)
    return 1 if problems else 0


def _run_locate(root: Path, name: str) -> int:
    try:
        source = find_skill_source(root, name)
    except SkillCatalogError as error:
        print(f"skill-checks: {error}", file=sys.stderr)
        return 2
    print(source.directory)
    return 0


if __name__ == "__main__":
    sys.exit(main())
