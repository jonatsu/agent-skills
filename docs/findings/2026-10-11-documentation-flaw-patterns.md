# Documentation Flaw Patterns

Date: 2026-10-11. Status: the rules are in place; the dash sweep (pattern 16) remains in `TODO.md`.

These are recurring flaws in agent-written documentation. The repair of every skill's `ATTRIBUTIONS.md` surfaced
them, and the author has seen the same patterns in agent-written documentation generally, most of all in
technical docs. The rules that prevent them live in `writing-documentation`, `context-architecture`'s writing
rules, `skill-forge`'s provenance guidance, the `agents-context-docs` instruction-file template, and this
repository's `AGENTS.md`. `writing-for-humans` already covered the sentence-level patterns (8, 14, and 16).

Each pattern names what goes wrong, an observed example, and the fix.

## Patterns

01. **Work ledger in a durable document.** A reference document narrates the work done on its subject: repairs,
    reviews, investigations, sessions, and the dates they happened. Example: "The 2026-09-07 repair retained useful
    task boundaries while replacing…". The fix is to state the current state only. Git history and the
    repository's ledgers hold the work.

02. **Negative-result records.** The document lists what was checked and found irrelevant, or how thorough a
    check was. Examples: a "Present but not established" section about a deck that turned out unrelated; a "Scope
    of this investigation" section. The fix is to record only what bears on the subject.

03. **Volatile identifiers.** The document pins material with values that change whenever it is regenerated,
    such as the SHA-256 of a PDF rebuilt on every upstream update. The fix is a stable identifier: a release,
    tag, or commit, the version the material embeds, or the date it carries. A date that pins an observation of a
    moving target, such as a measurement on a branch, is evidence rather than narration; replace it with a commit
    pin when the record holds one, and keep it otherwise.

04. **References a reader cannot inspect.** Examples: the author's deleted or absorbed skills, commits in a
    private repository, an internal port brief. The fix is to cite only what a reader of the published document
    can reach, and to drop the rest.

05. **Policy restated in each instance.** Every file of a kind repeats the rule that governs it, such as a "These
    records are permanent" paragraph in each attributions file. The fix is to keep the rule once, in the
    repository's rules, and let instances follow it silently.

06. **Key fact buried in prose.** The fact a reader scans for sits mid-paragraph, such as a license declared in
    the third sentence. The fix is to lead with it, or to give it a field of its own.

07. **Grouping by history instead of by kind.** Sections sort content by when or why it was gathered, such as
    "Third-Party Cases Used During the Repair" beside an ordinary source list. The fix is one structure grouped
    by what the content is.

08. **Restating what the document already says.** Prose repeats the header or a structured field: "because the
    content license conflicts with this package's license" when the package license is at the top, or "the paper
    is under CC-BY-4.0" right below a `License` bullet saying so. The fix is to say each fact once.

09. **Lists of what was not done.** The document enumerates what it did not take or cover, such as "its plan
    loop, ledger, and scripts are not retained". The fix is to state what is, and to keep an exclusion only
    when a reader would otherwise assume the opposite.

10. **Inventory instead of summary.** One sentence carries a dozen items when the reader needs the three main
    ideas. The fix is to summarize to what the reader needs.

11. **Change lists in place of a relationship.** The document itemizes each modification made to adapted
    material instead of naming the kind of adaptation in a clause. The fix is one clause, such as "vendored and
    adapted to call the installed CLI".

12. **Pointers that carry the narrative.** A sentence elsewhere that points at the document repeats its
    history: "see `ATTRIBUTIONS.md`, including a 2026-09-07 finding that…". The fix is one neutral pointer
    sentence.

13. **Unrequested structure.** Sections or tables nobody asked for and no reader question needs, such as
    per-file provenance and "Composition" tables. The fix is to let each section answer a question a reader
    has.

14. **Defensive argumentation.** The document argues its own legitimacy, such as "No infringement finding is
    made here or was made before". The fix is to state the facts and let them stand.

15. **Over-broad cleanup rules.** The opposite failure, seen while fixing the above: dropping a whole
    "verification-only" section also dropped extensive first-party source reading that deserved an entry. The
    fix is to judge each item by its impact, not by its section label.

16. **Dashes as default punctuation.** Em and en dashes appear throughout `SKILL.md` files where a comma, colon,
    semicolon, or parentheses would do, and where no grammatical need exists. The writing skills allow a dash
    only when correctness requires one. The fix is to rewrite each such dash with the punctuation the clause
    relationship calls for, and to keep a dash only for a real range or a case grammar demands.

17. **Reconstructed precision.** An agent tidying a record replaces a vague value with a precise one it derived,
    such as pinning a source to "the last commit before the read date" when no commit was recorded. The result
    looks authoritative and claims something nobody observed. The fix is to keep the precision the evidence
    supports: a recorded pin, or else the read date.

## Instances Outside the Attribution Files

The repair touched only `ATTRIBUTIONS.md` and the sentences pointing at it. Three suspected instances elsewhere were
resolved afterwards:

- Dated measurement notes in the Yocto security skills' references were evidence pins, not work narration (pattern
  3, and a near miss for pattern 15). Six now name `meta-security` commit `b13f170`, the revision the build probe in
  agent-setup's `docs/research/yocto-security/` ran against. The seventh, "NVD feed of 2026-09-05" in
  `report-coverage-audit.md`, is sample report text and stays.
- A factual error: `chain-of-trust-wiring.md` warned that meta-avb's license "reports as `NOASSERTION`". The layer's
  `LICENSE` is the MIT text with a non-standard copyright line, which GitHub's detection does not match. The
  reference now says the layer is MIT-licensed.
- A work narrative in `tools/git-commits-and-recovery/LICENSE.upstream`'s own header, which said when the worktree
  material moved. The header now names "earlier revisions" in the past-tense form; the license texts are unchanged.
