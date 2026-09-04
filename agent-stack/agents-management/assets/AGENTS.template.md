# AGENTS.md: <project>

\<One or two lines: what this repo is, from an agent's perspective. Not a README rehash.>

<!--
  Keep CLAUDE.md as a symlink to this file:  ln -s AGENTS.md CLAUDE.md
  Never use `ln -sf`. If CLAUDE.md already exists as a real file, reconcile the two
  by hand instead. Delete this comment once the symlink is in place.

  Every line below should provide something the agent cannot get by reading the repo.
  Delete any section the repository does not justify; an empty section costs the
  same as a full one.

  Fill these from the ecosystem the repo actually has: its manifest, its
  runner, its conventions. If the repo has no ecosystem yet, delete the
  Commands and Environment sections rather than guessing one: a greenfield repo
  should not be committed to a package manager or test runner by its
  instruction file.
-->

## Commands

\<Only invocations carrying something the runner does not state. The agent can read the runner's own recipe
list, so do not transcribe it here. Delete this section entirely if the repo has no runner yet.>

- `<command>`: `<the constraint or reason that is not in the runner>`

## Architecture

<What the directory tree does not reveal. Delete this section rather than
pasting a tree the agent can produce with one listing command.>

- `<dir>` owns `<responsibility>`; `<other dir>` looks similar but is `<status>`
- `<boundary>` exists because `<reason>`

## Conventions

\<Only what is evidenced in the repo: commit history, a contributing guide, an editorconfig. Concrete enough
that a diff shows whether it was followed.>

- `<convention>`, never `<the alternative it replaces>`

## Environment

- `<VAR_NAME>`: `<purpose, and when it must be set>`

## Gotchas

\<One imperative line per gotcha: what to do, and the symptom that reveals it. Generated files, ordering
dependencies, silent failures, restart requirements.

Keep the evidence out of this file. No dates, commit identifiers, tool-version measurements, or accounts of
arrangements that have since been replaced. That material is read once a symptom appears, so it belongs in a
findings file below rather than in every session's context. Relocate it; never delete it to save room.>

- `<what to do, or never do>`: `<what it looks like when it bites>`

## Findings

\<Delete unless a gotcha above has evidence worth keeping. Otherwise put one file per subject under a
directory this repository chooses, each holding the measurements, superseded arrangements, and reasoning
behind the rules above.

Index them by symptom rather than by subject. An agent that recognizes what it is looking at will open the
file; an agent reading a list of topics has no reason to.>

Open the matching file when the symptom appears. Every rule above stands without it; these hold the evidence.

| Symptom                                 | Read                          |
| --------------------------------------- | ----------------------------- |
| `<what the agent observes going wrong>` | `<path to the findings file>` |

## Pointers

\<Delete if the repo has no auxiliary instruction files. Otherwise: use this table to guide agents that do
not parse includes or discover nested files. Verify the pointer behavior for each target agent.>

Open the matching file yourself before working in its area. Treat this table as the instruction rather than a
description of automatic loading.

| Read before you touch | File     | Holds             |
| --------------------- | -------- | ----------------- |
| `<path or glob>`      | `<file>` | `<what is in it>` |
