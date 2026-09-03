# Attributions

## Current skill

- Skill: `searchable-code`
- Author: Joonas Onatsu
- License: MIT

## Idea source

- Project: [modem-dev/skills](https://github.com/modem-dev/skills)
- Source path: `write-discoverable-code/SKILL.md`
- Source revision: `edcdedb38a545f67c065f4084b3627517f0d79cf`, read 2026-09-03
- License: MIT

The source supplied the organising insight — that agents navigate by plain-text search, so an identifier is a
search query — and the specific mechanics that follow from it: phrase-matching doc comments, whole string
literals, unique error-message prefixes, and the cost of bare-role filenames. This skill expresses those
independently; no upstream prose, code, examples, scripts, or assets are copied, adapted, translated, or
vendored.

Roughly a third of the source was deliberately not carried, because it addresses concerns other than
findability: branded identifier types and capability-token parameters (argument safety), discriminated unions
and avoiding `any` (type design), colocated tests, `@deprecated` markers, and the thin-orchestrator rule
(module structure, already governed by the repository's global workflow rules).

**One upstream claim was deliberately not carried, and the reason is worth recording.** The source states that
on a roughly 700k-line monorepo, one-word exported names are globally unique 61% of the time, three-word names
96%, and four-word names 98%, and concludes that three words is the knee of the curve. It names no method,
artifact, or repository, so the figures cannot be checked. They are the stated justification for its naming
rule. This skill uses "the shortest name that greps uniquely" instead, which rests on its own reasoning and
needs no measurement — restating an uncheckable figure as fact would have been the alternative.
