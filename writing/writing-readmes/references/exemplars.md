# Exemplar Patterns

Moves distilled from front doors that demonstrably read well, with the evidence behind each. Read this when
drafting or rewriting and you want a concrete shape rather than a principle.

## How to Read This File

Findings are graded by how much independent support they have:

- **Convention** — the same move appears in documents by unrelated authors. Treat as a default.
- **Choice** — exemplars diverge, and the divergence tracks something about the project. The condition matters
  more than the move.
- **Observed once** — a single instance worth knowing about, not yet a pattern.

One methodological warning, because it changes how much any single agreement is worth: two of the four sources
below are Azure-Samples repositories sharing a house template, down to near-identical prerequisite bullets and
closing legal sections. Where only those two agree, that is **one** data point wearing two hats, not two. Every
**Convention** below is supported across the two independent authors.

Sources are listed in [../ATTRIBUTIONS.md](../ATTRIBUTIONS.md). This file is open: adding an exemplar means
re-grading the findings, since a third independent author can promote a Choice to a Convention.

## Conventions

**Prove it works before asking for anything.** The two exemplars that lead with a demo — an animated GIF of
the finished product, placed above the fold, before any prose or install command — are the two that answer
"does this actually work" for free. The two that lead with installation were both independently identified as
weaker for exactly this: one has no visual proof anywhere despite being a real-time terminal tool whose whole
value is the live experience. This is the single strongest cross-author finding.

**Never ship a bare code block.** Both authors frame every snippet, by different mechanisms serving one
purpose: a sentence stating what the command does and why you are running it now, or a bold one-line label
above the block. The label form has a second benefit — a skimmer can read only the bold lines down the page
and still follow the sequence.

**Spend admonitions on skippable asides only.** Every exemplar that uses GitHub alerts uses them for context a
reader can safely ignore — a cost warning, a glossary aside, a faster alias — and never for a required step.
Skimming past an admonition must cost nothing. Both independent authors also use roughly one per document; a
wall of alert boxes reads as noise, one reads as considered.

**Put trust signals above the prose.** Badges sit immediately under the title, before the first sentence, and
cover a stable set of categories: build status, version, runtime requirement, licence, and one "try it
instantly" affordance. The categories transfer; the specific services do not.

**Defer or omit the legal and contribution block.** All four end on reader-facing content. Contributing,
trademarks and CLA text either sit in a short closing section after every reader question is answered, or are
absent entirely with the licence carried by a badge alone. None interrupts the document with them.

**Link an unfamiliar tool on first mention instead of describing it.** Prerequisite lists name and link each
tool rather than explaining it — the reader who knows it skips, the reader who does not gets the authoritative
source rather than a paraphrase that will rot.

## Choices

**Demo medium follows what the project actually does.** A visual or interactive result earns a GIF or
screenshot. A tool with no visual output substitutes a worked example with real output. The one exemplar that
substituted *navigation* for proof was flagged as having a gap, not a solution — an anchor-nav line is not
evidence.

**Opening shape follows what the project is.** A single concrete thing gets a capability statement that names
exactly what it builds. A collection or a pattern gets either a category label or a narrative hook that
recruits the reader as protagonist — *"Let's say you're a developer who has been tasked to…"* — before naming
any technology. The hook earns its length only when the value is abstract; a demonstrable tool should just
demonstrate.

**Collapse alternate paths when there are several equally valid ones.** Where a document offers three setup
routes, wrapping each in a disclosure element with only the recommended one open keeps the page short for
skimmers and complete for the person who needs route three. The exemplar that left all three expanded is
longer for every reader and better for none. Use this only for genuine alternatives — collapsing content the
reader needs hides it.

**In-page navigation is for flat, wide documents.** A single line of separator-joined anchor links under the
badges gives a long document a table of contents at almost no visual cost. Two exemplars use it. Keep it
honest: one of them lists fewer sections than the document contains, which quietly misrepresents the map. A
document whose structure escalates in depth can navigate by heading hierarchy instead.

## Named Moves

| Move                          | What it does                                                                                 | Use when                                         |
| ----------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Demo-before-install           | Proof of function precedes the ask for the reader's time                                     | Always, in whatever medium fits                  |
| Zero-to-working in N steps    | A numbered happy path — start, configure, verify — placed before the formal install section  | Setup is genuinely short and the payoff is fast  |
| `--help`-shaped options block | CLI flags rendered as a monospace block mirroring real `--help` output, not a Markdown table | Documenting a command-line interface             |
| Bold-label-over-snippet       | Each example self-describes in one bold line above its block                                 | A run of sibling examples a reader will skim     |
| Examples by scenario          | Worked examples grouped by the reader's situation, not by the tool's feature list            | The feature list is already documented elsewhere |
| Decision-aid subsection       | Two options contrasted side by side with an example each                                     | The reader must pick between two API surfaces    |
| Honest-limit redirect         | A closing section naming the alternatives and who should use them                            | Always — see below                               |
| Migration note in the README  | Breaking-change guidance inline, where a returning user looks                                | A released project with a version boundary       |
| Named exit ramps              | Learn-more, something-broke, and I-need-a-human as three separate sections                   | Enough audience to warrant it                    |
| Cost transparency up front    | Free-tier route stated before any resource-consuming path                                    | The project can bill the reader                  |

**The `--help`-shaped block deserves its own note**, because it inverts the usual advice to prefer a table.
Both independent authors reject the table for CLI flags, and the reason is drift: a fenced block reproducing
what the tool literally prints doubles as truthful evidence and can be regenerated, where a hand-maintained
table silently diverges from the binary.

**The honest-limit redirect is the highest-leverage move in this file.** One exemplar closes by listing
competing projects and who each suits. It costs the author nothing real and buys more credibility than any
claim in the document, because a front door that names its own boundary is the only kind a reader has grounds
to believe. It also answers a question every reader has and almost no README addresses.

## Observed Anti-Patterns

**A "Features" bullet list is the section most likely to answer nothing.** Two exemplars carry one and it was
independently flagged in both: in one it restates the overview in bullet form; in the other it is
category-label marketing phrasing that would describe any tool of its kind. Where features matter, show them
in the example or fold them into who the project is for.

**Prerequisites buried below the setup path.** One exemplar puts platform prerequisites four heading levels
deep, past its Getting Started section, so a reader can walk most of the setup before discovering a
requirement they cannot meet. Its sibling promotes the same content to the second top-level section. Surface a
blocking requirement before the reader commits effort.

**Heading depth past four levels.** One exemplar reaches five and becomes unnavigable by heading alone.

**Hedge-adjective taglines.** "Simple yet powerful" is a cliché that survives into an otherwise strong
document. A concrete verb phrase naming what the thing does outperforms any adjective pair.

**Hand-picked does not mean clean.** These documents contain a malformed nested link, an incomplete navigation
line, and at least one non-native grammatical construction. Copy the moves, not the fragments, and do not
assume anything in an admired document was deliberate.
