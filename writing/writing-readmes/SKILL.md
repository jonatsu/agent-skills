---
name: writing-readmes
description: "Write, rewrite, or judge the quality of a project's front door: a README, quickstart, getting-started page, or documentation landing page, so a stranger sees the point and can start. Use when a README reads flat, generic, or template-filled, when a project needs one from scratch, or when asked whether one is any good. Not for tutorials, how-to guides, references, runbooks, or decision records, which are writing-documentation. Not for checking whether a README's claims still match the repository, or for scaffolding baseline repository files, which are repo-management."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing READMEs

Use this skill for a project's front door: the README, the quickstart or getting-started page, the
documentation landing page. A front door is the first thing a stranger reads about the project, and it is
judged in about ten seconds by someone who has not decided to care yet.

That deadline is what separates this skill from its neighbours. Every other document is read by someone who
already chose the project.

- `writing-documentation` owns tutorials, how-to guides, references, explanations, runbooks and decision
  records — and reviews documents for structure and accuracy.
- `repo-management` owns repository scaffolding, the README templates and audience matrix, and the accuracy
  audit that checks a README's claims against the tree. Route "are these commands still real?" there.
- `writing-for-humans` owns the sentence and the paragraph. Apply it to whatever this skill produces.

A review request splits by what is being judged: **does it read well** is this skill, **is it still true** is
`repo-management`'s audit. A thorough review wants both.

## Iron Law

**Every section answers a reader question, or it goes.**

A front door is not a form to complete. Sections do not earn their place by being conventional, by appearing
in a template, or by existing in the last project's README. A section earns its place by answering something
the reader is actually asking at the moment they reach it — and nothing else does.

This is the rule that a section checklist cannot give you, and its absence is why generic READMEs happen:
given a list of sections, an agent fills all of them, and the result is uniformly flat because nothing in it
was chosen.

## The Five Questions

A stranger works through these in order. They abandon the page at the first one that goes unanswered.

1. **What is this?** One sentence, concrete, no metaphor. They should be able to repeat it to a colleague.
2. **Is it for me?** Who it serves, what problem it solves, and — the part most READMEs skip — what it does
   not do and who should use something else.
3. **Does it actually work?** Evidence before claims. Output, a screenshot, a real example with a real result.
4. **How do I start?** The shortest path from nothing to a working result.
5. **Where do I go next?** Pointers onward, one line each.

Order sections by these questions rather than by convention. Any candidate section maps to one of the five or
gets cut — that is the Iron Law applied.

Two consequences worth stating, because they are commonly got wrong:

- **Question 3 comes before question 4.** A reader who is not yet convinced will not run your install command.
  Show the thing working, then tell them how to get it.
- **Question 2 requires a limit.** A front door that claims no boundary reads as marketing, and a reader who
  discovers the boundary after installing is angrier than one who was told. Naming the alternatives and who
  each suits costs nothing and buys more credibility than any claim you can make about yourself.

A released project has a sixth reader the five questions miss: the **returning user**, asking *what changed
for me*. They look in the README, not the changelog. Where a version boundary breaks something, keep the
migration note here.

## Answer Question 1 in the First Five Lines

The opening is the whole document's fate. Write it last, once you know what the project actually is, and hold
it to:

- **A title, then one sentence.** Not a paragraph. The sentence names what the thing is and what it is for,
  in the reader's vocabulary rather than the implementation's.
- **No preamble.** Do not open with the problem domain's history, with "In today's world", or with a
  restatement of the project name as a definition.
- **No unexplained jargon.** A term the reader must already know to parse the first sentence has cost you
  the reader.

Test it by deleting everything after the first five lines and asking whether a stranger could say what the
project is and whether it is for them. If not, the opening is not carrying its weight, no matter what follows.

## Show It Working Before Asking for Anything

Concrete evidence answers question 3 and no amount of description substitutes.

- A short, real, copy-pasteable example with its actual output.
- A screenshot, terminal recording or diagram where the result is visual.
- Real values, not `foo` and `bar`. Invented placeholder data reads as a project nobody has run.

Keep it minimal. Strip setup that does not affect the result. One example that runs beats three that
illustrate.

**Never ship a bare code block.** Every snippet carries either a sentence saying what it does and why the
reader is running it now, or a bold one-line label above it. The label form lets a skimmer read only the bold
lines and still follow the sequence.

**Surface a blocking prerequisite before the reader spends effort**, not inside the setup section where they
find it half-committed. Anything that can stop them — a platform requirement, an account, a cost — belongs
above the first instruction.

Never invent output. If you cannot verify what the command prints, say so and leave the example unpadded
rather than fabricating a plausible transcript.

## Cut Hard

Common sections that usually answer nothing, and what to do instead:

| Section                             | Verdict                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| Contributing, Changelog             | One-line pointer to the file. The prose belongs in `CONTRIBUTING.md`.                |
| License                             | One line naming the licence and linking `LICENSE`. Never the text.                   |
| Table of contents                   | Only past roughly two screens; otherwise it is furniture.                            |
| Features, as a bullet list of nouns | Fold into question 2, or show it in the example instead.                             |
| Roadmap, Acknowledgements, Author   | Only where a reader's decision depends on it.                                        |
| Badges                              | Only where they report live state a reader would act on.                             |
| CLI options, as a Markdown table    | Use a fenced block mirroring real `--help` output — it cannot drift from the binary. |

A front door that links out is doing its job. Length is not thoroughness — every line the reader must scan
past to reach question 4 is a cost.

## Decoration Is Off by Default

Emoji, badges, logos, admonitions and ASCII art are permitted, not standard. Apply them when the user asks,
or when the surrounding documentation set already uses them and consistency is the stronger claim.

Otherwise leave them out. Decoration must carry information a sentence otherwise would; decorating a
structureless README yields a decorated structureless README, and the fix for flat writing is never texture.

When the target renderer is known to be GitHub, admonitions (`> [!NOTE]`, `> [!WARNING]`) are available for a
genuine hazard. They degrade to blockquotes elsewhere, so do not rely on them off GitHub.

## Match the Set Before Imposing a Default

When the project already has documentation, infer its conventions before drafting: heading style, register,
example density, decoration. Two documents make a convention; one is a coincidence.

An evidenced house convention outranks this skill's defaults for anything it covers. Consistency across a
project serves a reader more than one improved page. `writing-documentation` carries the fuller method for
building a style profile.

## Modes

- **Draft.** Establish what the project is and who it serves before writing a line. Where that is not
  recoverable from the repository, ask rather than guess — an invented purpose is the one error nothing
  downstream repairs.
- **Rewrite.** Diagnose first, in the terms of the five questions: which are unanswered, which are answered
  out of order, which sections answer nothing. Show the diagnosis before producing the replacement. Preserve
  every accurate claim; this mode changes the framing, not the facts.
- **Critique.** Report against the five questions and the Iron Law, worst first, each finding naming the
  reader question it fails. Judge quality only, and route factual verification to `repo-management`. Do not
  edit the file unless the user asked for a rewrite.

For an existing file, return the text or a diff unless the user asked for an in-place edit.

## Review

- Can a stranger answer "what is this" and "is it for me" from the first five lines alone?
- Is there concrete evidence it works, before the install instructions?
- Does the document state what the project does not do?
- Can a reader get to a working result from the shortest path shown, without leaving the page?
- Does every section map to one of the five questions?
- Are Contributing, Changelog and License pointers rather than prose?
- Is every example real, with real values and unfabricated output?
- Is decoration either absent or justified by the surrounding set?

Read [references/exemplars.md](references/exemplars.md) for worked patterns distilled from front doors that
demonstrably read well, and the moves behind them.
