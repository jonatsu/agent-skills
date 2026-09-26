---
name: context-compression
description: Compress model-bound reference context or accumulated session state to a stated budget while preserving task-relevant facts, relationships, authority, and uncertainty. Use when supplied context must become materially smaller for another LLM call; not for ordinary human-facing editing, handoff writing, prompt repair, or exact-source preservation.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Context Compression

Compress context for a known downstream model task. The compressed text is lossy, so retain the original
source through validation. When later recovery may be needed, provide an exact reference the downstream
consumer can access. Plausible compressed text is not proof of equivalent meaning.

Optimize total tokens needed to complete the downstream task, including re-reading, rather than minimizing
this one input at any cost.

## Establish the Compression Contract

Before deleting content, identify:

- the downstream task and consumer;
- the target size, token budget, or constraint that makes compression necessary;
- facts, relationships, wording, or spans that must survive exactly;
- acceptable loss, if any; and
- where the source remains retrievable during validation and later recovery.

Ask for a missing task or consequential preservation requirement. When only the exact budget is missing, a conservative
first pass may proceed if the source remains available; state the achieved size instead of inventing a target.

Route by the requested deliverable:

- use `handoff` when the deliverable is a continuity brief for another session, agent, machine, or person;
- use `prompt-optimizer` when observed behavior requires changing prompt instructions; and
- use a writing skill when editing human-facing prose for clarity or concision.

Do not compress text whose exact form is the evidence or interface unless the user explicitly authorizes a separate
lossy representation. This includes quotations, source records, code, schemas, commands, tool definitions, policies,
licenses, and signed or regulated text.

## Reduce in Least-Lossy Order

Try these operations in order. Measure after each one; stop reducing when the result meets the budget, then
validate preservation:

1. Remove material irrelevant to the downstream task.
2. Deduplicate repeated facts and explanations.
3. Replace bulky retrievable material with an exact reference plus the finding needed now.
4. Encode repeated relationships with headings, labels, lists, or tables.
5. Delete predictable grammatical scaffolding under the rules below.
6. Abstract or generalize content only when the budget still requires it and the contract permits the loss.

Do not summarize a file merely because it is large. A searchable source reference can be both smaller and more faithful.

## Delete Grammar Deliberately

Models often understand compact fragments, but grammatical categories are only deletion candidates. Delete a token or
rewrite a phrase when the remaining wording or structure still encodes its task-relevant meaning.

### Usually Safe to Remove or Rewrite

- Empty frames: `it is important to note that X` becomes `X`; `there are three failures` becomes `Failures: 3`.
- Wordy equivalents: `in order to` becomes `to`; `due to the fact that` becomes `because`.
- Redundant emphasis: delete `very`, `really`, or similar intensifiers when degree is not evidence or user intent.
- Articles `a`, `an`, and `the` in unambiguous labels and fragments: `the retry policy` may become `Retry policy`.
- Copulas `am`, `is`, `are`, `was`, `were`, `be`, `been`, and `being`, plus expletive subjects, when a label carries
  the relation and any task-relevant time: `status is blocked` becomes `Status: blocked`.
- Complementizer `that` when the clause boundary remains clear: `logs show that retry failed` becomes
  `Logs show retry failed`.
- Relative pronouns `which`, `that`, `who`, and `whom` when their clauses can become modifiers:
  `artifact that was generated` becomes `generated artifact`.
- Nominalizations: `made a decision to retry` becomes `decided to retry`.
- Passive voice when the source identifies the agent: `was approved by Mina` becomes `Mina approved`.
- Repeated subjects in parallel lists when the heading supplies the subject.

### Remove Only with an Explicit Replacement

- Pronouns such as `it`, `this`, `that`, `these`, `those`, `he`, `she`, and `they`: replace an ambiguous pronoun with
  its noun before considering deletion.
- Tense and aspect: move the time or state into a label such as `Completed`, `Current`, or `Proposed`.
- Auxiliaries such as `have`, `has`, `had`, `do`, `does`, and `did`, and infinitive `to`: remove them only when a label
  or imperative preserves tense, aspect, and the verb's role.
- Prepositions such as `of`, `for`, `to`, `in`, `on`, `at`, `by`, `with`, `without`, `between`, `among`, `within`,
  `after`, `before`, `over`, `under`, `through`, and `from`: remove them only when layout or labels preserve ownership,
  agency, inclusion, direction, location, and time.
- Conjunctions `and`, `or`, and `but`: use labeled lists such as `all of` and `one of` when layout replaces the
  words. Retain an explicit contrast marker when it changes the decision.

### Preserve Unless an Equivalent Marker Remains

- negation and exclusions: `not`, `no`, `never`, `without`, `except`;
- authority and modality: `must`, `must not`, `may`, `may not`, `should`, `required`, `allowed`, `prohibited`;
- quantities, units, ranges, approximations, and comparison operators;
- conditions, causes, consequences, and exceptions;
- alternatives, conjunction requirements, and contrasts;
- chronology, deadlines, duration, frequency, and current versus historical state;
- uncertainty, attribution, evidence status, and confidence;
- ownership, agency, direction, containment, and scope;
- proper names, identifiers, paths, commands, error text, hashes, and version strings; and
- user corrections, accepted decisions, open questions, and unresolved risks.

For example:

```text
Original: It is important to note that there are three cache entries that are currently invalid.
Compact:  Current invalid cache entries: 3.

Original: Migration may start after approval A or B, but it must not continue without a verified backup.
Compact:  Migration: may start after approval A or B; must not continue without verified backup.
```

The second result retains permission, sequence, alternatives, contrast, prohibition, and the backup condition.
`Migration start: approval A B` loses them.

## Preserve Changing State

For repeated compaction, process the newly removed span and reconcile it with the existing compressed state. Do not
regenerate the whole summary by default, because repeated summaries can silently erode older details. Do not merely
append either: mark replaced decisions and completed work as superseded while retaining the current authority and the
reason for the change.

Separate stable facts from current state. Preserve exact artifact identifiers in an index when later work depends on
them. A useful coding-session state may include objective, constraints, files changed, decisions and rationale, current
failures, verification evidence, risks, and next action. Include only fields the downstream task needs.

## Measure and Validate

Use the target model's tokenizer when one is available. Otherwise report characters, words, or an explicitly labeled
token estimate. Never present a proxy as an exact token count.

Validate the result against the source before discarding or hiding anything:

1. Check protected spans and exact identifiers mechanically where possible.
2. Ask task-specific recall questions covering facts, relationships, authority, uncertainty, and exclusions.
3. Test the downstream decision or continuation that the context must support.
4. Compare failures and re-fetching against the original context or an uncompressed control when the decision matters.

A single fatal loss overrides an average score. If a required constraint, relationship, or exact value is missing or
changed, restore it and reduce compression elsewhere. Treat invented facts and false certainty as failures even when the
output fits the budget.

Deliver the compressed context with the measured reduction, the source reference when available, any intentional
omissions, and validation performed. State untested fidelity instead of calling the result equivalent.
