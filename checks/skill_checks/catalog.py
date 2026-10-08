"""Discover this repository's skill packages without applying check-specific policy."""

import stat
from collections.abc import Iterable
from pathlib import Path

import attrs

SKILL_FILE_NAME = "SKILL.md"
# Top-level directories that hold no deployable skill: archived packages, the script tests, this tooling, and
# version-control or environment state.
EXCLUDED_TOP_LEVEL = frozenset({"archived", "tests", "checks", ".git", ".venv", ".github"})


class SkillCatalogError(Exception):
    """The requested skill catalog is unusable."""


class InvalidSkillDirectories(SkillCatalogError):
    """One or more explicitly named paths do not contain SKILL.md."""

    def __init__(self, missing_skill_files: tuple[Path, ...]) -> None:
        self.missing_skill_files = missing_skill_files
        super().__init__("one or more paths are not skill directories")


@attrs.frozen
class SkillSource:
    """One skill directory and its required entrypoint."""

    directory: Path
    skill_md: Path


def discover_skill_sources(
    repo_root: Path,
    named_directories: Iterable[Path] = (),
    *,
    working_directory: Path | None = None,
) -> tuple[SkillSource, ...]:
    """Return named or default-discovered skills in deterministic path order.

    Default discovery covers every deployable group: `<domain>/`, `lazy/<domain>/` at any depth, and
    `claude/`. Explicit names bypass the exclusions and resolve from the caller's working directory.

    Raises:
        SkillCatalogError: If a named directory is invalid or default discovery is empty.
    """
    root = repo_root.resolve()
    named = tuple(named_directories)
    if named:
        base = (working_directory or Path.cwd()).resolve()
        sources: list[SkillSource] = []
        invalid: list[Path] = []
        for raw_directory in named:
            directory = raw_directory if raw_directory.is_absolute() else base / raw_directory
            skill_md = directory / SKILL_FILE_NAME
            if not skill_md.is_file():
                invalid.append(skill_md)
                continue
            sources.append(SkillSource(directory.resolve(), skill_md.resolve()))
        if invalid:
            raise InvalidSkillDirectories(tuple(invalid))
        return tuple(sorted(sources, key=lambda source: str(source.directory)))

    discovered = tuple(
        SkillSource(skill_md.parent.resolve(), skill_md.resolve())
        for skill_md in sorted(root.rglob(SKILL_FILE_NAME), key=str)
        if _is_default_skill(skill_md, root)
    )
    if not discovered:
        raise SkillCatalogError(f"no {SKILL_FILE_NAME} found under {root}")
    return discovered


def find_skill_source(repo_root: Path, name: str) -> SkillSource:
    """Return the one default-discovered skill directory named `name`.

    Every caller that needs a skill's location resolves it here instead of hardcoding a domain path, so
    moving a skill between domains never breaks a caller keyed by name.

    Raises:
        SkillCatalogError: when no skill or more than one skill has this name.
    """
    try:
        sources = discover_skill_sources(repo_root)
    except SkillCatalogError as error:
        raise SkillCatalogError(f"no skill named {name!r}: {error}") from error
    matches = tuple(source for source in sources if source.directory.name == name)
    if not matches:
        raise SkillCatalogError(f"no skill named {name!r} found under {repo_root}")
    if len(matches) > 1:
        locations = ", ".join(str(source.directory) for source in matches)
        raise SkillCatalogError(f"skill name {name!r} is ambiguous: {locations}")
    return matches[0]


def _is_default_exclusion(relative_path: Path) -> bool:
    parts = relative_path.parts
    if parts and parts[0] in EXCLUDED_TOP_LEVEL:
        return True
    return any(parts[index : index + 2] == ("evals", "fixtures") for index in range(len(parts) - 1))


def _is_default_skill(skill_md: Path, root: Path) -> bool:
    try:
        mode = skill_md.lstat().st_mode
    except OSError:
        return False
    if not stat.S_ISREG(mode):
        return False
    try:
        relative = skill_md.resolve().relative_to(root)
    except ValueError:
        return False
    return not _is_default_exclusion(relative)
