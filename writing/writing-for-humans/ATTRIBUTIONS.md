# Attributions

## Current skill

- Skill: `writing-for-humans`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: assembled from the author's own writing rules plus three adapted
  upstream sources

## Original authors and sources

**Primary source** — structure, provenance and skimmability principles, the
backbone of this skill:

- The author's own global writing rules (`rules/WRITING.md`), ported into a
  portable, agent-agnostic skill.

**Secondary source** — seven distilled composition rules: positive form, parallel
construction, emphatic word at sentence end, omit-needless-words phrase
reductions, the dangling-modifier rule, keeping related words together, and
breaking a run of loose sentences:

- *The Elements of Style* by William Strunk Jr. (1918). Public domain.
- The first four were taken when this skill was written. The last three were
  added 2026-08-25, after reviewing `softaworks/agent-toolkit`'s
  `writing-clearly-and-concisely`, which is Strunk repackaged as a skill: the
  comparison showed this skill had independently absorbed 8 of his 11 composition
  rules and was missing three that are concrete and worth having. Stated as
  compact modern directives, NEVER as the verbatim 1918 prose.

**Tertiary source** — the promotional-vocabulary blocklist in
`references/phrases.md`:

- Upstream project: [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit),
  skill `writing-clearly-and-concisely`.
- Upstream chain: adapted by softaworks from
  [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills),
  itself adapted from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style).
- Upstream license: MIT, Copyright (c) 2026 Leonardo Flores.

**Quaternary source** — the AI-tell catalogues that became `references/phrases.md`,
`references/structures.md` and `references/examples.md`, plus several rules in
the Specificity and agency section:

- Upstream project: [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop).
- Pinned at commit `8da1f030185bdfe8471220585162991eaeb970e9` (branch `main`),
  resolved 2026-08-24. Upstream's own changelog last records content changes on
  2026-01-13.
- Upstream license: MIT, Copyright (c) 2025 Hardik Pandya.
- Original author: Hardik Pandya (https://hvpandya.com).

**Quinary source** — three mechanisms in `SKILL.md`: the converging-signals rule
before rewriting, the count-each-passage-once rule, and the supplied-writing-sample
override:

- Upstream project: [blader/humanizer](https://github.com/blader/humanizer),
  itself built from Wikipedia's
  [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
  (WikiProject AI Cleanup).
- Upstream license: MIT, Copyright (c) 2025 Siqi Chen.

**Senary source** — five entries in `references/structures.md` (copula avoidance,
synonym cycling, forced groups of three, false ranges, the document-level formula
table) and two in `references/phrases.md` (closers, knowledge-cutoff hedging):

- Upstream project: [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing).
- Upstream license: MIT, Copyright (c) 2025 jpeggdev.
- Only the patterns were taken. Its architecture was rejected: a per-pattern
  conditional for nearly every rule, and a 15-item "5+ hits = likely
  AI-generated" scoring rubric. Its worked examples are cited in
  `references/examples.md` as a warning rather than a model — see the review
  record below.

All upstream MIT licenses were fetched verbatim from their repositories'
`LICENSE` files on 2026-08-24 and ship beside this file as `LICENSE.upstream`.

## Adaptation note

This skill takes its structure and provenance discipline from the author's own
`WRITING.md`, adds four distilled rules from Strunk stated as compact modern
directives rather than the verbatim 1918 prose, and adopts the
promotional-vocabulary blocklist from softaworks' `writing-clearly-and-concisely`.
Strunk's dogmatic "avoid the passive voice" was softened to an "active by
default, passive when the actor is irrelevant" rule.

On 2026-08-24 the separately deployed `stop-slop` skill was merged into this one
and removed from `skills/kasetto/base.yaml`. The two skills overlapped little by
volume but contradicted each other wherever they touched, and both were loadable
in the same session. What changed in the merge:

- **Reframed rather than copied.** Stop-slop's "narrator-from-a-distance",
  "put the reader in the room" and "cut quotables" rules were written for essays.
  Restated as specificity and unnamed-actor rules, they apply to any prose, which
  is what let the merged skill stay genre-generic instead of splitting by
  document type.
- **Person and fragmentation became a register table**, replacing stop-slop's
  "'You' beats 'People'" and its blanket fragment ban, both of which contradicted
  this skill's third-person default for reference prose.
- **The em-dash ban became a budget and a substitution ladder.** This repo's
  author reported on 2026-08-24 that banning the glyph relocates the habit to
  `--` rather than removing it. That is a field report, not a measurement; the
  reasoning behind the ladder is that the defect is the undecided aside, and the
  glyph only its symptom.
- **Dropped:** the absolute passive-voice ban, the "two items beat three" rule,
  the "kill all adverbs" absolute (kept as a named-offender list, since
  "explicitly" and "deliberately" are load-bearing in normative prose), and the
  five-dimension 1-10 scoring rubric, which graded essay qualities that
  `technical-writing`'s review checklist already covers for documentation.
- **Kept close to upstream:** the phrase blocklists, the binary-contrast,
  negative-listing and rhetorical-setup tables, and the false-agency table.
- **Upstream's five before/after examples were dropped.** Both review gates below
  found they demonstrate single-pattern fixes the model already performs and that
  `phrases.md` already names. `references/examples.md` keeps only two multi-step
  rewrites, both written for this skill.

## Review record, 2026-08-24

The merged draft was graded by the `skill-judge` skill and separately exercised
against three real prose samples from this repository, each in a different
register. Both ran in fresh subagents with no access to the reasoning behind the
merge. The draft scored 100/120. What the two gates changed:

- **A worked example taught fabrication.** It rewrote an actor-less sentence into
  named people, months and counts that the original did not support, and praised
  the result. `technical-writing`'s Iron Law forbids exactly this. The example now
  shows both the has-the-history and the has-only-the-draft rewrite, and states
  the prohibition.
- **The Iron Law was one-directional**, policing subtraction while an example
  praised addition. It now requires a rewrite to carry exactly the claims the
  original carried.
- **"Cut lazy extremes" fired on RFC 2119 keywords** — found independently by
  both gates. Applied to this repository's design corpus it would have downgraded
  obligations while appearing to cut tone. The rule now governs descriptive
  claims only.
- **"Cut engineered punchlines" was cut entirely.** It misfired on both
  argumentative samples, could not distinguish a compressed conclusion from
  decoration, and failed this skill's own invariant that every rule be failable
  against a specific sentence. What replaced it tests whether removing the line
  loses a claim.
- **Dates that mark a sentence now lead rather than defer.** The corpus check
  found the original provenance rule contradicted this repository's
  amend-in-place-with-a-date convention, where the date's position IS the marker.
- **"Recorded because…" was exempted from the meta-commentary blocklist**, for
  the same reason: this repository's house voice requires it.
- **A fragment ceiling living only in a reference** contradicted the register
  table in the body and added a second conditional, breaking invariant 1. Removed.
- **The wh-word ban was narrowed to pseudo-cleft openers.** As written it
  condemned two sentences in this skill's own body.

## Candidate review, 2026-08-24

Three further AI-writing skills were reviewed for adoptable material, in two
research lanes. All three are MIT. Only what is listed under the quinary and
senary sources above was taken, and every claimed gap was verified absent from
this skill's files by search before adoption rather than on the reviewer's word.

- [blader/humanizer](https://github.com/blader/humanizer) — three mechanisms
  adopted. Its 35-pattern table was declined as already covered.
- [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing) —
  seven patterns adopted, architecture declined. **Its worked examples fabricate
  named sources, quotes and statistics as part of the demonstrated fix**, which
  is the failure this skill's Iron Law exists to prevent. Recorded in
  `references/examples.md` because the mechanism generalises: a rule that rewards
  concrete detail creates pressure to invent it. Its Pass 8 ("Add Human Texture
  and Soul") has no register gating and would inject first person and personal
  asides into a spec.
- [israelsaba/ai-writing-detector-skill](https://github.com/israelsaba/ai-writing-detector-skill)
  (MIT, Copyright (c) 2026 Israel Saba) — **nothing adopted.** Its absolute
  em-dash ban is the failure mode this skill's dash budget exists to avoid, and
  its pt-BR wordlists would be a second conditional. Its one idea worth keeping,
  a coefficient-of-variation burstiness metric over sentence length, is deferred
  to `skills/TODO.md` in this skill's source repository (`agent-setup`; the path
  does not resolve from a deployed copy): the mechanism is sound, its published
  thresholds cite no study, and computing it needs a script rather than a rule.

## Second candidate review and re-score, 2026-08-25

`softaworks/agent-toolkit`'s `humanizer` skill was reviewed after the adoptions
above. It is a fork of `blader/humanizer`, so 18 of its 24 patterns were already
present here, several with the same examples. Five markup tells were adopted into
`references/structures.md` (boldface overuse, inline-header bullets, title case,
emoji, curly quotes in plain-text contexts) along with the chat-artifacts list.
Nothing else was taken.

**Its "PERSONALITY AND SOUL" section instructs the opposite of this skill's Iron
Law**, and its worked examples fabricate throughout: an invented New York Times
interview with a year and an argument, an invented architect's quote, an invented
2019 Chinese Academy of Sciences survey, invented dates for IT parks and a
drainage project. That is the third reviewed skill in a row demonstrating
fabrication in its canonical examples, which is why `references/examples.md`
records the mechanism rather than any single instance, and why the anti-pattern
list now names injected personality directly.

`softaworks/agent-toolkit`'s `writing-clearly-and-concisely` was re-reviewed on
2026-08-25, having been an upstream since this skill was written. Three Strunk
rules were taken (see the secondary source above). Its ~50-entry misused-words
glossary was examined and declined: it is prescriptive usage correctness for an
author rather than a rewrite discipline, and parts of it are obsolete. Its
`signs-of-ai-writing.md` is Wikipedia's guide unabridged, and every portable
category in it was already present here.

**All five reviewed skills trace to one source.** Wikipedia's
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup, is upstream of `blader/humanizer`, of
`jpeggdev/humanize-writing` which cites it, and of both softaworks skills — one
toolkit shipping the guide unabridged and a distillation of it under two names.
Recorded because it explains why the returns collapsed after the second skill and
sets the expectation for any future candidate: a sixth skill from this lineage
would add nothing. It also means Wikipedia's own framing is worth more than any
of its downstreams. That page describes itself as "descriptive, not prescriptive
— observations, not rules", which is nearer this skill's converging-signals gate
than to the flat blocklists every downstream made of it.

A second `skill-judge` pass on 2026-08-25 scored the package 100/120 again and
found three defects the first pass could not have seen, because round 2 created
them:

- **The converging-signals gate sat above the two Iron Law checks**, so read
  literally, a single fabricated statistic in an otherwise clean rewrite was a
  lone signal to be left alone. That inverted the rule this skill treats as
  outranking every other. The gate is now scoped to style checks explicitly.
- **The voice-sample override had no floor** and reached the fabrication check.
  It now stops at the Iron Law, the fabrication check and scope protection, and
  states that two paragraphs cannot establish a dash rate.
- **Invariant 1 was false, and had been before round 2.** The audit found five
  genre conditionals outside the register table, each with its own vocabulary for
  the axis. They are folded into the table as two new columns; the invariant is
  reworded to what it actually protects. `Count each passage once` was cut as a
  reviewer-output rule in a skill that produces no report.

What the corpus check found that no fix addresses, recorded because it sets
expectations for this skill rather than pointing at a defect: the skill changed
the outcome materially on instructional prose, contributed one cosmetic change to
reference prose already written to a stricter internal standard, and produced one
correct fix plus three declined findings on argumentative prose. The dash budget
fired twice, was right both times, and never identified a paragraph that the
sentence-length rule had not already flagged.
