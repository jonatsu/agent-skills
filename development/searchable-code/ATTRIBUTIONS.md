# Attributions

## Current skill

- Skill: `searchable-code`
- Current author: Joonas Onatsu
- Current license: MIT, unchanged from upstream
- Status: **adapted from upstream**, condensed and reorganised

## Original author and source

- Original author: Modem ([modem-dev](https://github.com/modem-dev))
- Copyright holder: `Copyright (c) 2026 Modem`, as stated in the upstream `LICENSE`
- Upstream project: [modem-dev/skills](https://github.com/modem-dev/skills)
- Source path: `write-discoverable-code/SKILL.md`
- Source revision: `edcdedb38a545f67c065f4084b3627517f0d79cf`, read 2026-09-03
- Upstream license: MIT

## Adaptation

**This is an adaptation, not an independent expression, and an earlier version of this file wrongly claimed
otherwise.** The first draft asserted that no upstream prose or examples were copied. A side-by-side check on
2026-09-03 refuted that. The skill retains at least ten of the upstream's distinctive example identifiers:

- `diffUserObjects`, `queueEventForDispatch`, `sanitizeEmailHtml`
- `billing-plan-config`, `organizationId`, `users/diff.ts`
- `github.pr.merged`, `Webhook signature mismatch`
- `session has expired`, `source time, not insert time`

It also retains several formulations that differ from upstream by a word or two, such as "qualify as far as
uniqueness requires, then stop" and "that line is the whole message". The correction is recorded rather than
quietly replacing the old sentence, because a false provenance claim is what a licence audit would have
relied on.

Upstream supplied the organising insight — that agents navigate by plain-text search, so an identifier is a
search query — and the mechanics that follow from it: phrase-matching doc comments, whole string literals,
unique error-message prefixes, and the cost of bare-role filenames.

The adaptation condenses and reorganises. Roughly a third of the source was dropped because it addresses
concerns other than findability: branded identifier types and capability-token parameters (argument safety),
discriminated unions and avoiding `any` (type design), colocated tests, `@deprecated` markers, the
thin-orchestrator rule and "a module should make sense with its imports unread" (module structure, already
governed by this repository's global workflow rules), and "name types like they'll be quoted back" (type
naming).

**One upstream claim was deliberately not carried, and the reason is worth keeping.** The source states that
on a roughly 700k-line monorepo, one-word exported names are globally unique 61% of the time, three-word names
96%, and four-word names 98%, and concludes that three words is the knee of the curve. It names no method,
artifact, or repository, so the figures cannot be checked. They are the stated justification for its naming
rule. This skill uses "the shortest name that greps uniquely" instead, which rests on its own reasoning and
needs no measurement — restating an uncheckable figure as fact would have been the alternative.

## Upstream license

The upstream source is used under the MIT License. The verbatim license text ships as `LICENSE.upstream`;
preserve it and this attribution file when redistributing the skill. The upstream repository root at that
revision contains no `NOTICE` file, verified 2026-09-03.
