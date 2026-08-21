# Attributions

## Current skill

- Skill: `claude-md-auditor`
- Current author: Joonas Onatsu
- Current license: Apache License 2.0 (inherited from upstream; not relicensed)
- Status: adapted from upstream and substantially rewritten

## Original authors and source

- Original author: Anthropic
- Upstream project: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Upstream plugin: `claude-md-management` version 1.0.0
- Source path: `plugins/claude-md-management/skills/claude-md-improver/`
- Upstream skill name: `claude-md-improver`

## What was kept, and what was rebuilt

This is closer to a rewrite than a port. Provenance per file:

| File here | Relationship to upstream |
|---|---|
| `SKILL.md` | Rewritten. Keeps the audit-then-propose-then-apply shape and the approval gate; every phase's content is new |
| `references/scoring-rubric.md` | Rebuilt from `quality-criteria.md`. Retains five of the six criterion names; anchors, weights, evidence requirements, and reporting rules are new |
| `references/templates.md` | Upstream's, with the broken fences repaired |
| `references/update-guidelines.md` | Upstream's, unchanged in substance |
| `references/loading-model.md` | New. No upstream counterpart |

## Adaptation note

A review of the upstream plugin is recorded at
`docs/claude-md-management-plugin-review.md`, with file:line evidence for each
defect below. The upstream plugin is not installed here; this skill replaces it.

Material changes, in the order they matter:

- **The rubric now requires evidence.** Upstream scored "Architecture clarity"
  (20 points) and "Currency" (15) from the CLAUDE.md text alone, having read
  nothing else, and `quality-criteria.md:94` instructed the model to run
  documented commands "mentally or actually" — a licence to fabricate the
  highest-weight criterion it claimed to check. Thirty-five of a hundred points
  rested on evidence never gathered. Each criterion now names the evidence it
  requires, and a criterion without it is reported `not assessed` and leaves the
  denominator.
- **Added the loading model, which upstream lacked entirely.** None of its 801
  lines mention `@` imports, scope precedence, on-demand subdirectory loading,
  `.claude/rules/`, compaction behavior, or `/context`. That is the knowledge an
  audit actually needs, and its absence is why the original scored a
  three-import entrypoint as an empty file. Sourced from the official memory
  documentation, read 2026-08-21.
- **Corrected two filenames that do not exist.** Upstream's discovery searched
  for `.claude.md` and `.claude.local.md` — neither is ever read by Claude Code —
  and missed `CLAUDE.local.md`, which is. It then recommended the wrong name to
  the user three more times, sending personal instructions into a file that
  silently does nothing. Both are now documented as findings to report.
- **Stopped hardcoding `~/.claude/CLAUDE.md`.** The user scope follows
  `CLAUDE_CONFIG_DIR` when set; the hardcoded path reports the user file as
  missing on every relocated setup.
- **Fixed discovery.** Upstream ran `find .` from the working directory, which
  can never reach the global file its own table listed as in scope, with no
  `-type f`, no pruning of `node_modules`/`.git`/vendor, and a `head -50` cap
  that a vendored tree can consume entirely. Discovery now walks ancestors,
  resolves the config directory, prunes, and classifies each file as
  launch-loaded, conditional, or never loaded.
- **Removed a false architectural claim.** Upstream stated that parent-directory
  auto-discovery "makes monorepo setups work automatically". Parent traversal
  never reaches `./packages/*/CLAUDE.md`, which are children; per-package files
  work through on-demand loading instead.
- **Fixed the precision theatre.** Upstream anchored criteria at 0/5/10/15/20
  while demanding per-criterion `X/20` scores and an "average score: X/100"
  across unrelated files. Scores now sit on the anchors, are reported as
  `earned / assessed`, and are never averaged across files.
- **Wired in the orphaned reference.** `update-guidelines.md` was referenced from
  nowhere in the plugin despite holding its only concrete good-versus-bad
  examples; the advice that did load was written four separate times. It is now
  loaded at the proposal phase, and the duplicated prose is gone.
- **Repaired broken fences.** Four of five templates in `templates.md` were
  truncated by a nested fence closing the outer block early, as was the diff
  example in `SKILL.md`. Outer fences now use four backticks.
- **Dropped the stale `#` tip.** Upstream told users to press `#` to incorporate
  learnings into CLAUDE.md; the review could not confirm this against Claude Code
  2.1.233, and the current documented path is auto memory, a separate system this
  skill explicitly leaves alone.
- **Restructured to this repository's skill conventions**: Iron Law, trackable
  workflow with blocking markers, anti-patterns, and a pre-delivery checklist.

The plugin's other component, the `/revise-claude-md` command, was **not**
ported. Stripped of scoring it is a subset of `claude/reflect`, which routes
captures by scope and enforces an autonomy boundary the command lacks, and this
repository deploys skills rather than commands.

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
