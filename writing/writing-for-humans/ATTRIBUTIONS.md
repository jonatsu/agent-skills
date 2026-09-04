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
- [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing) informed the warning that
  specificity rules can pressure a writer to invent details. MIT, Copyright (c) 2025 jpeggdev.

The MIT license texts fetched on 2026-08-24 remain in `LICENSE.upstream`.

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
by its controlled dictionary, which this project does not hold and does not reproduce. This skill's ban on em
and en dashes is a house rule and is not derived from the standard, which states that it gives no general
punctuation rules.

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
