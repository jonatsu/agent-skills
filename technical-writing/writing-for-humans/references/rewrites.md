# Worked Rewrites

Use this reference when the target of an edit is clear but its size is not. Each pair shows how far to cut and
what the result should look like. The passages are technical prose, because that is this skill's scope; the
rules they demonstrate are the ones in `SKILL.md`.

Read the note under each pair. A rewrite is only correct because something specific survived it, and the note
names what.

Examples are fenced rather than quoted so that a formatter cannot reflow them and so that the marks under
discussion, headings and bold runs among them, stay visible as source.

## Not X But Y

Before:

```text
This is not just a caching layer, it is a correctness boundary. The point is
not that requests get faster, but that two readers never see different
versions of the same record.
```

After:

```text
The cache is a correctness boundary as well as a speed optimisation: two
readers never see different versions of the same record.
```

The negative halves named nothing anyone had claimed. Both surviving facts are in the rewrite, and the colon
states the relation the contrast left implicit.

### Split Across Sentences

Before:

```text
This does not mean the checkpoint is corrupt. It means the settings that
produced it no longer match the settings of this run.
```

After:

```text
The checkpoint is intact; the settings that produced it no longer match this
run's.
```

The two-sentence form is the same move at a larger scale. "Intact" had to be written explicitly: deleting the
first sentence alone would have dropped a claim.

## A Closer That Restates Its Paragraph

Before:

```text
atomic_write.py writes every artifact through a temporary file and a rename,
so a crash mid-write leaves the previous version in place rather than a
truncated one.

That is the whole point.
```

After:

```text
atomic_write.py writes every artifact through a temporary file and a rename,
so a crash mid-write leaves the previous version in place rather than a
truncated one.
```

Cut the closer entirely. A one-sentence paragraph earns its place by carrying a new fact, and this one asks
the reader to pause on a claim already made.

## An Aphorism Standing In For The Claim

Before:

```text
At its core, what really matters is observability. Logging is the language of
operational trust.
```

After:

```text
A failed run is only diagnosable if it recorded which stage failed and on
which input.
```

The aphorism named a topic. The rewrite names the property that makes the topic matter, which is what the
reader needed. Where the source supports no such specific claim, cut the sentence rather than inventing one.

## A Run-Up That Announces The Point

Before:

```text
Let's dive into how the resolver handles collisions. Here's what you need to
know: honestly, it's simpler than it looks.
```

After:

```text
The resolver appends a numeric suffix to the stem and retries, up to the
configured limit.
```

The staged candour goes with the run-up. "Honestly" inside an ordinary sentence is fine; the standalone opener
before a routine claim is the tell.

## An Objection Nobody Raised

Before:

```text
To be clear, this is not an argument against schema versioning. A tempting
approach would be to migrate old artifacts in place, but that would combine
pages recognised under different settings into one record. Don't get me
wrong, migration works elsewhere. The tool sets the old checkpoint aside
instead.
```

After:

```text
The tool sets an incompatible checkpoint aside rather than migrating it,
because migration would combine pages recognised under different settings
into one record.
```

Three defences of a position nobody attacked. The rejected alternative held the only real content, so it moved
into the reason clause. An alternative a reader would genuinely weigh stays; this one was answered in the same
breath it was raised.

## A Forced Triad

Before:

```text
The pipeline offers flexibility, reliability, and performance. Each stage
validates its input, records its decisions, and reports its confidence.
```

After:

```text
Each stage validates its input and records the decisions behind its output,
including a confidence score.
```

The first sentence had no content. The second was a genuine list, but "reports its confidence" is part of
recording decisions rather than a third thing, so the rewrite states two and subordinates the third. Keep
three items where the subject has three.

## Serves As, Stands As, Boasts

Before:

```text
ports.py serves as the seam between stages and represents the contract
adapters must satisfy. The module boasts five protocols.
```

After:

```text
ports.py is the seam between stages, and its five protocols are the contract
an adapter must satisfy.
```

Three long verbs became one `is` and one possessive. Nothing was lost, because none of them carried meaning
the plain verb does not.

## A Relation Left Vague

Before:

```text
The retry budget is related to the request timeout. The vision advisor is
associated with the scanned path.
```

After:

```text
The retry budget must be smaller than the request timeout, or the last retry
is cancelled mid-flight. The vision advisor runs only on the scanned path.
```

"Related to" and "associated with" hide whether a value bounds another, is derived from it, or merely sits
near it. Write the relation the source states. Where the source genuinely does not say, keep the vague wording
rather than inventing a specific one.

## A Gap Filled With A Guess

Before:

```text
The upstream project does not document the flag's default. It likely defaults
to false, following the convention used by the other boolean options.
```

After:

```text
The upstream project does not document the flag's default. Read it from
config.defaults before relying on it.
```

The hedge does not make the guess safe. Either state the gap and name the way to close it, or cut the
sentence. Never leave a plausible invention where a reader will take it as reported.

## Bold As Decoration

Before:

```text
- **Validation:** Configuration is validated at the process boundary.
- **Resolution:** Relative paths are resolved from the configuration file.
- **Collision:** Output collisions are detected before any write.
```

After:

```text
Configuration is validated at the process boundary, relative paths are
resolved from the configuration file rather than the working directory, and
output collisions are detected before any write.
```

Every label restated the opening of its own item, so the bold marked nothing. Prose carried it in one
sentence, and the rewrite then had room for the distinction the list omitted.

A labelled list survives where the labels differ in kind and a reader scans for them, as in a table of
statuses where `active`, `landed`, and `superseded` are the thing being looked up.

## A Heading Restated

Before:

```text
## Checkpoints

Checkpoints let a run resume.

A checkpoint is written after each logical page and removed once the artifact
lands.
```

After:

```text
## Checkpoints

A checkpoint is written after each logical page and removed once the artifact
lands, so an interrupted run resumes from the last completed page.
```

The restating line was deleted and its only fact, that checkpoints enable resumption, folded into the sentence
that carries the detail. Deleting it outright would have dropped the claim.

## Writing About The Previous Version

Before:

```text
This function replaces the old approach of scanning every entry, which was
O(n^2) on large documents.
```

After:

```text
Lookups go through the index, so cost is constant in the number of entries.
```

The comment described a change rather than the code. It dates itself at the next edit, and a later reader
cannot tell whether the comparison still holds. Change logs, release notes, migration guides, and decision
records are the exception, because change is their subject.

## Over-Correction

Every pair above cuts. These two go too far, and each result is as much an artifact as the marks the edit was
meant to remove.

Before:

```text
The probe degrades to an unknown status rather than failing the command that
reports it.
```

After, wrong:

```text
The probe just returns unknown. No drama.
```

Informality was fabricated, and "rather than failing the command that reports it" carried the actual
guarantee. The sentence already met every rule in `SKILL.md`, so the correct edit was none.

Before:

```text
Recognition may reduce the proofreading burden on clean scans.
```

After, wrong:

```text
Recognition reduces the proofreading burden.
```

Shortening removed a hedge the source supported and a scope condition, turning a qualified claim into a
general one. Protect the words carrying a limit, condition, exception, or qualification: a length target
reaches for those first.
