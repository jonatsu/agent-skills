# Instruction File Section Shapes

Shapes only. Whether a section earns its place is decided by
`update-guidelines.md`, and several shapes below fail that test if filled in
naively — each carries the warning inline.

**Contents**
- [Key principles](#key-principles)
- [Sections](#sections)
- [Template: root, minimal](#template-root-minimal)
- [Template: root, fuller](#template-root-fuller)
- [Template: package or module](#template-package-or-module)
- [Template: monorepo root](#template-monorepo-root)

---

## Key principles

- **Concise**: one line per concept where possible.
- **Actionable**: a reviewer can tell from a diff whether it was followed.
- **Project-specific**: what is true here, not what is true everywhere.
- **Non-derivable**: if a listing command or a manifest answers it, cut it.
- **Current**: reflects the repository as it is, checked rather than assumed.

Use only the sections the repository justifies. An empty or generic section
costs the same as a full one.

## Sections

### Commands

⚠️ A transcription of the runner's recipe list scores 5 and should be cut. Give
the invocations that carry something the runner does not state.

```markdown
## Commands

- `<command>` — `<the constraint or reason that is not in the runner>`
- `<command>` — `<why this form rather than the obvious one>`
```

### Architecture

⚠️ A directory tree the agent can produce with one listing command is not worth
context. Write what the tree does not show.

```markdown
## Architecture

- `<dir>` owns `<responsibility>`; `<other dir>` looks similar but is `<status>`
- Entry point is `<path>`, not the obvious `<other path>`
- `<boundary>` exists because `<reason>`
```

### Conventions

```markdown
## Conventions

- `<convention>`, never `<the alternative it replaces>`
- `<preference>` because `<reason>`
```

### Environment

```markdown
## Environment

- `<VAR_NAME>` — `<purpose, and when it must be set>`
- `<setup step that is not in the manifest>`
```

### Gotchas

The highest-value section. Each line should be something that cost someone a
debugging session.

```markdown
## Gotchas

- `<non-obvious behavior>` — `<what it looks like when it bites>`
- `<ordering dependency or prerequisite>`
- `<thing that fails silently>`
```

### Pointers to other files

The portable mechanism for anything not in the main file: guidance scoped to a
subtree, per-package files, long reference material. Works whether or not the
agent parses includes.

⚠️ Phrase each row as an imperative naming its trigger. A row that describes
what the harness supposedly does is not an instruction.

```markdown
## Pointers

Open the matching file yourself before working in its area — treat this table as
the instruction, not as a description of something that happens automatically.

| Read before you touch | File | Holds |
|---|---|---|
| `<path or glob>` | `<file>` | `<what is in it>` |
```

### Workflow

```markdown
## Workflow

- `<when to do X>`
- `<preferred approach for Y, and what it replaces>`
```

## Template: root, minimal

````markdown
# <Project Name>

<One-line description>

## Commands

- `<command>` — `<the reason this form is needed>`

## Gotchas

- `<gotcha>`
````

## Template: root, fuller

````markdown
# <Project Name>

<One-line description>

## Commands

- `<command>` — `<constraint the runner does not state>`

## Architecture

- `<what the directory tree does not reveal>`

## Conventions

- `<convention>`, never `<alternative>`

## Environment

- `<VAR>` — `<purpose and timing>`

## Gotchas

- `<gotcha>`

## Pointers

| Read before you touch | File | Holds |
|---|---|---|
| `<path or glob>` | `<file>` | `<what is in it>` |
````

## Template: package or module

For a package inside a monorepo, or a distinct module with its own rules.

Pair this with a symlink beside it, so agents that discover nested files by
their own filename find it, and with a pointer row in the root file, so agents
that do not discover nested files are told to open it.

````markdown
# <Package Name>

<What this package is for>

## Usage

- `<the non-obvious part of consuming it>`

## Dependencies

- `<dependency>` — `<why it is needed, or what breaks without it>`

## Notes

- `<constraint that does not apply elsewhere in the repo>`
````

## Template: monorepo root

````markdown
# <Monorepo Name>

<Description>

## Packages

| Package | Path | What lives there |
|---------|------|------------------|
| `<name>` | `<path>` | `<purpose>` |

## Commands

- `<repo-wide command>` — `<reason>`

## Pointers

Open the package's own file before working in it.

| Read before you touch | File | Holds |
|---|---|---|
| `<package path>` | `<package file>` | `<what is in it>` |

## Cross-Package Patterns

- `<shared pattern>`
- `<generation or sync rule, and what breaks if it is skipped>`
````
