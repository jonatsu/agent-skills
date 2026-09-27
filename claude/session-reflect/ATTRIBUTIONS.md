# Attributions

## Current skill

- Skill: `session-reflect`, named `reflect` until 2026-09-28
- Author: Joonas Onatsu
- License: MIT (this repository's `LICENSE`)
- Status: original work. This is **not** a fork or a port — three ideas were lifted from the upstream below
  and rewritten; no upstream text was copied.

## Idea source

- Upstream project: [alvinunreal/oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim)
- Upstream license: MIT (`package.json` declares `"license": "MIT"`; the `LICENSE` file carries the MIT
  permission text under an unnamed `Copyright (c) 2025` holder, so no individual can be credited)
- Source path: `src/skills/reflect/SKILL.md`
- Snapshot read: the copy installed by the `oh-my-opencode-slim@2.2.8` plugin into
  `~/.config/opencode/skills/reflect/`, committed there at `ccb37af` on 2026-07-12

The two skills share only a name. Upstream's is a workflow-pattern recommender that suggests reusable skills,
agents, and commands; this one is an end-of-session sweep that routes learnings to durable homes. Upstream's
own lineage stops there — `oh-my-opencode-slim` describes itself as a fork of `oh-my-opencode`, but that
project ships no `reflect` skill, so there is no third party to credit.

## What was taken

Three ideas, each rewritten into an existing section rather than appended:

| Idea                                                                                                                                | Upstream location                               | Where it landed             |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------- |
| Read the destination before proposing a new artifact; extend what already covers the candidate instead of creating a near-duplicate | "Core Contract" and "Inventory Existing Assets" | §2, after the routing table |
| A standing instruction is paid on every session it was not written for, so weigh that cost before codifying one                     | "Guardrails"                                    | §3, after the ladder        |
| Evidence carries secrets and private material; a capture must not                                                                   | "Evidence Sources" and "Guardrails"             | §5, as a bullet             |

## What was not taken

The recommender job itself, and everything supporting it: the `--sessions` session-archaeology mode, its
per-session JSON summaries, confidence scores, summary caching, and aggregation; the three output-format
blocks; and the candidate-scoring ladder, which duplicates §3 with different thresholds. The sweep's §8
compaction backlog already does session archaeology through a Claude-native mechanism.

## Why no license header travels

Under the four-trigger threshold in `~/.config/claude/CLAUDE.md`, an upstream notice travels when a contiguous
run of the original survives modulo renaming, when the work is a transliteration keeping the same steps and
decomposition, when identifiers or comments or error strings or magic constants are carried over, or when text
is copied and edited rather than rewritten. All four are false here: three ideas were restated in this skill's
own voice and structure, and MIT's notice condition binds copies and substantial portions of the software.
This ledger entry is the attribution.
