---
name: flake-manifest-sync
description: 'Safely edit flake inputs or dependencies where the top-level flake.nix, or an equivalent manifest, is auto-generated from a hand-maintained source module rather than being the source of truth itself. Use when asked to add, update, remove, pin, or bump a flake input, or when flake.nix carries a generated/do-not-hand-edit header comment. Triggers on: flake input, bump dependency, generated flake.nix, write-flake, source-of-truth module, flake-file.nix.'
license: MIT
metadata:
  author: Joonas Onatsu
---

IRON LAW: NEVER hand-edit a generated manifest past its "do not edit" header. Edit the
source-of-truth module the manifest is generated from, then regenerate.

# Flake Manifest Sync

Generic workflow for repos where a generated dependency manifest (most commonly `flake.nix` itself, e.g. via
`github:vic/flake-file`) is produced from a separate source module by a regeneration command. Editing the generated file
directly works right up until the next regeneration silently reverts it — the failure is delayed, not immediate, which
is what makes it dangerous.

This is a tooling choice individual repos make (e.g. by adopting `github:vic/flake-file`), not a property of any
framework or flake style — most repos hand-maintain `flake.nix` with no generation step. Confirm the specific repo
actually has a generated manifest (check for a "do not hand-edit" header) before assuming one exists.

## Workflow

```text
Manifest Sync Progress:
- [ ] Step 1: Confirm the generated-manifest pattern applies
- [ ] Step 2: Edit the source module only ⛔ BLOCKING
- [ ] Step 3: Regenerate
- [ ] Step 4: Diff the full result ⚠️ REQUIRED
- [ ] Step 5: Sanity-build the affected target
```

### Step 1: Confirm the pattern applies

Check the generated file's header for language like "auto-generated, do not hand-edit past this point." Identify the
actual source-of-truth module (commonly named something like `flake-file.nix`) and the current regeneration command —
check the repo's devshell/README for the exact current name, since these get renamed.

### Step 2: Edit the source module only ⛔ BLOCKING

Make the actual change — add/remove/pin an input, change a `follows` relationship — in the source-of-truth module. NEVER
edit past the generated file's header comment, even for a "just this once" fix.

### Step 3: Regenerate

Run the documented regeneration command.

### Step 4: Diff the full result ⚠️ REQUIRED

`git diff` the generated file after regeneration and read every hunk, not just the region expected to change. Ask: does
any part of this diff look like it's _reverting_ something, rather than applying the intended change?

If yes — STOP. This is the signature of an earlier hand-patch that bypassed the source-of-truth module and was never
folded back into it; regenerating is about to silently discard that fix. Recover the original intended change, fold it
into the source module properly, and only then re-run regeneration — or flag it to the user if the original intent isn't
recoverable.

### Step 5: Sanity-build

Evaluate/build at least one target that depends on the changed input to confirm the flake still resolves cleanly.

## Why This Matters

A generated manifest drifts from its source silently and with a significant delay: someone hand-patches the generated
file directly, it works, nobody updates the source module, and the divergence sits invisible until the _next_
regeneration wipes it out with no error — often long after the context explaining the original patch is gone. Treat any
commit that touches only the generated file (not its paired source module) as a signal to check for this kind of drift
before the next regeneration.

## Anti-Patterns to Avoid

- Hand-editing the generated file past its header for a "quick fix" without also updating the source module in the same
  change.
- Running the regeneration command and eyeballing only the diff region that was expected to change, instead of reading
  the full diff.
- Treating a clean exit code from the regeneration command as proof nothing was lost — the diff step is what actually
  verifies this, not the exit code.

## Pre-Delivery Checklist

- [ ] All input/dependency changes were made in the source module, never past the generated file's header
- [ ] The full post-regeneration diff was read, not just the expected hunk
- [ ] No unintended reversion of prior content was found in the diff (or, if found, was recovered and folded into the
  source module)
- [ ] At least one dependent target builds/evals successfully afterward
