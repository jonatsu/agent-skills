# Attributions

## Current skill

- Skill: `agents-management`
- Current author: Joonas Onatsu
- Current license: Apache License 2.0 (inherited from upstream; not relicensed)
- Status: merged from two skills, one adapted from upstream and substantially
  rewritten, one original

## Composition

`agents-management` merges two predecessors:

| Predecessor | Origin | Contribution |
|---|---|---|
| `claude-md-auditor` | adapted from Anthropic upstream, Apache-2.0 | The audit branch: loading model, scoring rubric, update guidelines, templates |
| `agent-repo-docs` | original, MIT, Joonas Onatsu | The author branch: repo-fact verification, llms.txt, the AGENTS.md asset |

The MIT-licensed original work is folded under Apache-2.0 with the author's
consent, being the same author. The Apache-2.0 obligations from upstream govern
the merged skill.

## Original authors and source

- Original author: Anthropic
- Upstream project: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Upstream plugin: `claude-md-management` version 1.0.0
- Source path: `plugins/claude-md-management/skills/claude-md-improver/`
- Upstream skill name: `claude-md-improver`
- Upstream carries a `LICENSE` and no `NOTICE` (checked 2026-08-26), so
  `LICENSE.upstream` ships alone.

## What was kept, and what was rebuilt

Closer to a rewrite than a port. Provenance per file:

| File here | Relationship to upstream |
|---|---|
| `SKILL.md` | Rewritten. Keeps the audit-then-propose-then-apply shape and the approval gate; every phase's content is new, and the author branch has no upstream counterpart |
| `references/scoring-rubric.md` | Rebuilt from `quality-criteria.md`. Retains five of six criterion names; anchors, weights, evidence requirements, red flags and reporting rules are new |
| `references/update-guidelines.md` | Upstream's good-versus-bad pairs survive; the framing, the two tests, the worked examples and the checklist are new |
| `references/templates.md` | Upstream's section list, reshaped. Several templates were inverted, because upstream templated content its own rubric penalizes |
| `references/loading-model.md` | New. No upstream counterpart |
| `assets/AGENTS.template.md`, `assets/llms.template.txt` | Original, from `agent-repo-docs` |

## Adaptation note

The defects that drove the original rewrite, each with file:line evidence in the
upstream plugin, are recorded below. The upstream plugin is not installed here;
this skill replaces it.

- **The rubric now requires evidence.** Upstream scored "Architecture clarity"
  (20 points) and "Currency" (15) from the file text alone, having read nothing
  else, and `quality-criteria.md:94` instructed the model to run documented
  commands "mentally or actually" — a licence to fabricate the highest-weight
  criterion it claimed to check. Thirty-five of a hundred points rested on
  evidence never gathered. Each criterion now names the evidence it requires, and
  a criterion without it is reported `not assessed` and leaves the denominator.
- **Added the loading model, which upstream lacked entirely.** None of its 801
  lines mention includes, precedence, on-demand nested loading, rules
  directories, or how to confirm what loaded. That is the knowledge an audit
  actually needs, and its absence is why the original scored a three-include
  entrypoint as an empty file.
- **Corrected filenames that are never read.** Upstream's discovery searched for
  dot-prefixed variants no agent reads, then recommended them to the user three
  more times, sending instructions into files that silently do nothing.
- **Fixed the precision theatre.** Upstream anchored criteria at 0/5/10/15/20
  while demanding per-criterion scores off the anchors and an average across
  unrelated files. Scores now sit on the anchors, are reported as earned over
  assessed, and are never averaged.
- **Wired in the orphaned reference.** `update-guidelines.md` was referenced from
  nowhere in the plugin despite holding its only concrete good-versus-bad
  examples; the advice that did load was written four separate times.
- **Reconciled two files against the rubric they ship with.** Upstream's
  `update-guidelines.md` offered a transcription of the runner's own command
  list as its worked example of a helpful addition, and `templates.md` templated
  a directory-tree dump — both of which the rewritten rubric explicitly
  penalizes. The rubric had been raised to an evidence-gated standard and the
  two files beside it had never been brought up to it.
- **Removed the ecosystem assumption.** Every worked example in upstream's
  guidance was drawn from one language ecosystem, which made general advice read
  as specific advice. Runner detection stays broad; examples no longer assume a
  package manager, test runner, or language the repository has not evidenced.
- **Repaired broken fences.** Four of five templates were truncated by a nested
  fence closing the outer block early.

### Scope change in this merge

Two fixes credited to the earlier rewrite no longer apply, because the merged
skill is narrower rather than because they regressed. `agents-management` is
**repository-local only**: it does not read, score, or edit user-level or global
configuration. The earlier "stopped hardcoding the user config path" and "walks
ancestors and resolves the config directory" changes described behavior that is
now out of scope and has been removed rather than fixed.

The plugin's other component, its revise command, was **not** ported. Stripped
of scoring it is a subset of the `reflect` skill, which routes captures by scope
and enforces an autonomy boundary the command lacks.

## Third-party material

### mattpocock/skills — `writing-for-agents`

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/`
- License: MIT, Copyright (c) 2026 Matt Pocock
- Read 2026-08-26

Two ideas adopted and independently re-expressed in this repository's voice; no
text copied. The **no-op test** — an instruction the model already obeys by
default pays load to say nothing, and a failing sentence is deleted whole rather
than trimmed — appears in `references/update-guidelines.md` and in `SKILL.md`'s
proposal phase, deliberately not in the scored rubric, since it is not citable
evidence. The **cache principle** — a document restating the environment is a
copy of a lookup, earning its load only when the lookup is expensive — is the
organizing idea of `references/update-guidelines.md`.

### netresearch/agent-rules-skill

- Source: <https://github.com/netresearch/agent-rules-skill>
- License: dual — MIT for code, **CC-BY-SA-4.0 for content**, Copyright
  Netresearch DTT GmbH, 2025–2026
- Read 2026-08-26

**No prose was copied, and none may be.** The content license is share-alike,
which would propagate to any adapted text and conflict with the Apache-2.0
obligations this skill already carries. Only facts and ideas were taken, which
copyright does not cover, and each was re-expressed independently:

- Per-directory symlinks are required for nested instruction files to be picked
  up; a root symlink alone does not reach them.
- A pointer instruction may be acknowledged without being acted on. Recorded in
  `references/loading-model.md` as an external, undated, unreproduced result,
  with imperative phrasing as the mitigation — not asserted as fact.
- Generated content and hand-written knowledge should be separated by markers so
  a regeneration cannot swallow the latter.
- Structure and score checks answer "right shape", never "is the knowledge still
  here"; a diff of removed lines is the check that does.

### DenisSergeevitch/agents-best-practices

- Source: <https://github.com/DenisSergeevitch/agents-best-practices>,
  `references/system-prompts-instructions.md` and `references/architecture.md`
- License: MIT, Copyright (c) 2026 Denis Shiryaev. Read verbatim from the
  repository's own `LICENSE` at the default branch, 2026-08-27
- Read 2026-08-27

Upstream is a harness-design skill and covers none of this skill's subject — it
never mentions `AGENTS.md`, `CLAUDE.md`, `copilot-instructions` or `llms.txt`.
Two ideas were taken from it and independently re-expressed for repository-local
instruction files; no text copied.

- **A prompt states policy; code enforces it.** Upstream argues this for a
  harness permission check. Here it becomes the rank of an instruction file
  itself, in `SKILL.md` and in `references/update-guidelines.md` §6 — with the
  corollary upstream does not draw, that a safety rule with no gate behind it
  scores worse than its absence.
- **Prompt patterns that claim authority they do not hold** — the autonomy grant,
  "complete the task no matter what", and self-approval of a risky action.
  Upstream lists them for system prompts; the same three appear in instruction
  files, where the user's own turn outranks them.

Upstream's untrusted-content boundary is a harness concern and was NOT adopted as
written. What survives is the repository-local case only: vendored, generated and
third-party text is data the repo stores, never guidance it has adopted.

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
