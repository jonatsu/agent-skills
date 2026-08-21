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

A `--quick` flag that skips confirmation gates is a common pattern:

```markdown
## Step 2: Confirm Options ⚠️ REQUIRED

Unless `--quick` was passed:
- Present options to user
- Wait for confirmation

If `--quick`: use auto-selected defaults and proceed.
```

### Default Values

MUST define sensible defaults for every parameter so `/my-skill content.md` with zero flags still produces good output.
