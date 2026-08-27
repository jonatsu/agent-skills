# Attributions

## Current skill

- Skill: `system-prompts`
- Author: Joonas Onatsu
- License: MIT
- Status: **original work.** Written from the domain on 2026-08-27, replacing an
  adaptation of the upstream skill named below. No upstream text survives.

## What this replaces

The previous version was adapted from `can1357/oh-my-pi`
(`.omp/skills/system-prompts/SKILL.md`, commit
`a1a07fa9e13073e1f48c5422e76e2aac5b524b49`, MIT, Copyright Can Bölük). It was
rewritten rather than edited, for four reasons:

- **Unmeasured claims stated as fact.** "`NEVER` and `AVOID` are single-token in
  cl100k/o200k" is **false** — measured with `tiktoken` 0.14.0 on 2026-08-27,
  ` AVOID` is 2 tokens in both encodings, and both keywords cost 2 at the start
  of a line. A "~20%" middle-of-context degradation figure was attributed to no
  source and does not appear in the abstract of the paper the effect comes from.
  Both are now in the skill's `Measured claims` section with what actually backs
  them.
- **A tag vocabulary presented as house style.** The seven-tag table
  (`<system-conventions>`, `<stakes>`, `<yielding>`, …) was upstream's own
  harness convention. It is replaced by a four-line rule: adopt the target
  harness's markers, never invent them.
- **A transcribed prompt presented as general guidance.** The "Tone Patterns That
  Work" section quoted one live system prompt. Removed.
- **A scope collision.** The description claimed `CLAUDE.md`, `AGENTS.md` and
  `rules/*.md`, which `agents-management` owns. Two skills competed for the same
  prompt. Scope is now system prompts, agent and subagent definitions, and tool
  descriptions, with the three neighbouring skills named explicitly.

Retained ideas, all independently re-expressed and none carrying upstream
phrasing: RFC 2119 discipline in prompts, one-claim-per-bullet density,
imperative voice, and the shape of a tool prompt. The RFC alias convention itself
(`NEVER`, `AVOID`) is this repository's own, from its root instruction file, not
upstream's.

Because no contiguous run of upstream code or prose survives, this is a ledger
entry rather than a licence header, and no `LICENSE.upstream` ships. Upstream was
MIT and this skill is MIT, so no relicensing question arises either way.

## Third-party material

### DenisSergeevitch/agents-best-practices

- Source: <https://github.com/DenisSergeevitch/agents-best-practices>,
  `references/system-prompts-instructions.md`
- License: MIT, Copyright (c) 2026 Denis Shiryaev. Read verbatim from the
  repository's own `LICENSE` at the default branch, 2026-08-27
- Read 2026-08-27

Three ideas adopted and independently re-expressed; no text copied.

- **A prompt states policy; code enforces it.** Upstream's formulation, with the
  worked example of a permission check returning `approval_required`. The
  corollary this skill adds — that an ungated safety rule scores worse than its
  absence, because a reviewer who finds it stops looking for the real gate — is
  not upstream's.
- **Prompt patterns that claim authority the prompt does not hold**: the autonomy
  grant, "complete the task no matter what", and self-approval of a risky action.
  Upstream lists them; the rank analysis explaining *why* each fails is this
  skill's.
- **The untrusted-content boundary**, including the source list and the practice
  of labelling the boundary explicitly. Upstream's boundary statement was
  paraphrased rather than copied, and the caveat that a label reduces but does
  not prevent injection compliance is added here.

Upstream's instruction hierarchy is a nine-rung ladder spanning provider policy
to retrieved content. It was NOT adopted as written — most of its rungs are
harness-design concerns. Only the two that change what a prompt author writes
survive, as the `Rank` calibration.

## Sources cited in the skill

- Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua,
  Fabio Petroni, Percy Liang. *Lost in the Middle: How Language Models Use Long
  Contexts.* Transactions of the Association for Computational Linguistics, 2023.
  <https://arxiv.org/abs/2307.03172>. Abstract read 2026-08-27; cited for
  retrieval position effects only.
