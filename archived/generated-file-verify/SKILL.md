---
name: generated-file-verify
description: 'Verify a build-tool-produced doc, config, or manifest before regenerating it, by determining whether its content is genuinely live-derived from current config or static hand-authored text routed through a generic writer. Use when asked to regenerate docs or refresh a generated manifest, diagram, or README, or when generated output looks stale or contradicts the checked-out tree. Triggers on: regenerate docs, stale docs, generated README, eval cache, writeText generator, files.file.'
license: MIT
metadata:
  author: Joonas Onatsu
---

IRON LAW: NEVER run a "regenerate X" command expecting it to fix content without first reading the
generator's source to confirm the content is actually live-derived from config, not hand-authored text.

# Generated File Verification

Two failure modes hide behind an identical call site ("run the regenerate command") in repos with Nix-produced (or
similarly build-tool-produced) docs, manifests, or config dumps. Telling them apart before acting saves wasted
regeneration cycles and prevents shipping stale content that _looks_ freshly regenerated.

## Workflow

```text
Generated-File Verify Progress:
- [ ] Step 1: Classify the generator ⚠️ REQUIRED
- [ ] Step 1b: Confirm exactly one generator owns the target file ⚠️ REQUIRED
- [ ] Step 2 (conditional): Fix hand-authored source text first
- [ ] Step 3: Verify in an isolated worktree, not the real tree
- [ ] Step 4 (conditional): Rule out a stale cache before chasing a content bug
- [ ] Step 5: Write back to the real tree only once verified
```

### Step 1: Classify the generator ⚠️ REQUIRED

Read the generator module's actual source, not just its output. Ask: is this content computed from the current, live
config/entity graph at build/eval time, or is it a thin writer (e.g. a `writeText`-style wrapper) around hand-authored
strings — a fixed table, hardcoded counts, a name, a copyright line, an email?

- **Live-derived**: safe to rerun any time. It can't go stale because it's recomputed fresh every run.
- **Static prose wrapped in a generator**: rerunning only re-stamps whatever the hand-authored source text currently
  says. If that source is stale, the output stays stale — "regenerating" accomplishes nothing until the source text
  itself is edited.

### Step 1b: Confirm exactly one generator owns the target file ⚠️ REQUIRED

Before regenerating, confirm exactly ONE generator owns the target path. Two modules writing the same file is a silent
trap: whichever ran last wins on disk, and if one is enforced by a repo check (e.g. a per-file `nix flake check` registered
by a file-generation module, often with no exclusion option) while another overwrites it, the check and the committed
file drift.

- Grep the whole repo for the target filename across generator modules, not just the one you happen to be looking at.
- If two own it, pick a single owner and route the other elsewhere — e.g. README = the checked static-prose writer; the
  live topology chart to a _separate_ file like `TOPOLOGY.md`.
- A checked static-text writer and a separate imperative `cp` cannot co-own one path — the check enforces one text while
  the copy stamps another (e.g. a check-enforced `README.md` prose writer vs. a diagram script that copies its own
  rendering over the same file).

### Step 2 (conditional): Fix hand-authored source text first

If Step 1 found static content, do not run the generator expecting it to fix anything. Edit the hand-authored strings
directly — this may require asking the user for values that can't be derived from the repo (ownership, identity, contact
fields).

### Step 3: Verify in an isolated worktree, not the real tree

Whenever there's any chance the output could conflict with something already committed, or the output just needs review
before being trusted:

```
git worktree add --detach /tmp/<name>-verify HEAD
# copy in any uncommitted edits that should be reflected in the test run
cd /tmp/<name>-verify && <regeneration command>
# inspect the output; copy back only what's been reviewed
cd - && git worktree remove --force /tmp/<name>-verify
```

NEVER run the regeneration command directly against the real working tree as the default verification step.

**Drive that worktree with plain `git` and native file tools.** Any session tool that latches a project root from
directory markers (some MCP filesystem/context servers do) can re-root the whole session onto the throwaway worktree —
it carries a full set of project markers — jailing later path-taking calls out of the real repo. If unrelated reads
start failing on paths that plainly exist right after touching the worktree, suspect that re-rooting and reconnect the
tool rather than debugging the paths.

### Step 4 (conditional): Rule out a stale cache before chasing a content bug

If regenerated output looks impossibly wrong given the actual checked-out tree — it references files, entities, or names
that are verifiably absent from both the working tree _and_ git history — ask: could this be a stale build/eval cache
rather than a real content bug? Retry with the build tool's cache-bypass flag first (e.g. Nix's `--no-eval-cache`)
before auditing source files for a bug that may not exist.

### Step 5: Write back to the real tree only once verified

Diff the final result before committing.

## Anti-Patterns to Avoid

- Treating "run the regenerate-docs command" as automatically trivial without first reading the generator's source to
  classify it.
- Running a generator directly against the real working tree as the default verification step instead of an isolated
  worktree.
- Reading or running inside the verification worktree with a project-root-latching session tool, or handing its path to
  a subagent that shares the session's tool state — either can re-root the session out of the real repo, and the
  failure looks nothing like its cause.
- Spending time auditing source files for a "content bug" before trying a cache-bypass flag, when the eval/build result
  contradicts the actual checked-out tree.
- Regenerating a file without confirming only one generator writes it — a second writer silently reverts or drifts it,
  and a flake-check may enforce the loser.

## Pre-Delivery Checklist

- [ ] Generator source was read and classified as live-derived or static before running it
- [ ] The target file was confirmed to have exactly one owning generator (no competing writer that a flake-check might
  enforce against)
- [ ] Any static hand-authored content was fixed at the source, not papered over by rerunning the generator
- [ ] Regeneration was tested in an isolated worktree before touching the real tree, driven with plain `git` and native
  file tools rather than any project-root-latching session tool
- [ ] A cache-bypass flag was tried before concluding an impossible-looking result is a real content bug
- [ ] Final output was diffed and reviewed before being written to the real tree
