---
name: deep-research
description: Research one subject exhaustively from external sources, following every thread through documentation, standards, source code, papers, patents, datasheets, and archives, and report a cited synthesis with its open threads. Use when asked to dig into, research thoroughly, or find everything about a subject, to settle a question no single lookup answers, or to judge an open-source project before adopting it. Not for one authoritative lookup or the current repository's own code.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Deep Research

Research a subject until its threads run out, not until a first answer appears. A thread is anything a source points
to that might hold more: a reference, a cited work, a name, a part or patent number, a later version, or a term the
source leaves unexplained. The richest material often sits outside ordinary web results, in patents, standards,
datasheets, source code, issue trackers, mailing lists, and archives.

## Choose the Branch

- **Exhaustive research**, the default: follow steps 1 to 6.
- **Settle a question** between rival answers: follow steps 1 and 2, then [Settle a Question](#settle-a-question),
  then steps 4 to 6.
- **Judge a project to adopt**: follow [Judge a Project to Adopt](#judge-a-project-to-adopt) within the steps.

## 1. Map the Subject

Open the notes file before the first search, in the format [references/research-notes.md](references/research-notes.md)
gives, where the repository keeps temporary work, or else in `.scratch/<date>-<task>/research/`. It holds the map, the
thread register, and the query log, so the work survives a lost context.

List the subject's facets: the parts, entities, mechanisms, periods, and languages a complete account covers. Give each
facet the question it must answer. When the user gives no budget for an exhaustive run, agree one in sources or time
and record it.

The map is done when every facet has its question and a status of open.

## 2. Start Wide

Begin with short queries of a few words, from several kinds of source per facet, before narrowing. Search where web
search does not reach: patent databases, standards bodies, code search, paper indexes, mailing-list archives, and the
Wayback Machine. Search each relevant language. Log every query with where it ran, and never repeat one.

When the harness allows subagents, give independent facets to parallel lanes, as `dispatching-subagents` describes. A
lane running this skill does its own reading.

## 3. Follow Every Thread

Add each thread to the register as you meet it. Work in rounds: in each round, follow every open thread once, then
record its status as followed, dead end, or parked, with the reason.

- **Backward:** the references, prior art, and sources a work cites.
- **Forward:** the works that cite it, later versions, patent family members, errata, and fixes.
- **Sideways:** other work by the same author, inventor, company, or project.
- **To the origin:** trace every claim to the source that first made it, past summaries and copies.

Decide whether a source is relevant before chasing from it, and record each dead end so nobody searches it again. When
a source is paywalled or blocked, try an archive copy, a preprint, an author's copy, or a mirror. Park it as blocked,
with its URL, when none works.

## 4. Weigh the Evidence

Count a claim's independent origins, not its URLs: press releases, copies, and aggregators repeating one source count
as one. Prefer primary sources, date every claim, and treat a conflict between sources as a finding to report. Give
each major claim a confidence level with its basis.
[references/source-evaluation.md](references/source-evaluation.md) holds the warning signs, the conflict rules, and the
confidence wording.

## 5. Stop on Evidence

Research is done when all of these hold:

- every thread in the register is followed, a dead end, or parked with its reason;
- the last full round found nothing new for any facet;
- a check by a different route finds nothing new, such as another index or a citation chase from what you found;
- every facet holds evidence, or a recorded "searched, found none".

Before stopping, reread the map and name the thinnest facet and the source you trusted most. Then decide whether either
needs another round. When the budget runs out first, park every open thread with "budget" as its reason.

## 6. Report

1. **Synthesis**, by facet: what is established, with the sources for each load-bearing claim.
2. **Confidence** for each major claim, keeping fact, inference, and open conflict apart.
3. **Open threads**: each parked thread with its reason, such as budget, blocked, low value, or out of scope.
4. **Notes file**: its path.

## Settle a Question

1. List every plausible answer, including those you doubt.
2. For each piece of evidence, mark which answers it fits. Weigh evidence that separates the answers over evidence
   they all fit.
3. Try to disprove each answer rather than confirm it. An answer without support stays open until evidence rules it
   out.
4. Check how the conclusion changes if the few most important pieces of evidence were wrong.

Report every answer still standing, with the evidence that would change the conclusion.

## Judge a Project to Adopt

Give two separate verdicts:

- **Fit:** does the mechanism do what the need requires? Judge it from the code that implements it, not its README.
- **Soundness:** is it safe to depend on? Judge its tests, failure behaviour, maintenance, and licence as a whole.

Treat popularity and age as hints, never as a verdict: a newcomer that fits better wins on that fit. Messy code, an
unfamiliar style, or AI authorship counts against a project only when tests and evidence that it works do not offset
it. When the mechanism fits but the project is not sound to depend on, recommend extracting the pattern, and cite the
code path that shows it.
