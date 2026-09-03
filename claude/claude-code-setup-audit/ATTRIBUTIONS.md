# Attributions

## Current skill

- Skill: `claude-code-setup-audit`, renamed from `claude-automation-recommender` on 2026-09-03
- Current author: Joonas Onatsu
- Current license: Apache License 2.0 (inherited from upstream; not relicensed)
- Status: adapted from upstream and materially modified

The rename is deliberate and not a claim of separate origin. "Recommender" named the output while hiding the
discipline that makes the output trustworthy — the skill's defining behavior is inventorying an existing
configuration and subtracting it, with "already covered" as a valid result. The new name resembles the
upstream *plugin* name `claude-code-setup` because both describe the same subject; this remains a skill, and
"audit" is what distinguishes it.

## Original authors and source

- Original author: Anthropic
- Upstream project:
  [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Upstream plugin: `claude-code-setup` version 1.0.0
- Source path: `plugins/claude-code-setup/skills/claude-automation-recommender/`
- Source commit: `a5c7fb5d86a4cd34c4f47819658654c3d8f08dda`

## Adaptation note

This skill is derived from the upstream `claude-automation-recommender` skill shipped in the
`claude-code-setup` plugin, and has been modified for this repository. The upstream plugin is no longer
installed here; this copy replaces it.

Material changes, in the order they matter:

- **Added Phase 0, an inventory pass.** Upstream listed `.claude/` and `CLAUDE.md` in Phase 1 and then never
  used the result, so a configured setup received recommendations for automations it already ran. Phase 0 now
  reads project and user settings, `.mcp.json`, `claude mcp list`, and `claude plugin list`, and Phase 2
  subtracts what it finds. "Already covered" is now a valid answer instead of a quota to fill.
- **Fixed the frontmatter key.** Upstream declared `tools:`, which is *agent* frontmatter and is ignored on a
  skill — so a skill documented as read-only ran with Edit and Write in scope. Now `allowed-tools:`, extended
  with WebSearch and WebFetch, which the body instructs the agent to use three times but upstream never
  granted.
- **Removed the hardcoded context7 recommendation.** Replaced with a provider-neutral docs-lookup category
  that recommends a self-hosted indexer first, and requires any hosted server to be flagged for external data
  flow and credentials.
- **Corrected every emitted command.** `claude mcp add context7` is not runnable (the transport form is
  required); `/plugin install`, `/plugin list`, and `/plugin info` are not the install contract
  (`claude plugin marketplace add` first, then `plugin@marketplace`, and `details` rather than the nonexistent
  `info`). Verified against `claude mcp add --help` and `claude plugin --help`.
- **Filled in the hooks reference.** Upstream's `hooks-patterns.md` carried detection tables but no hook JSON
  for formatting, linting, type-checking, tests, or file protection, and no explanation of the hook contract —
  so "auto-format on edit" was left to be implemented as `prettier --write .`. Added runnable configurations,
  the stdin/exit-code/matcher contract, a latency cost model, and non-macOS notification commands. The
  protection and formatting hook bodies were executed against sample payloads before being documented.
- **Added the missing agent template** to `subagent-templates.md`, which previously contained no template,
  plus the `tools` versus `allowed-tools` distinction.
- **Fixed the broken fence nesting** in the Phase 3 output template, which terminated early and truncated the
  template the model reads.
- **Removed filler and cosmetic defects**: the duplicated hooks quick-reference table, the "Observtic"
  heading, the single-row `$ARGUMENTS` table, and the generic Memory MCP recommendation.
- **Restructured to this repository's skill conventions**: Iron Law, trackable workflow checklist with
  blocking markers, anti-pattern list, and pre-delivery checklist.

Further changes on 2026-09-03, following a `skill-review` pass:

- **Replaced the frozen catalogues with live discovery.** The plugin and MCP-server lists named third-party
  artifacts on other projects' release schedules, and nothing in this repository could detect them going
  stale. `plugins-reference.md` now names no plugin at all and teaches enumeration instead; `mcp-servers.md`
  keeps the data-flow doctrine, the exclusions, and the non-obvious detection signals, and drops the
  twenty per-vendor entries whose content was the vendor's name. Upstream's plugin table sampled four of the
  thirty-nine plugins the official marketplace held on that date, with no stated criterion for the four.
- **Corrected three factual errors.** `subagent-templates.md` marked `model` and `color` as required agent
  frontmatter; `color` is not, verified against six working agents that all omit it. `SKILL.md` recommended
  `tsc --noEmit` on `PostToolUse` while its own reference and its own anti-pattern list said otherwise. The
  `Stop` hook example carried a `matcher`, which is a tool-name filter and is inert on a non-tool event.
- **Fixed the Phase 0 probe.** `command -v claude && claude mcp list || echo "CLI unavailable"` reported the
  CLI as missing whenever the subcommand merely failed, contradicting the skill's own rule that a failed
  inventory is not an empty one.
- **Corrected the global config path.** `~/.claude.json` is wrong wherever `CLAUDE_CONFIG_DIR` is set; the
  file lives inside the configured directory. Verified on such a machine.
- **Cut the references by roughly a third**, removing detection tables that restated `SKILL.md` and eight
  worked skill examples that restated each other. The hook contract, cost model, and runnable configurations
  were kept intact — they are the content that is unavailable elsewhere.
- **Added `compatibility`** and moved `license` to the specification's top-level field, where the Apache-2.0
  obligation is visible to a consumer.

## Upstream license

The upstream source is used under the Apache License, Version 2.0. A verbatim copy is kept alongside this file
as `LICENSE.upstream`.

As required by section 4 of that license, this is a modified version; the changes are listed above. Keep this
file and `LICENSE.upstream` with the skill when redistributing.

Copyright Anthropic, PBC.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at <http://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed under the License is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the License.
