# AGENTS.md — <project>

<One or two lines: what this repo is, from an agent's perspective. Not a README rehash.>

<!--
  Keep CLAUDE.md as a symlink to this file:  ln -s AGENTS.md CLAUDE.md
  Never `ln -sf` — if CLAUDE.md already exists as a real file, reconcile the two
  by hand instead. Delete this comment once the symlink is in place.

  Every line below must be something the agent cannot get by reading the repo.
  Delete any section the repository does not justify; an empty section costs the
  same as a full one.

  Fill these from the ecosystem the repo ACTUALLY has — its manifest, its
  runner, its conventions. If the repo has no ecosystem yet, delete the
  Commands and Environment sections rather than guessing one: a greenfield repo
  should not be committed to a package manager or test runner by its
  instruction file.
-->

## Commands

<Only invocations carrying something the runner does not state. A transcription
of the runner's own recipe list is worse than nothing — the agent can read it.
Delete this section entirely if the repo has no runner yet.>

- `<command>` — `<the constraint or reason that is not in the runner>`

## Architecture

<What the directory tree does NOT reveal. Delete this section rather than
pasting a tree the agent can produce with one listing command.>

- `<dir>` owns `<responsibility>`; `<other dir>` looks similar but is `<status>`
- `<boundary>` exists because `<reason>`

## Conventions

<Only what is evidenced in the repo — commit history, a contributing guide, an
editorconfig. Concrete enough that a diff shows whether it was followed.>

- `<convention>`, never `<the alternative it replaces>`

## Environment

- `<VAR_NAME>` — `<purpose, and when it must be set>`

## Gotchas

<The highest-value section. Each line should be something that cost someone a
debugging session: generated files, ordering dependencies, things that fail
silently, restart requirements.>

- `<non-obvious behavior>` — `<what it looks like when it bites>`

## Pointers

<Delete if the repo has no auxiliary instruction files. Otherwise: this table is
the only mechanism that works on every agent, including those that do not parse
includes and those that do not discover nested files.>

Open the matching file yourself before working in its area — treat this table as
the instruction, not as a description of something that happens automatically.

| Read before you touch | File | Holds |
|---|---|---|
| `<path or glob>` | `<file>` | `<what is in it>` |
