# Attributions

## Current Skill

- Skill: `agents-management`
- Current author and adapter: Joonas Onatsu
- Current license: Apache License 2.0, inherited from upstream
- Status: substantially modified and merged from one upstream-derived skill and one original skill

Keep this file and `LICENSE.upstream` with the skill when redistributing it. The upstream repository supplied no `NOTICE`
file when checked on 2026-08-26.

## Composition

| Predecessor | Origin | Contribution |
|---|---|---|
| `claude-md-auditor` | Anthropic upstream, Apache-2.0 | Evidence discipline, audit workflow, content-quality guidance, and templates |
| `agent-repo-docs` | Joonas Onatsu, MIT | Repository-fact verification, initialization, `llms.txt`, and the `AGENTS.md` asset |

The author of `agent-repo-docs` contributed that work to this merged Apache-2.0 package.

## Upstream Source

- Original author: Anthropic
- Project: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Plugin and version: `claude-md-management` 1.0.0
- Source path: `plugins/claude-md-management/skills/claude-md-improver/`
- Upstream skill name: `claude-md-improver`

This package is a modified version under section 4 of Apache-2.0. The current package replaces the upstream
Claude-specific score-and-edit workflow with framework-neutral initialization, maintenance, migration, and qualitative
audit branches. It adds capability discovery and known-client loading adapters, removes aggregate scoring, verifies
repository claims before using them, preserves divergent real files for user reconciliation, and separates guidance from
deterministic enforcement.

## File Provenance

| File | Relationship to upstream |
|---|---|
| `SKILL.md` | Rewritten as the shared scope, router, invariants, and completion contract |
| `references/initialize.md` | Original initialization workflow |
| `references/maintain.md` | Rewritten from the earlier update workflow and original preservation guidance |
| `references/audit.md` | Rebuilt from upstream quality criteria as evidence-based judgments without scores |
| `references/loading-model.md` | Original capability model and client adapters |
| `references/templates.md` | Substantially reduced and reshaped from upstream section ideas |
| `assets/AGENTS.template.md`, `assets/llms.template.txt` | Original `agent-repo-docs` assets |

## Other Sources

### mattpocock/skills: `writing-for-agents`

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/`
- License: MIT, Copyright (c) 2026 Matt Pocock
- Read 2026-08-26

The cache and behavior tests adopt ideas from this source and express them independently. No prose was copied.

### netresearch/agent-rules-skill

- Source: <https://github.com/netresearch/agent-rules-skill>
- License: MIT for code and CC-BY-SA-4.0 for content, Copyright Netresearch DTT GmbH, 2025-2026
- Read 2026-08-26

No prose was copied because the content license conflicts with this package's license obligations. Independently expressed
ideas cover per-directory adapters, imperative pointers, generated-content boundaries, and removed-line preservation.

### DenisSergeevitch/agents-best-practices

- Source: <https://github.com/DenisSergeevitch/agents-best-practices>
- Files: `references/system-prompts-instructions.md` and `references/architecture.md`
- License: MIT, Copyright (c) 2026 Denis Shiryaev
- Read 2026-08-27

No prose was copied. Independently expressed ideas distinguish prompt guidance from code enforcement and identify prompt
patterns that claim authority they do not hold.

## Upstream License Notice

Copyright Anthropic, PBC.

Licensed under the Apache License, Version 2.0. You may obtain a copy at <http://www.apache.org/licenses/LICENSE-2.0>.
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See `LICENSE.upstream` for the
complete terms.
