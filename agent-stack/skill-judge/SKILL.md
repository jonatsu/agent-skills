---
name: skill-judge
description: Evaluate an agent skill's design quality with a scored rubric — 8 weighted dimensions, a 120-point total, a knowledge-delta scan, and an improvement report. Use when reviewing, auditing, grading, or improving a SKILL.md or skill package, or when asked "is this skill any good", "score this skill", or "how do I make this skill better". Complements skill-forge (authoring) and writing-great-skills (vocabulary); this is the grading lane.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Skill Judge

IRON LAW: Score against **knowledge delta**, never polish. A well-formatted skill
that explains what the model already knows is a bad skill. Length, tone, and
structure never earn points on their own — only knowledge the model lacks does.

Grade an existing skill and return an actionable report. This is the review lane
for skills; `skill-forge` authors them, `writing-great-skills` supplies the
vocabulary (leading word, no-op, duplication, progressive disclosure, freedom
calibration) — consult it rather than re-deriving those concepts here.

## The core measure

> Good skill = expert knowledge the model lacks − what the model already knows.

A skill's value is its **knowledge delta**: decision trees, trade-offs, edge
cases, anti-patterns, and domain procedures that take real experience to
accumulate. Everything the model already holds (basic concepts, standard library
use, generic best practice, "write clean code") is a **no-op** that wastes shared
context. Classify every section as one of four knowledge types:

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | The model genuinely doesn't know this | Keep — this is the value |
| **Activation** | Known, but the model may not think of it unprompted | Keep only if brief |
| **Recoverable** | The model lacks it, but a live authoritative source answers it better | Replace with a pointer |
| **Redundant** | The model definitely knows this | Delete |

Maximize Expert, use Activation sparingly, cut Redundant without mercy.

**Recoverable is the type reviewers miss**, because it passes the knowledge-delta
test: the model really does not know that flag, parameter name, or count. Ask the
second question — can the agent obtain this at run time from `--help`,
`--version`, a tool schema, `doctor`/`status`, a registry listing, or the file
itself? If yes, the skill's copy is not merely wasteful, it **drifts**: wrong from
the next upstream release onward while still reading as authoritative. One graded
appendix gave its tool count as 81 in the title, 76 in two notes, and 63 by its
own arithmetic, against 80 actual rows — four answers to a question the running
tool answers once, correctly.

Two exceptions, and they decide real cases. Content is NOT recoverable when the
live source is unreachable in the situations the skill fires in — a
troubleshooting skill cannot route you to the `--help` of the tool that is
broken — or when the live source is **wrong**: a published schema stripped of its
own combinators, a documented warning that never fires. Content recording where
the authoritative source lies is among the most valuable a skill can carry, and
it looks exactly like the content this type tells you to cut. Check correctness
before cutting.

## Evaluation dimensions (120 points)

### D1 — Knowledge delta (20) — the core dimension

Does the skill add genuine expert knowledge?

| Score | Criteria |
|-------|----------|
| 0–5 | Explains basics ("what is X", how to write code, standard-library tutorials) |
| 6–10 | Mixed: some expert content diluted by obvious material |
| 11–15 | Mostly expert knowledge, minimal redundancy |
| 16–20 | Pure delta — every paragraph earns its tokens |

Red flags (cap at ≤5): "what is [basic concept]" sections, step-by-step tutorials
for standard operations, common-library usage, generic best practice, definitions
of industry-standard terms, and transcribed CLI surfaces, parameter schemas,
config-key lists, or inventory counts that the tool reports about itself.

Green flags: decision trees for non-obvious choices, trade-offs only an expert
knows, real-world edge cases, "NEVER do X because [non-obvious reason]",
domain-specific thinking frameworks, and content that records where an
authoritative source is wrong.

### D2 — Mindset + domain procedures (15)

Does it transfer expert *thinking patterns* and *procedures the model wouldn't
know*? Thinking patterns ("before designing, ask: what makes this memorable?")
shape decisions; domain procedures ("unpack → edit XML → validate → pack") supply
non-obvious sequences. Generic procedures (open, edit, save) score low.

| Score | Criteria |
|-------|----------|
| 0–3 | Only generic procedures the model already knows |
| 4–7 | Domain procedures present but no thinking framework |
| 8–11 | Balanced: thinking patterns + domain-specific workflows |
| 12–15 | Shapes thinking AND supplies procedures the model wouldn't know |

### D3 — Anti-pattern quality (15)

Half of expertise is knowing what NOT to do. The model hasn't stepped on the
landmines, so good skills name the "absolute don'ts" with reasons.

| Score | Criteria |
|-------|----------|
| 0–3 | No anti-patterns |
| 4–7 | Vague warnings ("avoid errors", "be careful") |
| 8–11 | Specific NEVER list with some reasoning |
| 12–15 | Expert-grade: specific + the non-obvious WHY experience teaches |

Test: would an expert say "yes, I learned that the hard way", or "that's obvious"?

### D4 — Specification compliance, especially the description (15)

The description is the only text the agent sees before loading — a great body
behind a vague description is a skill that never fires.

| Score | Criteria |
|-------|----------|
| 0–5 | Missing or invalid frontmatter |
| 6–10 | Has frontmatter but the description is vague |
| 11–13 | Valid; description states WHAT but is weak on WHEN |
| 14–15 | Description answers WHAT, WHEN, and carries trigger KEYWORDS |

`name`: lowercase, alphanumeric + hyphens, ≤64 chars. Description must answer
WHAT it does, WHEN to use it (explicit trigger scenarios), and which KEYWORDS
should surface it. (See `writing-great-skills` on writing the description.)

### D5 — Progressive disclosure (15)

Metadata (name + description) is always in memory; the body loads on trigger;
`references/`, `scripts/`, `assets/` load on demand.

| Score | Criteria |
|-------|----------|
| 0–5 | Everything dumped in SKILL.md (>500 lines, no layering) |
| 6–10 | References exist but no guidance on when to load them |
| 11–13 | Good layering with explicit load triggers |
| 14–15 | Load triggers embedded in workflow + "do NOT load" guidance |

**A skill with no references is not thereby capped.** Ask first whether any
content in the body is specialist lookup material — needed for some reviews and
dead weight in others. If none is, the correct package HAS no references, and it
scores on conciseness and self-containment against the bands above: a
self-contained skill carrying nothing it does not always need earns the top band
with zero reference files. Size does not decide this; content does. Cap only
where material that clearly belongs behind a trigger is loaded on every run.

### D6 — Freedom calibration (15)

Match specificity to fragility: creative tasks want high freedom (principles, not
steps); fragile operations want low freedom (exact scripts). Test: "if the agent
makes a mistake here, what's the consequence?" High consequence → low freedom.

| Score | Criteria |
|-------|----------|
| 0–5 | Severely mismatched (rigid scripts for creative work, or vague for fragile ops) |
| 6–10 | Partially appropriate |
| 11–13 | Well calibrated for most scenarios |
| 14–15 | Calibrated throughout |

### D7 — Evaluation evidence (10)

Was the skill built against evidence, or written and then admired? A skill is an
addition to a model, so its value is an empirical claim — and the only way to
know it helps is to have measured a task it was supposed to help with.

**Score only what the package can show.** Four things are inspectable; award them
independently rather than picking a band by feel:

| Present in the package | Points |
|---|---|
| ≥3 evaluations, each naming a realistic request and what counts as success | 4 |
| A recorded no-skill baseline — what the agent did unaided | 3 |
| The models the runs were made on, named | 2 |
| Enough retained detail that a regression re-runs without reconstruction | 1 |

**Do NOT score authoring order.** Whether evaluations were written before or
after the body is what makes them worth having, and it is **not establishable
from a finished package** — only version history shows it. If the repository
proves the order, say so as a finding; NEVER infer it, and NEVER deduct for an
order you cannot see. `skill-forge` owns teaching the order; this dimension owns
whether the evidence exists.

**A no-skill baseline is what makes a number mean anything.** "The skill works"
is not a result. "Without it the agent missed the auth step in 3 of 5 runs; with
it, 0 of 5" is.

**Weakest-model coverage is where this silently fails.** A skill tuned on a
frontier model routinely underspecifies for a small one, and a skill deployed to
several agents or read inside delegated contexts is being run by models nobody
tested. Award the model point only where the tested set covers the deployed set,
and name the untested classes in the report.

NEVER accept "it obviously helps" in place of a measurement, and NEVER treat the
absence of evaluations as a documentation gap — it is missing evidence for the
skill's central claim.

### D8 — Practical usability (15)

Can an agent act on it immediately?

| Score | Criteria |
|-------|----------|
| 0–5 | Confusing, incomplete, or self-contradictory |
| 6–10 | Usable with noticeable gaps |
| 11–13 | Clear for common cases |
| 14–15 | Covers edge cases, fallbacks, and error handling |

Check for decision trees on multi-path scenarios, working (not pseudo) examples,
stated fallbacks when the primary path fails, and realistic edge cases.

**Portability is scored here, and it is a hard cap rather than a deduction.** Cap
D8 at **10** when the skill depends on an environmental fact it never verifies,
and at **5** when that dependency is silent — no probe, no fallback, no message.
Provenance on empirical claims is scored here too: a version and a date, or the
claim is unverifiable rather than usable.

⛔ Load `references/portability-scoring.md` when the target names any tool, path,
runner or repository binding, or asserts how something behaves. It carries the
`metadata.scope` rule that decides whether the cap applies at all, the two
exemptions and the trap inside each, and the full checklist.

## Evaluation protocol

1. **Read the whole package, not just SKILL.md.** Reference files are where
   contradictions hide, and a grade that skipped them is a guess wearing a score.
   Record which files you read and which you did not.
2. **Knowledge-delta scan.** Tag each section `[E]`/`[A]`/`[Rec]`/`[R]` and give
   the ratio TWICE — once for SKILL.md, once for the whole package. They diverge
   sharply when the weight sits in `references/`, and one number reported without
   its scope is two different claims about the same skill. Good skill: >70% E,
   <10% R, and nothing left `[Rec]` that a pointer could replace.
3. **Cross-file consistency pass**, in two directions.

   **Assertion vs assertion** — where two files state the same fact, check they
   agree. A reference contradicting the body is worse than either being absent:
   the agent reads one, acts on it, and never sees the other. Field names, op
   semantics, counts, and defaults are where this bites.

   **Assertion vs the artifact it governs** — the direction that catches more,
   and the one a careful reader skips, because both halves read as correct in
   isolation and neither looks like a defect on its own. Three classes:
   - **Rule vs its own examples.** Does every worked example, template, and
     command obey the rule the package states elsewhere? A package that
     penalizes a pattern in its rubric and demonstrates it in its templates has
     shipped the defect twice and taught it once.
   - **Meta-claim vs package.** Countable claims about the package itself —
     "each section carries a warning", "all four templates", "the only
     mechanism that…" — are cheap to verify and routinely false after an edit
     that added a fifth thing.
   - **Rule vs the skill's own conduct.** Does the skill obey what it demands?
     A portability rule broken by the command printed beneath it, or a MUST the
     skill itself does not satisfy, is a rule the reader learns to discount —
     and it discredits the neighbouring rules that were fine.

   Report each against whichever dimension the broken instance sits in — D1 for
   a wrong example, D8 for a wrong command. Do NOT add a dimension; the
   120-point scale is fixed.
4. **Structure pass.** Validate frontmatter, and read `metadata.scope` FIRST —
   it decides how D8 is scored, and reading it after forming an impression of
   the skill is how an undeclared local skill talks its way into an exemption.
   Absent means `portable`. Count SKILL.md lines; list
   reference files and sizes; note which workflow mechanisms the procedure uses,
   as description rather than classification; check load triggers; flag
   any single reference larger than the rest of the package combined.
5. **Score each dimension.** Cite specific lines as evidence; give a one-line
   justification per score; note the fix when below max.
6. **Total and grade.** Sum D1–D8 (max 120). A ≥90% (108+), B 80–89% (96–107),
   C 70–79% (84–95), D 60–69% (72–83), F <60% (<72). A grade over a partially
   read package MUST say so, and its D1, D5 and D8 scores are provisional.
7. **Report** using the template below.

## Report template

```markdown
# Skill Evaluation: [name]

- **Score**: X/120 (X%) — Grade [A–F]
- **Workflow mechanisms**: [ordering/routing/delegation/refinement/detection/scoring/templating/degradation, or none] — descriptive, not scored
- **Knowledge ratio** SKILL.md E:A:Rec:R = W:X:Y:Z | package E:A:Rec:R = W:X:Y:Z
- **Coverage**: read [files]; not read [files] — scores provisional if any
- **Verdict**: [one sentence]

| Dimension | Score | Max | Note |
|-----------|-------|-----|------|
| D1 Knowledge delta | X | 20 | |
| D2 Mindset + procedures | X | 15 | |
| D3 Anti-patterns | X | 15 | |
| D4 Spec / description | X | 15 | |
| D5 Progressive disclosure | X | 15 | |
| D6 Freedom calibration | X | 15 | |
| D7 Evaluation evidence | X | 10 | |
| D8 Usability | X | 15 | |

## Critical issues
[must-fix problems]

## Top 3 improvements
1. …
2. …
3. …
```

## References

Two files. Both are lookup material for part of a review, never preparation for one.

| Load when | File |
|---|---|
| Scoring D8 on a skill that names any tool, path, runner or repository binding, or that asserts how something behaves | `references/portability-scoring.md` |
| A dimension has already scored low and the finding needs a named diagnosis and a stated repair | `references/failure-patterns.md` |

**Do NOT load:**

- `portability-scoring.md` for a skill with no tool, path or runner dependency at all — its
  caps cannot apply, and reading it invites hunting for a defect the package cannot have.
- `failure-patterns.md` BEFORE scoring. It is a catalogue of named defects, and a reviewer
  holding it scores toward the patterns it lists rather than the package in front of them.
  Score first from the dimensions, then name what you found.

## NEVER when evaluating

- NEVER reward professional formatting or length on their own.
- NEVER forgive explaining basics with "but it adds helpful context".
- NEVER skip mentally running the decision trees — do they reach correct choices?
- NEVER overlook a missing description or a missing NEVER list — both are major gaps.
- NEVER treat all procedures as valuable — separate domain-specific from generic.
- NEVER excuse an environmental dependency because the tool happens to be
  installed here. The question is whether the skill still works on a machine
  that never heard of it — unless the tool IS the skill's subject, in which case
  the question is whether it says what to do when the tool is absent.
- NEVER score a package you have only partly read without saying which files you
  skipped. A grade resting on half a package reads exactly as confident as one
  resting on all of it.
- NEVER cut content just because a live source also carries it. Check first that
  the source is correct and reachable when the skill fires; documenting where an
  authoritative source lies is high-value content that looks like duplication.

## The meta-question

> "Would an expert in this domain say: 'yes, this captures knowledge that took me
> years to learn'?"

Yes → the skill has genuine value. No → it compresses what the model already
knows, which is worthless compression.
