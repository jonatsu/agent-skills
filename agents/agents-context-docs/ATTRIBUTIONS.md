# Attributions

- Author: Joonas Onatsu
- License: `Apache-2.0`

This package is a modified version of an Apache-2.0 work under section 4 of that license. Keep `LICENSE.upstream` with
the skill when redistributing it.

## Third-party Sources

### Anthropic — `claude-md-improver` skill

- Source: <https://github.com/anthropics/claude-plugins-official>, `plugins/claude-md-management/skills/claude-md-improver/`
- License: `Apache-2.0`
- Version: `claude-md-management` plugin 1.0.0

Adapted: the evidence discipline, audit workflow, content-quality guidance, and template ideas derive from the
upstream skill, modified into a framework-neutral, unscored workflow.

### Matt Pocock — `writing-for-agents` skill

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/`
- License: `MIT`
- Version: read 2026-08-26

The cache and behavior tests adopt ideas from this source and express them independently. No prose was copied.

### Netresearch DTT GmbH — `agent-rules-skill`

- Source: <https://github.com/netresearch/agent-rules-skill>
- License: `MIT AND CC-BY-SA-4.0`
- Version: read 2026-08-26

No prose was copied due to the content license. Independently expressed ideas cover per-directory adapters,
imperative pointers, generated-content boundaries, and removed-line preservation.

### Denis Shiryaev — `agents-best-practices`

- Source: <https://github.com/DenisSergeevitch/agents-best-practices>, `references/system-prompts-instructions.md` and
  `references/architecture.md`
- License: `MIT`
- Version: read 2026-08-27

No prose was copied. Independently expressed ideas distinguish prompt guidance from code enforcement and identify
prompt patterns that claim authority they do not hold.

### agentydragon — `ducktape` skills `knowledge_hygiene` and `verify_docs`

- Source: <https://github.com/agentydragon/ducktape>, `skills/knowledge_hygiene/` and `skills/verify_docs/`
- License: `AGPL-3.0-only`
- Version: `4ad338af25ea537dc7f817390b2e25c2a7a903f0`

No prose was copied or adapted due to the license. Independently expressed ideas: cost as size times load
frequency, the "true in any repository using the tool" test, self-duplication through file inclusion, tool and field
descriptions as always-loaded text, and a rule repeated for emphasis counting as one rule.

## Upstream License Notice

Copyright Anthropic, PBC.

Licensed under the Apache License, Version 2.0. You may obtain a copy at
<http://www.apache.org/licenses/LICENSE-2.0>. Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied. See `LICENSE.upstream` for the complete terms.
