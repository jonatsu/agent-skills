# Attributions

## Current skill

- Skill: `system-prompts`
- Author: Joonas Onatsu
- License: MIT
- Status: **original work.** Written from the domain on 2026-08-27, replacing an
  adaptation of the upstream skill named below. No upstream text survives.
- Composition: absorbed the former `prompt-optimizer` (original, MIT, same author) on 2026-08-27 as its REPAIR branch.
  Same author and same licence, so the merge raised no licensing question. A new, independently rewritten
  `skills/shared/agent-stack/prompt-optimizer/` was restored on 2026-09-04 with a narrower failure-driven evaluation and
  repair boundary; repository history preserves the earlier archive mapping.

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
  Both are now in `references/evidence.md` with what actually backs them.
- **A tag vocabulary presented as house style.** The seven-tag table
  (`<system-conventions>`, `<stakes>`, `<yielding>`, …) was upstream's own
  harness convention. It is replaced by a four-line rule: adopt the target
  harness's markers, never invent them.
- **A transcribed prompt presented as general guidance.** The "Tone Patterns That
  Work" section quoted one live system prompt. Removed.
- **A scope collision.** The description claimed `CLAUDE.md`, `AGENTS.md` and
  `rules/*.md`, which `agents-management` owns. Two skills competed for the same
  prompt. Scope is now system prompts, agent and subagent definitions, and tool
  descriptions. Two neighbouring skills are named as boundaries, and `claude-api`
  as a handoff for model and parameter facts.

Retained ideas, all independently re-expressed and none carrying upstream
phrasing: RFC 2119 discipline in prompts, one-claim-per-bullet density,
imperative voice, and the shape of a tool prompt. The RFC alias convention itself
(`NEVER`, `AVOID`) is this repository's own, from its root instruction file, not
upstream's.

Because no contiguous run of upstream code or prose survives, this is a ledger
entry rather than a licence header, and **oh-my-pi contributes no
`LICENSE.upstream`** — the one that ships covers a different upstream, named
under Third-party material below. Upstream was MIT and this skill is MIT, so no
relicensing question arises either way.

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

### Rules-audit notebook (local), and its upstream chain

- Source: `~/.config/claude/docs/RULES-AUDIT-NOTEBOOK.md`, dated 2026-08-27 — a
  local document, not published, merging this machine's own rules audit with a
  third-party principles document
- Upstream half:
  [`abhishekray07/claude-md-templates`](https://github.com/abhishekray07/claude-md-templates),
  `principles.md` at commit `8514fe7460db` (2026-04-09). MIT, Copyright (c) 2026
  Abhishek Ray, itself attributed to the CLAUDE.md Starter Kit by Claude Code Camp
- Read 2026-08-27

The REVIEW branch, `references/global-rule-files.md`, the escape-hatch and
hedge-word sections, the over- versus under-compliance gate, the evidence-grade
table and six corrections to claims this skill previously asserted all derive
from that notebook. Ideas and structure were taken; no text was copied, and the
decomposition was changed — the notebook is organised as one review procedure for
global rule files, while this skill splits the same material across three
branches covering prompts generally.

**Attribution here is deliberately conservative.** The notebook states that half
its content is upstream-derived and half is original, but does not mark which is
which per section, so the upstream chain is named in full rather than guessed at.
Both the notebook's own licence position and this skill's are MIT, so no
relicensing question arises; `LICENSE.upstream` ships with Abhishek Ray's notice
because a portion of what was drawn on is derivative of it and the boundary is
not determinable.

Two things were taken from the notebook and **downgraded rather than adopted as
stated**: the two arXiv studies and the corrections table are recorded here as
reported by that audit and have NOT been re-verified against the primary sources
inside this skill. Both places that use them say so and grade them
DOCUMENTED-at-one-remove. The notebook's own rule — open the source before
repeating a number — is the reason the downgrade is stated rather than assumed.

Not adopted: the notebook's four-tier size discussion beyond "no threshold is
established", and its per-rule metadata schema, which belongs to a maintained
multi-tool ruleset rather than to a single prompt.

## Sources cited in the skill

- Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua,
  Fabio Petroni, Percy Liang. *Lost in the Middle: How Language Models Use Long
  Contexts.* Transactions of the Association for Computational Linguistics, 2023.
  <https://arxiv.org/abs/2307.03172>. Abstract read 2026-08-27; cited for
  retrieval position effects only.
