# Instruction File Shapes

Use these shapes only during initialization or a structural rewrite. Include a section only when verified repository
knowledge earns the recurring context cost.

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

- `<non-obvious behavior>`: `<failure symptom or consequence>`

## Pointers

Open the matching file before working in its area.

| Read before you touch | File | Holds |
|---|---|---|
| `<path or glob>` | `<instruction file>` | `<scope>` |
```

Delete sections that would contain a runner transcription, directory listing, generic advice, or README summary. The
fillable version is `../assets/AGENTS.template.md`.

## Package File

Use a package file when its instructions differ materially from the root. Add the verified filename adapter beside it and
an imperative pointer in the root file.

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

## llms.txt

Use `../assets/llms.template.txt` only when the user requests a documentation index. Keep an H1, an optional summary
blockquote, H2 groups of resolving links, and an `Optional` group last. Do not place agent instructions in it.
