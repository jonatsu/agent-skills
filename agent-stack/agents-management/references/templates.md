# Instruction File Shapes

Use these shapes only during initialization or a structural rewrite. Include a section only when verified
repository knowledge earns the recurring context cost.

## Root File

```markdown
# <Project Name>

<One sentence that distinguishes this repository for an agent.>

## Commands

- `<command>`: `<constraint or reason the runner does not state>`

## Architecture

- `<path>` owns `<responsibility>`; `<similar path>` has `<different status>`.

## Conventions

- `<concrete, repository-evidenced convention>`

## Gotchas

- `<what to do, or never do>`: `<failure symptom or consequence>`

## Documentation

Route to the hub; do not inline what belongs in a genre beneath it.

| File | What it holds | Read when |
|---|---|---|
| `docs/README.md` | the documentation hub: one row per genre | `<the genres a reader here needs>` |

## Findings

Open the matching file when the symptom appears.

| Symptom | Read |
|---|---|
| `<what the agent observes going wrong>` | `<findings file>` |

## Pointers

Open the matching file before working in its area.

| Read before you touch | File | Holds |
|---|---|---|
| `<path or glob>` | `<instruction file>` | `<scope>` |

## Update triggers

When the left changes, update the right in the same change.

| When this changes | Update |
|---|---|
| `<source of truth>` | `<doc or file that must resync>` |
```

The floor routes to `docs/README.md` and to the findings and scoped-instruction files above; it does not
enumerate the genres beneath the hub. Which documents exist and how they are organized is owned by
`context-architecture`'s [named default layout](../../context-architecture/references/default-layout.md); the
default findings tier is `docs/findings/`, and an existing repository convention wins over both.

Delete sections that would contain a runner transcription, directory listing, generic advice, or README
summary. The fillable version is `../assets/AGENTS.template.md`.

`Gotchas` holds one imperative line per entry. Its supporting evidence, meaning dates, commit identifiers,
tool-version measurements, and superseded arrangements, goes to a findings file instead, indexed by symptom.
`Findings` and `Pointers` route differently and both can apply: `Pointers` sends an agent to a scope before it
starts work, while `Findings` sends it to evidence after something has already gone wrong.

## Package File

Use a package file when its instructions differ materially from the root. Add the verified filename adapter
beside it and an imperative pointer in the root file.

```markdown
# <Package Name>

<What differs from the repository root.>

## Usage

- `<non-obvious usage constraint>`

## Dependencies

- `<ordering or initialization dependency the manifest does not show>`

## Gotchas

- `<package-specific failure mode>`
```

The same split applies here. A package file inherits the root file's findings directory rather than starting
its own.

## llms.txt

Use `../assets/llms.template.txt` only when the user requests a documentation index. Keep an H1, an optional
summary blockquote, H2 groups of resolving links, and an `Optional` group last. Do not place agent
instructions in it.
