---
name: agent-repo-docs
description: "Generate or update AGENTS.md (agents.md standard) and llms.txt (llmstxt.org format) for a repository, populated from verified repo facts and kept consistent with each other and the README. Use when the user says 'add AGENTS.md', 'create an agents file', 'write llms.txt', 'generate agent docs', 'document this repo for coding agents', 'document this repo for LLMs', 'update the AGENTS.md', 'make an onboarding file for agents', or mentions agents.md / llms.txt. Actions: generate, create, write, update, refresh, sync AGENTS.md or llms.txt."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Agent Repo Docs

IRON LAW: NEVER write a command, path, convention, or link you have not verified against THIS repository. AGENTS.md and llms.txt describe the actual repo — no invented build/test commands, no placeholder text, no dead links. If a fact can't be verified, flag it for the user instead of guessing.

## What each file is (don't mix them up)

- **AGENTS.md** — a "README for agents": plain Markdown instructions a coding agent needs
  (setup/build/test commands, code style, conventions, gotchas). No required fields, any
  headings. It is NOT a copy of the README (README is for humans; keep it concise).
- **llms.txt** — a link index for LLMs at repo root: an H1, an optional summary blockquote,
  optional detail prose, then H2 sections of curated links to the repo's docs. It is NOT an
  instruction doc.

## Workflow

```text
Agent Repo Docs Progress:

- [ ] Step 1: Scope ⚠️ REQUIRED — which file(s), repo root, create vs update, monorepo?
- [ ] Step 2: Inspect the repo ⚠️ REQUIRED — gather VERIFIED facts (no guessing)
- [ ] Step 3: Confirm plan ⚠️ REQUIRED — sections/links + unverifiable items, get approval
- [ ] Step 4: Write AGENTS.md (agents.md standard)
- [ ] Step 5: Write llms.txt (llmstxt.org format)
- [ ] Step 6: Consistency + link check
- [ ] Step 7: Deliver — summary + flagged unknowns
```

## Step 1: Scope ⚠️ REQUIRED

Ask / determine: AGENTS.md, llms.txt, or both? Is this the repo root? Do the files already
exist (→ update/diff, don't blind-overwrite)? Is it a monorepo (→ AGENTS.md may nest per
package; agents read the nearest file, closest wins)?

## Step 2: Inspect the repo ⚠️ REQUIRED

Gather only facts you can see. Ask:
- What are the real setup/build/test/run commands? Find them in `package.json` scripts,
  `Makefile`, `justfile`, `mise.toml` tasks, `pyproject.toml`, CI workflows — do NOT invent
  conventional-looking commands. If unsure a command works, mark it unverified.
- What language/toolchain, and which linters/formatters/config actually exist?
- What is the directory structure and where do the real docs live (README, `docs/`, ADRs)?
- What conventions are evidenced (commit style from `git log`, existing `CONTRIBUTING`,
  editorconfig)? What agent gotchas exist (generated files, restart requirements, secrets)?
- What does the README already cover? (AGENTS.md MUST NOT duplicate it.)

## Step 3: Confirm plan ⚠️ REQUIRED

Present the file(s) to write/change, the section list (AGENTS.md) and link list (llms.txt),
and any facts you could NOT verify. ⚠️ Get approval before writing — especially before
overwriting an existing file; show a diff of what changes.

## Step 4: Write AGENTS.md

Plain Markdown, root of the repo (or per-package for monorepos). Include only sections the
repo justifies; common ones: `## Setup commands`, `## Build & test`, `## Code style`,
`## Dev environment tips`, `## Conventions`, `## PR / commit guidelines`, `## Security`,
`## Gotchas`. Every command copy-pasteable and verified. Instructions agents need — not a
README rehash. Start from `assets/AGENTS.template.md` if helpful.

## Step 5: Write llms.txt

Follow the llmstxt.org structure exactly, in order:
1. `# Project Name` (H1, required).
2. `> One-sentence summary blockquote` (optional, recommended).
3. Optional detail paragraph(s) — any Markdown except headings.
4. `## Section` blocks, each a list of `- [title](url): optional note` links to real docs.
5. An `## Optional` section last for secondary links that MAY be skipped for shorter context.

Links MUST resolve (relative paths for an in-repo file, or real URLs). Start from
`assets/llms.template.txt` if helpful.

## Step 6: Consistency + link check

Confirm: AGENTS.md and llms.txt agree with each other and the repo; every llms.txt link
resolves; AGENTS.md duplicates nothing from the README; no placeholder text survived.

## Step 7: Deliver

Summarize what was written/changed and list anything left unverified (so the user can fill
it). Keep both files in sync on future edits — update both when repo facts change.

## Anti-Patterns

- Inventing conventional-looking build/test commands not present in the repo.
- Placeholder residue: `TODO`, `your-email@example.com`, `https://example.com`, fake badges.
- Duplicating the README into AGENTS.md — they have different jobs and audiences.
- llms.txt links that 404 or point to nonexistent files.
- Overwriting an existing AGENTS.md/llms.txt without diffing and confirming.
- Putting instructions in llms.txt (it's a link index) or link-dumps in AGENTS.md.
- Treating AGENTS.md as having "required fields" — it is free-form Markdown.
- One giant root AGENTS.md for a monorepo instead of nested, nearest-wins files.

## Pre-Delivery Checklist

- [ ] Every command / path / convention was verified against the repo (located or run).
- [ ] No placeholder text remains (TODO, FIXME, example.com, your-email).
- [ ] AGENTS.md holds agent instructions and does NOT duplicate the README.
- [ ] llms.txt follows the llmstxt.org order (H1 → optional blockquote → detail → H2 link
      lists → `Optional`), and every link resolves.
- [ ] AGENTS.md and llms.txt are mutually consistent.
- [ ] Any pre-existing file was diffed and its changes confirmed, not silently replaced.
- [ ] Unverifiable facts were flagged to the user, not guessed.
