# Attributions

## Current skill

- Skill: `claude-automation-recommender`
- Current author: Joonas Onatsu
- Current license: Apache License 2.0 (inherited from upstream; not relicensed)
- Status: adapted from upstream and materially modified

## Original authors and source

- Original author: Anthropic
- Upstream project: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Upstream plugin: `claude-code-setup` version 1.0.0
- Source path: `plugins/claude-code-setup/skills/claude-automation-recommender/`
- Source commit: `a5c7fb5d86a4cd34c4f47819658654c3d8f08dda`

## Adaptation note

This version is derived from the upstream `claude-automation-recommender` skill
shipped in the `claude-code-setup` plugin, and has been modified for this
repository. The upstream plugin is no longer installed here; this copy replaces
it.

Material changes, in the order they matter:

- **Added Phase 0, an inventory pass.** Upstream listed `.claude/` and `CLAUDE.md`
  in Phase 1 and then never used the result, so a configured setup received
  recommendations for automations it already ran. Phase 0 now reads project and
  user settings, `.mcp.json`, `claude mcp list`, and `claude plugin list`, and
  Phase 2 subtracts what it finds. "Already covered" is now a valid answer
  instead of a quota to fill.
- **Fixed the frontmatter key.** Upstream declared `tools:`, which is *agent*
  frontmatter and is ignored on a skill — so a skill documented as read-only ran
  with Edit and Write in scope. Now `allowed-tools:`, extended with WebSearch and
  WebFetch, which the body instructs the agent to use three times but upstream
  never granted.
- **Removed the hardcoded context7 recommendation.** Replaced with a
  provider-neutral docs-lookup category that recommends a self-hosted indexer
  first, and requires any hosted server to be flagged for external data flow and
  credentials.
- **Corrected every emitted command.** `claude mcp add context7` is not runnable
  (the transport form is required); `/plugin install`, `/plugin list`, and
  `/plugin info` are not the install contract (`claude plugin marketplace add`
  first, then `plugin@marketplace`, and `details` rather than the nonexistent
  `info`). Verified against `claude mcp add --help` and `claude plugin --help`.
- **Filled in the hooks reference.** Upstream's `hooks-patterns.md` carried
  detection tables but no hook JSON for formatting, linting, type-checking,
  tests, or file protection, and no explanation of the hook contract — so
  "auto-format on edit" was left to be implemented as `prettier --write .`. Added
  runnable configurations, the stdin/exit-code/matcher contract, a latency cost
  model, and non-macOS notification commands. The protection and formatting hook
  bodies were executed against sample payloads before being documented.
- **Added the missing agent template** to `subagent-templates.md`, which
  previously contained no template, plus the `tools` versus `allowed-tools`
  distinction.
- **Fixed the broken fence nesting** in the Phase 3 output template, which
  terminated early and truncated the template the model reads.
- **Removed filler and cosmetic defects**: the duplicated hooks quick-reference
  table, the "Observtic" heading, the single-row `$ARGUMENTS` table, and the
  generic Memory MCP recommendation.
- **Restructured to this repository's skill conventions**: Iron Law, trackable
  workflow checklist with blocking markers, anti-pattern list, and pre-delivery
  checklist.

## Upstream license

The upstream source is used under the Apache License, Version 2.0. A verbatim
copy is kept alongside this file as `LICENSE.upstream`.

As required by section 4 of that license, this is a modified version; the
changes are listed above. Keep this file and `LICENSE.upstream` with the skill
when redistributing.

Copyright Anthropic, PBC.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at <http://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
