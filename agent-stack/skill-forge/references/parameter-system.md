# Parameter System

## The $ARGUMENTS Variable

Skills receive user input through the `$ARGUMENTS` variable. This includes everything the user types after the skill invocation.

Example: `/my-skill article.md --style dark --quick`
-> `$ARGUMENTS` = `article.md --style dark --quick`

## Designing Parameters

### Basic Structure

MUST document parameters as a table in SKILL.md:

```markdown
## Options

| Option | Description | Default |
|--------|-------------|---------|
| `<content>` | Input file or text | Required |
| `--style <name>` | Visual style | auto |
| `--quick` | Skip confirmation gates | false |
| `--lang <code>` | Output language | en |
```

### Parameter Types

1. **Positional**: `<content>`
2. **Named flags**: `--style dark`
3. **Boolean flags**: `--quick`
4. **Partial execution**: `--outline-only`, `--images-only`
5. **Selective redo**: `--regenerate 3`

### Argument Hint

SHOULD add `argument-hint` to frontmatter:

```yaml
argument-hint: [content] [--style name] [--quick] [--lang code]
```

### Quick Mode

A `--quick` flag MAY skip gates that only collect **preferences** — which style, which
language, which of several equally valid outputs.

`--quick` MUST NEVER skip a gate guarding a destructive operation: delete, overwrite,
force-push, send, deploy. One flag typed up front cannot authorize an action the user had no
way to foresee when they typed it, and a gate that a flag can switch off is not a gate.

```markdown
## Step 2: Confirm Options (skipped by `--quick`)

Unless `--quick` was passed:
- Present the style and language options
- Wait for the user's selection

If `--quick`: use the documented defaults and proceed.

## Step 5: Confirm Overwrite ⚠️ REQUIRED

Ask before replacing the existing file. `--quick` does NOT skip this gate.
```

If every gate a skill has is destructive, that skill has no `--quick` mode. Say so, rather
than adding a flag that skips nothing.

### Default Values

MUST define sensible defaults for every parameter so `/my-skill content.md` with zero flags still produces good output.
