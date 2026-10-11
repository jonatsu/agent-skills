# Attributions

- Author: Joonas Onatsu
- License: `CC-BY-SA-4.0`

The package adapts upstream material licensed `CC-BY-SA-4.0`, which requires attribution, an indication that the
material was changed, and the same license for adaptations. Keep `LICENSE.upstream` with the skill.

## Third-party Sources

### William Tan, Trail of Bits: `modern-python` skill

- Source: <https://github.com/trailofbits/skills>, `plugins/modern-python/skills/modern-python`
- License: `CC-BY-SA-4.0`
- Version: `d3323cefbcf645678b8dc481de204b02ad3d02dc`

Adapted: the package's structure comes from this skill, itself derived from
<https://github.com/trailofbits/cookiecutter-python>, including its task-based routing, `pyproject.toml` layout, uv
command reference, and migration checklist.

### Integralist: Python rules in `agent-skills`

- Source: <https://github.com/Integralist/agent-skills>, `.claude/rules/python.md`
- License: `LicenseRef-No-License`
- Version: `07155927c4a44cf97b050ea4f728fce840822ce9`

The repository declares no license for these rules, so all rights remain with its author. It informed the focused
Ruff baseline and the code-specific lint suppressions. Nothing was copied.

### Tim Vink: `httpx2.md` rule in `dotfiles`

- Source: <https://github.com/timvink/dotfiles>, `dot_claude/rules/httpx2.md`
- License: `LicenseRef-No-License`
- Version: read on or before 2026-09-06

The repository declares no license for this rule, so all rights remain with its author. The rule influenced the
preference for Pydantic's `httpx2` as the HTTP client for new code. Nothing was copied.
