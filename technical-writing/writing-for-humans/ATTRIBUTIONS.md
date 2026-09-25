# Attributions

## Current Skill

- Skill: `writing-for-humans`
- Current author: Joonas Onatsu
- Current license: MIT AND CC-BY-4.0
- Status: sentence- and paragraph-level prose policy and independently authored copy-editing guidance

## Retained Influences

The active skill retains these independently expressed influences for claim-preserving copy editing, style
adaptation, and AI-mark diagnosis.

- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), pinned at
  `8da1f030185bdfe8471220585162991eaeb970e9`, informed the chat-residue, promotional-language, and
  false-agency diagnostics. MIT, Copyright (c) 2025 Hardik Pandya.

- [blader/humanizer](https://github.com/blader/humanizer), based on Wikipedia's
  [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), informed the
  weak-signal threshold and writing-sample override. MIT, Copyright (c) 2025 Siqi Chen.

  Upstream rebuilt itself on 2026-09-06 around a single account of why model prose reads as it does, plus 25
  patterns ordered by strength. That revision, pinned at `9862685f575c65a8247f90369951df1b3416e3d6`, further
  informed the staging account, the act-on-one-sighting tier and its members: the negative half nobody
  claimed, the closer that restates its paragraph, the aphorism standing in for a claim, the announced
  run-up, the objection nobody raised, and the gap filled with a plausible guess. It also informed the
  forced-triad rule, the plain-verb rule against "serves as" and "boasts", the vague-relation rule that
  complements this skill's existing causality rule, the heading-restated and previous-version rules, the
  emphasis-density rule, and the closing search for the five marks that survive a rewrite. Every idea is
  expressed independently and the worked examples in `references/rewrites.md` are original; upstream's own
  examples are general-interest prose rather than technical writing.

  Its em-dash rule, its hyphenated-pair rule, and its fixed vocabulary list were considered and declined.
  This skill's dash rule is stricter and already carries the write-versus-edit asymmetry; `diagnostics.md`
  treats compound hyphenation more accurately than a flat tell; and a word blocklist contradicts both this
  skill's stance on evidence and its language-general scope, for the same reasons recorded against
  `Anbeeld/WRITING.md` below. Upstream's sentence-case heading rule is declined because it contradicts this
  skill's heading convention. Its bold rule was adopted only after measurement, recorded in
  `docs/evaluations/skills/2026-09-09-humanizer-prose-comparison.md`.

- [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing) informed the warning that
  specificity rules can pressure a writer to invent details. MIT, Copyright (c) 2025 jpeggdev.

- [Anbeeld/WRITING.md](https://github.com/Anbeeld/WRITING.md), `skills/writing`, pinned at
  `0c127ca4a4e51debec5adf4816f2bf464d83438b`, informed the task non-substitution rule, the quotation-integrity
  additions, the causality-inflation rule, the repeated-move inspection threshold, the authorship-provenance
  guard, the over-correction guard, the placeholder and leaked-token artifacts, the editing-distortion
  diagnostics, the unnamed-authority diagnostic, and the compound-hyphenation guidance. It also prompted the
  revision of the em-dash rule from a character ban to a rewrite-first default, though the rule adopted here is
  stricter than its source and reaches a different result. MIT, Copyright (c) 2026 Anbeeld.

  Its scope is the inverse of this skill's: it covers marketing, SEO, criticism, scripts and application
  materials while excluding commits and code comments, and it is English-only. Its medium-routing table, its
  document-structure rules, its voice-calibration procedure, its numbered required-checks gate, and its
  fixed jargon list were considered and declined. Structure belongs to `writing-documentation`, this skill's
  voice rule is already stricter, and a fixed word list contradicts both the skill's stance against blocklists
  and its language-general scope.

The MIT license texts remain in `LICENSE.upstream`, fetched on 2026-08-24 except for the `Anbeeld/WRITING.md`
text, fetched on 2026-09-06.

[Matt Pocock's `writing-for-agents`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/writing-for-agents/SKILL.md),
pinned at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` (Copyright (c) 2026 Matt Pocock, MIT), informed the
`reader-ready` leading word, its checkable completion criterion, and the rule that a material revision restarts
the complete reader pass. The instructions are independently written; no upstream text was copied or adapted.

## ASD-STE100 as an Inspirational Source

ASD-STE100 Simplified Technical English, Issue 9 (2025-01-15), was read directly on 2026-09-04 and informed the
guidance below. The standard is an inspirational source, not a dependency: this skill does not implement it, does
not cite its rule numbers, and makes no claim of conformance. The rules were adopted because they are good, not
because the standard carries them.

It informed the procedural and descriptive classification and its two sentence limits, the word-counting
convention, one instruction per sentence, the requirement to place a condition before the command it governs,
the rule against omitting words to shorten a sentence, the three-word ceiling on noun clusters, the restriction
on "-ing" verb forms, the preference for simple tenses, the preference for a verb over a noun built from one,
the paragraph topic sentence and six-sentence ceiling, and the inclusive-language rule.

Three of its rules were considered and deliberately declined: its prohibition on the semicolon, its absolute
ban on contractions, and its rule on articles before alphanumeric identifiers. Its remaining rules are defined
by its controlled dictionary, which this project does not hold and does not reproduce. This skill's em-dash
rule is a house rule and is not derived from the standard, which states that it gives no general punctuation
rules. That rule was a flat character ban until 2026-09-06, when it became a rewrite-first default with a
density cap and an explicit write-versus-edit asymmetry. The ban could not distinguish a dash doing real work
from a dash covering a relation the writer declined to name, and it left unclear whether an editor should
strip an author's existing dashes.

No rule text and no dictionary entry is reproduced here or in `SKILL.md`. The standard is free to obtain and not
free to redistribute: its copyright notice grants reproduction rights to eight listed categories of ASD, AIA and
AIAC members, defence ministries, airworthiness authorities and universities, and this project is in none of
them. `docs/plans/archived/ste-adoption.md` records the decisions, including the rejected alternatives.

The `mohitagw15856/pm-claude-skills house-style-enforcer` influence on the 2026-09-03 exemplar-evidence
style-adaptation branch moved to `writing-documentation` on 2026-09-04 together with the section it informed.
This skill retains only the sentence-level rule that an author's voice must not be flattened.

## Adapted Technical-Prose Policy

- [Yue Zhao, *The Elements of Agent Style*, `agents/AGENTS.md`](https://github.com/yzhao062/agent-style/blob/05fc6c8a77d4a8efc08ddfdc4d01534cb98ed2c8/agents/AGENTS.md),
  released as v0.4.2 under CC BY 4.0, supplied the technical-prose rules previously adapted in
  `agents/rules/instructions/writing.md`. This revision moves and further adapts those rules into the skill.
  It retains the audience, terminology, sentence, paragraph, Markdown, action-writing, heading, formal-prose,
  and clarity-override decisions. The adaptation changes scope, organization, wording, and interaction with
  copy editing and AI-mark removal. The upstream license remains in `LICENSE.upstream`, and its notice remains
  in `NOTICE.upstream`.

## Removed Influences

The prior package also retained composition, grammar, dash, heading, vocabulary, and document-genre rules from
Strunk and several upstream writing skills. Document composition remains outside this skill. Technical-prose
rules now come from the attributed `agent-style` adaptation above rather than a separate global writing file.
