"""Validate this fixture's flat integer configuration against its JSON schema."""

import json
import sys
from pathlib import Path
from typing import Any


def load_defaults(path: Path) -> dict[str, int]:
    """Load the fixture's flat key and integer-value YAML subset."""
    defaults: dict[str, int] = {}
    for line_number, raw_line in enumerate(path.read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, raw_value = line.partition(":")
        if not separator or not key.strip() or not raw_value.strip():
            raise ValueError(f"{path}:{line_number}: expected 'key: integer'")
        try:
            defaults[key.strip()] = int(raw_value.strip())
        except ValueError as error:
            raise ValueError(
                f"{path}:{line_number}: value must be an integer"
            ) from error
    return defaults


def validate(defaults: dict[str, int], schema: dict[str, Any]) -> list[str]:
    """Return every schema violation relevant to the fixture."""
    errors: list[str] = []
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for key in required:
        if key not in defaults:
            errors.append(f"missing required setting: {key}")

    if schema.get("additionalProperties") is False:
        for key in defaults.keys() - properties.keys():
            errors.append(f"unknown setting: {key}")

    for key, value in defaults.items():
        rule = properties.get(key)
        if not isinstance(rule, dict):
            continue
        if rule.get("type") == "integer" and not isinstance(value, int):
            errors.append(f"{key} must be an integer")
        minimum = rule.get("minimum")
        if isinstance(minimum, int) and value < minimum:
            errors.append(f"{key} must be at least {minimum}")

    return errors


def main() -> int:
    """Validate paths supplied by the fixture's Just recipe."""
    if len(sys.argv) != 3:
        print("usage: check_config.py DEFAULTS SCHEMA", file=sys.stderr)
        return 2

    defaults_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2])
    try:
        defaults = load_defaults(defaults_path)
        schema = json.loads(schema_path.read_text())
        errors = validate(defaults, schema)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1

    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
