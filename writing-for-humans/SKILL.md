---
name: writing-for-humans
description: Structure human-facing prose so it reads clear and skimmable — topic sentences, one idea per paragraph, active third-person voice, positive form, parallel structure, deferred provenance, and a promotional-vocabulary blocklist. Use when drafting, editing, condensing, or reviewing documents people read — READMEs, design docs, ADRs, guides, tutorials, release notes, specs, or long-form comments. Complements technical-writing (document workflow) and stop-slop (AI-tell removal); other skills reach it for the skimmable-prose discipline.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Writing for Humans

Optimize human-facing prose for a reader **skimming**, not only for information
density. Keep the density and rigor — change the presentation so a human can
navigate it. Applies to documents people read — READMEs, design docs, ADRs,
guides, release notes, long-form comments — not chat replies or terse tool output.

## Structure

- One idea per paragraph, led by a topic sentence that states the point.
- Keep paragraphs to ~3–4 sentences and sentences to one main clause. Split
  qualification pile-ups instead of stacking em-dashes and nested parentheticals.
- Use headings, lists, and tables for genuine structure that aids navigation —
  never as a template to fill, never with nothing behind them. Never emit a
  broken or empty table.

## Sentences

- **Prefer active voice and third person.** Write "the function returns the
  parsed token", not "the parsed token is returned" or "you get back a token".
  Use passive only when the actor is unknown or irrelevant ("the file was
  deleted"); it is convenient and sometimes necessary, not banned.
- **State positively.** Assert what is, not what isn't: "he forgot" over "he did
  not remember"; "dishonest" over "not honest". Reserve *not* for genuine denial
  or antithesis, never for evasion.
- **Put the new element last.** End each sentence on the word you want emphasized —
  usually the new information, with known context first.
- **Keep coordinate ideas parallel.** Similar content takes similar grammatical
  form, so the reader sees the likeness.
- **Omit needless words.** Cut "the fact that", "there is/are … that", and
  "who is/which was" padding. Make every word carry meaning.

## Provenance

- Defer heavy provenance — dates, PR/issue numbers, commit hashes, caveats,
  sources — to a trailing clause, a footnote, or a dedicated Sources/Notes section.
- State the claim first, support it after. Don't inline every qualification into
  the sentence that makes the claim.

## Avoid AI tells

Cut generic, promotional, LLM-default vocabulary that carries no information:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy.
- **Empty "-ing" phrases:** ensuring reliability, showcasing features,
  highlighting capabilities.
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge.
- **Overused LLM vocabulary:** delve, leverage, multifaceted, foster, realm,
  tapestry.

Be specific, not grandiose — say what it does. For a full AI-tell pass (filler,
formulaic structure, rhythm, passive voice), run `stop-slop`; this list only
covers the promotional-vocabulary gap stop-slop omits.
