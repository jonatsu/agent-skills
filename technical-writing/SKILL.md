---
name: technical-writing
description: Draft, rewrite, condense, expand, or review technical documentation — README files, design docs, API references, tutorials, onboarding guides, release notes, specs, CLI help, and code comments — so it reads clear, concise, reader-first, accessible, and evidence-backed. Use when writing or improving documentation, or when asked to draft, rewrite, review, condense, or expand technical prose.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Technical Writing

**IRON LAW: Never invent facts, APIs, numbers, or examples. If information is
missing, say so plainly or ask one focused question — do not fabricate to fill
the gap.**

## Overview

Help the target reader understand something quickly and take the right
action. Prefer simple wording, explicit structure, consistent terminology,
accessible presentation, and concrete examples.

## Workflow

1. **Identify the reader and outcome.** Infer who the reader is, what they
   already know, and what they need to do after reading. State the purpose
   early; narrow the scope if the request is broad.
2. **Choose the right document shape.**
   - Task-oriented structure for how-to guides, tutorials, and onboarding.
   - Concept → key points → examples for explanatory content and design docs.
   - Reference structure for APIs, commands, flags, schemas, and limits.
   - Tables only when comparison is faster than prose.
3. **Draft for clarity.** Common words over jargon unless the technical term
   is required. Active voice. Short sentences; split stacked clauses. Precise
   verbs and concrete nouns. Unambiguous pronouns — repeat the noun if needed.
   One term per concept, used consistently. Back strong claims with the
   evidence, observation, metric, trace, example, or constraint behind them.
4. **Organize for scanning.** Lead sections and paragraphs with the main
   point. Use informative headings that name a task or takeaway. Convert
   dense enumerations into lists with parallel structure. Put prerequisites,
   limits, and caveats before the reader hits them.
   - For the sentence- and paragraph-level skimmability discipline (topic
     sentences, active third-person voice, positive form, emphatic word order,
     deferred provenance), apply the `writing-for-humans` skill via the Skill
     tool if it appears in this session's available-skills list.
5. **Make examples earn their length.** Use the smallest realistic example
   that proves the point. Explain why it matters when that isn't obvious.
   Avoid irrelevant setup. Use anti-examples only when they clarify a likely
   mistake.
6. **Make it accessible.** No color-only references ("click the red
   button"). Meaningful link text. Alt text for informative images. Inclusive
   language. No dense screenshots or diagrams left unexplained in text.
7. **Write helpful error messages when relevant.** State what failed, why (if
   known), and exactly how to fix it — name the invalid value, required
   format, limit, or conflicting state. Keep the tone neutral and direct.
8. **Edit aggressively.** Remove filler, throat-clearing, and repeated
   context. Give each paragraph one clear job. Verify every term, command,
   filename, flag, and example. Cut any sentence that doesn't help the reader
   decide or act.
   - MAY invoke the `stop-slop` and/or `humanize-writing` skills via the Skill
     tool if either appears in this session's available-skills list, for a
     final pass over drafted or rewritten prose that strips AI writing tells
     (filler, hedging, buzzwords, formulaic structure). If neither is listed,
     rely on the Rewrite Heuristics and Review Checklist below instead.

## Default Output Pattern

For new documents, prefer this order: title, one-sentence summary, audience
or prerequisites, main sections in reader task order, examples, edge cases or
troubleshooting, then links to deeper reference material.

## Rewrite Heuristics

- Replace "allows you to" with the verb it's hiding.
- Replace abstract nouns with actions.
- Replace "simply", "just", "obviously", or "easy" with concrete instruction,
  or remove them.
- Replace long lead-ins with the point.
- Replace passive constructions when the actor matters.
- Define acronyms on first use unless the audience clearly already knows
  them.

## Review Checklist

- Can the target reader understand the first paragraph without extra
  context?
- Does each heading help someone scan to the right section?
- Are terms consistent throughout?
- Are commands, paths, and identifiers exact?
- Does each example earn its length?
- Are prerequisites and constraints explicit?
- Are strong claims backed by evidence, or clearly marked as assumptions?
- Does an error state explain recovery?
- Would this still work for a reader using assistive technology?

## Response Modes

- **Draft**: produce the requested document directly.
- **Rewrite**: preserve meaning; improve clarity and structure.
- **Review**: identify ambiguity, missing context, structural problems, and
  weak examples before suggesting edits.
- **Condense**: keep substance, remove redundancy.
- **Expand**: add missing prerequisites, examples, or caveats without bloat.

For Rewrite/Condense/Expand on an existing file, default to returning text
(or a diff) rather than overwriting on disk, unless the user explicitly asked
for an in-place edit.

## Style Guardrails

Concise, production-friendly wording. Don't over-explain obvious basics to
expert readers. No marketing tone unless asked.
