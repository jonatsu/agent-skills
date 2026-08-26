# What Earns a Place in an Instruction File

## Core principle: a document that restates the environment is a cache

The repository is a source of truth in its own right. The task runner, the
manifest, the config files, the directory layout, a tool's own help output —
an agent can read all of them. A line that repeats one of these is a copy of a
lookup, and it earns its load only when the lookup is expensive or the answer
is wrong.

Cache what the agent cannot find by looking: the unwritten convention, the
reason behind a choice, the gotcha no config confesses.

Every line is paid for in every session, forever. Removal is usually worth more
than addition.

## The two tests

Apply both to every candidate line, before proposing it.

**The cache test** — could the agent get this by reading a file or running a
help command? If yes, cut it, unless the line adds the part the lookup does not
carry: a reason, an ordering, a constraint.

**The no-op test** — does this change behavior versus what the agent would do
anyway? An instruction the model already obeys by default pays load to say
nothing. The test is model-relative, not reader-relative: a line can read as
sound advice and still be a no-op. When a sentence fails, **delete the whole
sentence** rather than trimming words from it.

## What TO add

### Commands, with the part the runner does not state

The runner already lists its own recipes. What it cannot tell the agent is why
one of them is invoked oddly.

```markdown
## Commands

- Run the suite through the project's environment manager, not the ambient
  interpreter — the two resolve different versions and the type checker
  disagrees with the linter otherwise.
- The integration target must run sequentially; the fixtures share one database.
```

Why: the invocation is discoverable, the constraint is not.

### Gotchas and non-obvious patterns

```markdown
## Gotchas

- The lockfile is authoritative; delete the dependency directory if resolution
  disagrees with it.
- Generated output is committed. Regenerate rather than hand-editing, or the
  drift gate fails on the next commit.
```

Why: prevents repeating a debugging session.

### Ordering and initialization dependencies

```markdown
## Dependencies

The auth module requires the crypto layer initialized first. Import order in
the bootstrap entry point is load-bearing, not stylistic.
```

Why: architecture knowledge that reading any single file does not reveal.

### Conventions that a diff can be checked against

```markdown
## Conventions

- Value types use the project's attrs-style decorator, never plain classes.
- Locate bundled data by package identity, never by walking up from a file path.
```

Why: concrete enough that a reviewer can tell from the diff whether it was
followed.

### Environment quirks

```markdown
## Environment

- Build-time variables must be set before the build, not at runtime.
- The cache directory must sit on the same filesystem as the checkout; a
  cross-device link fails silently and the build falls back to a slow path.
```

Why: environment-specific knowledge no config file states.

## What NOT to add

### 1. Obvious code info

Bad:
```markdown
The UserService class handles user operations.
```

The class name already says this. Fails the cache test.

### 2. Generic best practices

Bad:
```markdown
Always write tests for new features.
Use meaningful variable names.
```

Universal advice, not project-specific. Fails the no-op test — the agent does
this anyway.

### 3. One-off fixes

Bad:
```markdown
We fixed a bug in commit abc123 where the login button did not work.
```

Will not recur; clutters the file.

### 4. Verbose explanations

Bad:
```markdown
The authentication system uses JWT tokens. JWT (JSON Web Tokens) are
an open standard (RFC 7519) that defines a compact and self-contained
way for securely transmitting information between parties as a JSON
object. In our implementation, we use the HS256 algorithm which...
```

Good:
```markdown
Auth: JWT with HS256, tokens in the Authorization Bearer header.
```

The explanation of a well-known technology is a no-op. The project's choice
within it is not.

### 5. A transcription of the runner

Bad:
```markdown
| Command | Purpose |
|---------|---------|
| dev     | Start the dev server |
| build   | Production build |
| test    | Run the test suite |
```

Three rows, three lookups the agent can perform in one command, no reason
attached to any of them. This is the most common failure and the easiest to
mistake for thoroughness.

## Separating generated content from hand-written knowledge

Where any part of the file is produced by a tool, fence it with markers and
keep hand-appended knowledge outside them. A regeneration that swallows a
hard-won convention is indistinguishable from a successful update, and the
score goes *up* afterwards.

```markdown
<!-- GENERATED:START - do not edit inside this block -->
...tool output...
<!-- GENERATED:END -->

## Conventions
...hand-written, survives regeneration...
```

## Diff format for updates

For each proposed change, give three things.

**1. The file and location**

```text
File: ./AGENTS.md
Section: Conventions (new section, after Architecture)
```

**2. The change**

```diff
 ## Architecture
 ...

+## Conventions
+
+- The integration suite must run sequentially; the fixtures share one database.
```

**3. Why it helps a future session**

> **Why this helps:** the constraint is not stated anywhere in the runner or the
> test config, and the failure it prevents — intermittent cross-test pollution —
> reads as flakiness rather than as a missing flag.

A "why" that amounts to "saves the agent from looking it up" is the cache test
failing. Rewrite the line or drop it.

## Validation checklist

Before finalizing an update:

- [ ] Each addition passes the cache test — not derivable from a file or a help command
- [ ] Each addition passes the no-op test — changes behavior versus the default
- [ ] Every command named exists in this repo's runner (checked, not assumed)
- [ ] Every path referenced exists (checked, not assumed)
- [ ] No ecosystem assumed that the repository has not evidenced
- [ ] Nothing duplicated from the README or from another instruction file
- [ ] Hand-written knowledge sits outside any generated block
- [ ] Removals reviewed: no convention, gotcha, or reason silently dropped
