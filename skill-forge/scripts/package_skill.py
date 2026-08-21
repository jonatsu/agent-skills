#!/usr/bin/env python3
"""Package a skill folder into a distributable .skill file."""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path).resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        print(f"Error: invalid skill path: {skill_path}")
        return None
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return None
    print("Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"Validation failed: {message}")
        return None
    print(message)
    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)
    skill_filename = output_path / f"{skill_path.name}.skill"
    with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob("*"):
            if (
                file_path.is_file()
                and "__pycache__" not in file_path.parts
                and file_path.suffix != ".pyc"
            ):
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
    print(f"Packaged skill to: {skill_filename}")
    return skill_filename


def main():
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <path/to/skill-folder> [output-directory]")
        sys.exit(1)
    result = package_skill(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
