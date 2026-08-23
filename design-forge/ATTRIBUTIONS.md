# Attributions

## Current skill

- Skill: `design-forge`
- Author: Joonas Onatsu
- License: MIT
- Status: **original work.** No upstream text was copied, transliterated, or edited into this skill,
  so no file carries an upstream header. This ledger records idea-level influence only.

## Prior art reviewed

Four artifacts were reviewed on 2026-08-23 during the design session that produced this skill. The
review, the licence readings, and the grep evidence behind them are recorded in
`docs/plans/requirements-skill.md` in this repository. The licences below are as recorded there; they
were read from the upstream LICENSE files by that session, not re-verified when this skill was
written.

| Source | Licence as recorded | Used here |
|---|---|---|
| `theepan/ai-agent-skills` → `software-requirements` | MIT, © 2026 Theepan | Idea only — see below |
| `jam01/SRS-Template` | CC0 1.0 | Idea only — see below |
| `jam01/SDD-Template` | CC0 1.0 | Nothing |
| `jwynia/agent-skills` → `requirements-analysis` | No LICENSE file at repo root | Nothing |

A second review on 2026-08-23, while this skill was being written, covered four more
artifacts. Licences were read from each repository's actual LICENSE file; a missing file is
recorded as missing rather than guessed.

| Source | Licence | Used here |
|---|---|---|
| `rick4470/IEEE-SRS-Tempate` | MIT, © 2015 Rick | Nothing |
| `marcobuschini/Software-Requirements-Specification` | **No LICENSE file at repo root** | Nothing |
| `doorstop-dev/doorstop` | LGPL-3.0-only | Nothing — see below |
| `useblocks/sphinx-needs` | MIT, © 2016-2025 useblocks GmbH | Nothing |
| `docs.driesventer.com` markdown templates | No licence stated; informal permission to reuse on the site's homepage | Nothing |

## What was taken, and at what level

**The atomic requirement schema** in `references/authoring.md` — a per-requirement field set covering
identifier, statement, rationale, priority, source, acceptance criteria, dependencies and notes. The
idea of shipping this as a fixed schema, and the idea of pairing it with a banned-vague-words gate,
came from Theepan's MIT-licensed `software-requirements` skill. The field names, the wording, the
worked example, and the replacement table here were written from scratch. The field set itself is
long-standing requirements-engineering practice rather than that skill's invention.

**The breakout-file pattern** — separating what, how and why into distinct document sets rather than
one monolith — was noted in the CC0-licensed `jam01/SRS-Template`. CC0 imposes no attribution
obligation; it is recorded here for provenance.

## Sources quoted in `references/domains.md`

That file is the non-software vocabulary, and it quotes rather than paraphrases where the exact
wording matters. Each source and its reuse status:

| Source | Status | How it is used |
|---|---|---|
| NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev 2 | US government work, public domain | The four verification-method definitions, the verification glossary entry, the ConOps definition, the three baselines and the traceability definition are quoted directly |
| Texas Instruments / Burr-Brown reliability application notes (AB-059, SPRABY3) | Copyrighted, freely distributed | MTTF, failure-rate and FIT definitions are restated in our own words, and one worked FIT figure is cited as a measurement. No TI text is reproduced |
| European Commission, RoHS Directive 2011/65/EU page | Official EU public information | The ten restricted substances are listed as fact |
| SEBoK (Guide to the Systems Engineering Body of Knowledge) | Licence not checked | Cited by name for two factual claims — that it lists Sampling as a fifth technique, and that it records over-reliance on Test as a pitfall. No text reproduced |
| A hardware requirements specification template supplied by the user, provenance unknown | No licence, source unavailable | Used only to seed the list of hardware categories to go and verify. Every category that survived is stated in our own words, and the list was corrected against the sources above rather than adopted |

`references/domains.md` carries its own source-confidence table marking which claims are
primary-source-verified, which rest on secondary sources because the standard is paywalled, and which
are explicit gaps. That table is part of the deliverable, not a caveat appended to it.

## What was deliberately not taken

- The per-requirement status enum from the CC0 templates. Workflow state belongs in the tracker, and a
  second copy inside the document is one nobody updates. `references/authoring.md` says so and why.
- The large section skeletons from both jam01 templates — 43 headings in the SRS, 15 viewpoints in the
  SDD. Handed that skeleton, an agent told to keep a document complete fills every leaf, because an
  empty heading reads as an omission. That mechanism is named in `references/contract.md` as the
  reason this skill's section catalogue is short.
- Anything from `jwynia/agent-skills`. The repository carried no LICENSE file at its root when it was
  reviewed, so it grants nothing. Its ideas were noted in the design record and not used here.
- Anything from `marcobuschini/Software-Requirements-Specification`, for the same reason. Its text is
  in any case a near-identical derivative of the same template lineage as the MIT-licensed
  `rick4470/IEEE-SRS-Tempate`.
- Anything from `doorstop-dev/doorstop`. It is LGPL-3.0-only, and nothing from it — code, vocabulary
  or text — is present here. Its `reviewed` stamp was examined only to test whether this skill's lock
  model already existed in the wild. It does not: the stamp is warn-only, settable and clearable in
  both directions, and designed to be bulk-reset. It is prior art for **staleness detection**, which
  is a different thing from the **lifecycle governance** this skill implements, and the design record
  states the distinction rather than claiming the broader novelty.
- Anything from the `docs.driesventer.com` templates. The site offers an informal permission to reuse
  rather than a licence, and its templates carry no lifecycle machinery and no writing conventions to
  lift. Two of them also use `[[_TOC_]]`, which is Azure DevOps wiki syntax that renders as literal
  text elsewhere.
