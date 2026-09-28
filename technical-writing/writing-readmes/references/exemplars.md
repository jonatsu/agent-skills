# Exemplar Patterns

Craft distilled from nine front doors that read well, with the evidence behind each. Read this when drafting or
rewriting and you want a concrete rule rather than a principle.

## How to Read This File

Nine documents by seven independent authors. Findings are graded by how much independent support they have:

- **Convention** — the same move appears across unrelated authors. Treat as a default.
- **Choice** — the exemplars diverge, and the divergence tracks something about the document. The *condition*
  matters more than the move.
- **Observed once** — worth knowing, not yet a pattern.

Two of the nine are Azure-Samples repositories sharing a house template, down to near-identical prerequisite
bullets; where only those two agree, that is one data point wearing two hats. Sources are listed in
[../ATTRIBUTIONS.md](../ATTRIBUTIONS.md).

**The single finding that organizes everything else:** length and decoration are not defects. *Undirected*
length and decoration that answers no reader question is. Every heavy device across these nine — badge rows,
tables of contents, centered mastheads, HTML tables, domain primers — traces to a specific problem the
surrounding content created. None appears because READMEs have one. Minimalist advice applied literally to
these documents would force cutting either real content or the aid that makes the content navigable.

## Decision Rules

SKILL.md states each device's trigger. This section holds the evidence behind it and the finer form detail,
derived from where the exemplars diverge, not from where they happen to agree.

### Table of Contents

In the exemplars, the three-screen trigger meant **six or more top-level sections**, at least one with enough
sub-items to jump past siblings.

The *form* follows how self-explanatory the section titles are:

- **Bullet list** where titles convey their content on their own.
- **Horizontal separator-joined nav row** for a short, flat document. One exemplar with eleven mostly-short
  sections chose this over a vertical list — its authors judged a full list excessive at that length.
- **Two-column table with a one-line gloss per entry** where titles like "Pipeline" or "Results" do not
  self-explain.

*Placement* follows where linear reading stops being enough. Usually right after the opening block — never
above it, because the top belongs to identity, not navigation. One exemplar deliberately puts its TOC 40% down
the page, after a domain-literacy preamble: the document has a linear-read zone and a lookup zone, and the TOC
marks the boundary.

A curated top-of-document link row is a **different device** from a TOC, and the two coexist. The row is a
hand-picked subset — the two or three highest-intent jumps, typically Install and a demo — and should omit
anything the TOC already serves.

### Badges

No exemplar exceeds five badges in a row. Past about six they stop being scannable.

The absence of a badge is as deliberate as its presence. A config-file project carries no CI badge because it
has no build; one exemplar leaves its build badge commented out in source rather than advertising a check it
does not trust. Where a project has several genuinely distinct trust questions, **split into categorized
rows** — environment, then CI and quality, then community and licence — rather than one undifferentiated
lump. A bare star count carries no checkable fact and is the weakest instance observed.

### Centered Masthead and HTML

The stacked cluster behind a centered masthead is title, link row, badges, and hero image. One exemplar
left-aligns because prose starts within a line or two of the title, and loses nothing: its content is dense
text and code where centering adds no clarity.

Real HTML instances across the set — grouped badge rows, a `<table><td>` used as a bordered content box,
`<br>` forcing a line break inside a table cell, `<div align="center">` wrapping a Markdown table,
`<img width>` signalling relative importance, manual `<a id>` anchors recreating footnotes.
"Avoid HTML in READMEs" does not survive contact with these documents.

### Humor

Two authors arrive independently at SKILL.md's humor rule. One confines it entirely to the sections about the
project's philosophy and community, and it is wholly absent from features, prerequisites, install and
troubleshooting. The other threads it through each command's lead-in, then drops immediately into a dry,
joke-free list of exactly what the command does.

## Conventions

**Prove it works before asking for anything.** Every exemplar that leads with a demo — a GIF, a screenshot, a
hero image — answers "does this actually work" before the first sentence of prose. The ones that lead with
installation were independently flagged as weaker for it, including one real-time terminal tool with no visual
proof anywhere. The strongest cross-author finding in the set.

**Badges and a tagline precede any structural apparatus.** Identity first, navigation second, content third.

**Every code block is framed.** Every author frames every snippet, with a sentence or a bold one-line label.

**Admonitions carry skippable asides, at calibrated levels.** Alerts carry cost warnings, glossary asides,
compatibility notes — never a required step, so skimming past one costs nothing. One exemplar uses three
distinct alert levels for three severities rather than repeating one.

**Front-load a trust or legal clarification, ahead of the pitch.** A domain-squatting warning above the title;
a non-affiliation disclaimer under it. Where a reader could reasonably be misled about what they are looking
at, resolve it before selling anything.

**Push licence, contributing and support to the bottom.** All nine. None interrupts the document with them.

**An unfamiliar tool is linked on first mention, not described.** The reader who knows it skips; the one who
does not gets the authoritative source instead of a paraphrase that will rot.

## Choices

**Demo medium follows what the project does.** A visual result earns a GIF; a hardware project earns numbered
figures; a text tool substitutes a worked example with real output. One exemplar embeds a **separate GIF per
command** rather than one hero recording — costlier to keep current, but it proves each claim rather than the
product's existence.

**Opening shape follows what the project is.** A single concrete thing gets a capability statement naming
exactly what it builds. A collection or a pattern gets a category label or a narrative hook recruiting the
reader as protagonist. One exemplar has no tagline at all and defers the whole "what is this" job to its
introduction — viable only where the title and hero image already carry it.

**Feature-bullet grammar follows what the reader is doing.** Terse noun-phrase fragments for an audience
scanning capabilities fast; command-plus-rhetorical-question for an audience that must first be convinced a
specific annoyance is being solved. The second does not scale — one exemplar keeps it to three flagship
examples plus a catch-all, and it would exhaust a reader across twenty.

**Register follows audience expertise.** Terse and assumption-heavy for a developer tool; informal and
emphasis-heavy for hobbyists; academic with real inline citations for a project whose readers need domain
credibility before they can judge fit.

**Teach the domain first where the reader cannot otherwise judge fit.** One exemplar runs three "what is X?"
primers ahead of everything actionable, including ahead of its TOC. This contradicts get-to-the-point advice
and is correct for its audience — but it offers no skip-to-install path for a reader who already knows the
domain, which is the cost.

**Collapse alternate paths when there are several equally valid ones**, with only the recommended one open.
Notably, most of these exemplars use no disclosure elements at all and manage length through heading hierarchy,
reference-style links and section dividers instead.

## Named Moves

| Move                                     | What it does                                                                                                  | Use when                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Demo-before-install                      | Proof of function precedes the ask for the reader's time                                                      | Always, in whatever medium fits                        |
| Zero-to-working in N steps               | A numbered happy path placed before the formal install section                                                | Setup is short and the payoff is fast                  |
| Tiered help escalation                   | Closing ordered by response latency: in-tool help, then diagnostics, then FAQ, then issue search, then humans | Any project with users who will get stuck              |
| Anticipated-objection dialogue           | State the reader's skepticism verbatim, answer it with a concrete scenario                                    | The project resembles something the reader already has |
| Front-door scoping CTA                   | Say explicitly, before the first heading, that the full manual lives elsewhere                                | A real documentation site exists                       |
| Checklist-as-pitch                       | List the reader's own requirements as bullets, then claim the boxes                                           | The reader can self-qualify                            |
| Comparison table vs named alternatives   | Feature grid with a competitor column                                                                         | Differentiation is the reader's actual question        |
| Honest-limit redirect                    | Closing section naming the alternatives and who each suits                                                    | Always                                                 |
| `--help`-shaped options block            | CLI flags as a block mirroring real `--help` output, not a table                                              | Documenting a command-line interface                   |
| Bold-label-over-snippet                  | Each example self-describes in one bold line above its block                                                  | A run of sibling examples a reader will skim           |
| Lifecycle section for the returning user | "Updating" as a first-class section, branching on whether they customized                                     | A released project people re-visit                     |
| Named safety subsection                  | A real heading naming the risk and its consequence, not a buried footnote                                     | The tool can destroy or leak something                 |
| Reference-style links at the foot        | `[label][ref]` in prose, resolved in one block at the end                                                     | Long prose-heavy documents                             |
| Elided real example                      | Genuine config with `...` marking omission                                                                    | A synthetic toy example would misrepresent the shape   |
| Annotated directory tree                 | Fenced tree with a trailing comment per meaningful line                                                       | Layout is part of what the reader must learn           |
| Per-section emoji as TOC glyph           | Same emoji in the heading and its TOC entry                                                                   | The TOC is long enough to want visual scanning         |
| Logo-as-download-link                    | The masthead graphic *is* the primary CTA                                                                     | There is one obvious primary action                    |

**The tiered help escalation is the highest-leverage closing in the set.** Not "see the docs" but an ordered
path from cheapest to slowest — in-tool help keys, a built-in diagnostic command, the FAQ, issue search, then a
human channel. It teaches a reflex rather than handing a link, and the last thing the reader learns is how to
get unstuck without leaving the product. Exemplars that close on "PRs welcome" were rated perfunctory beside
it.

**The honest-limit redirect costs nothing and buys the most.** One exemplar closes by naming competing projects
and who each suits. A front door that names its own boundary is the only kind a reader has grounds to believe,
and it answers a question every reader has that almost no README addresses.

## Observed Anti-Patterns

**A "Features" bullet list is the section most likely to answer nothing.** Flagged independently in two
exemplars: in one it restates the overview in bullet form, in the other it is category-label phrasing that
would describe any tool of its kind. Where features matter, show them in the example or fold them into who the
project is for.

**A blocking prerequisite below the setup path.** One exemplar buries platform prerequisites four heading
levels deep, past Getting Started; another puts Requirements after six usage sections. Surface anything that
can stop the reader before they commit effort.

**Heading depth past four levels** becomes unnavigable by heading alone.

**A navigation aid that lies.** Two exemplars have link rows or TOCs omitting real sections, so a reader
skimming the map never learns those sections exist. If you draw a map, make it complete or make its partiality
obvious.

**Hedge-adjective taglines.** "Simple yet powerful" survives into an otherwise strong document. A concrete verb
phrase naming what the thing does beats any adjective pair.

**Hotlinking images from domains you do not control.** One exemplar's hardware table depends on stock-photo and
e-commerce URLs that will rot silently.

**Duplicated sections from an unfinished edit**, inconsistent divider usage, a path typo, a bibliography entry
never cited. Every one of these is present in a hand-picked exemplar. **Copy the moves, not the fragments** —
nothing in an admired document is guaranteed deliberate.
