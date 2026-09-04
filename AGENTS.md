# AGENTS.md: skills/

Instructions for agents working under `skills/`. `CLAUDE.md` is a symlink to this file.

Read the focused source before acting:

- `README.md` describes the deployed stack and normal add, edit, remove, and sync workflows.
- `skills-review-notes.md` is the authoritative review ledger and explains why the review exists.
- `archived/README.md` defines the archive procedure and recovery commands.
- `TODO.md` contains operational and future-feature backlog only. It is not a skill-review ledger.

## Authoring and Review

- Use `skill-forge` when creating, editing, restructuring, or replacing a skill.

- Use both `skill-review` and `skill-forge` for every skill review. `skill-review` governs assessment and
  evidence; `skill-forge` governs proposed repair shape and any separately authorized edits.

- Load `kasetto` before adding, editing, moving, archiving, restoring, removing, deploying, or verifying a
  skill. Its portable tool guidance complements this file's repository-specific hook and lock workflow.

- A review request does not authorize changing the skill. Report first unless the user also requested
  implementation.

- Update `skills-review-notes.md` in the same work. Move every completed skill to **Reviewed**, including a
  skill that is replaced or removed. Move a restored archived skill out of the deferred list when its review
  begins.

- Archived skills marked as deferred remain unreviewed. Do not spend time validating or repairing them unless
  their review is explicitly resumed.

- Keep `description` as an inline YAML scalar. **This constraint belongs to Kasetto, not to YAML or to the
  Agent Skills specification**, and it dissolves if the deployment tool is replaced. Kasetto 3.8.0 records a
  folded scalar's `>-` marker as the lock description instead of its text; reproduced on 2026-09-02 across
  all four shared locks, and again on 2026-09-03 on `claude/reflect`. Both skill validators accept the folded
  scalar, so neither catches the failure. `scripts/check-skill-descriptions.sh` does.

- **The 120-column ceiling governs prose and body text, never the `description`.** It is markdownlint's
  MD013, a line-width rule for wrapped prose, and a description cannot wrap while the constraint above holds.
  Frontmatter is already excluded mechanically: `.markdownlint-cli2.jsonc` sets a `frontMatter` regex that
  treats it as non-content, verified on 2026-09-03 when an 862-character description passed both Markdown
  hooks. Budget a description by length instead. The Agent Skills specification caps it at 1024 characters
  and `skills-ref` enforces that; this repository warns above 512, which is a local judgment about discovery
  cost rather than an upstream limit.

- **Validate one skill with `just skill-check <skill-directory>`, from the repository root.** It runs both
  validators — the Agent Skills specification through the vendored `skills-ref`, then skill-forge's local
  policy through `quick_validate.py` — labels each block, and fails if either does. Both run even when the
  first fails. The path may be relative to wherever you are; the scripts resolve it.

  Do NOT hand-assemble the underlying invocation. It needs `MISE_CACHE_DIR` and `MISE_STATE_DIR` under
  `skills/.cache/` so sandboxed validation needs no `/tmp` override, `mise exec -C skills` so
  `skills/mise.toml` supplies Python and uv, and `uv run` against the vendored validator project — which is
  why it was being retyped from memory and got parts wrong. `scripts/check-skill-spec.sh` and
  `scripts/check-skill-policy.sh` own that dance; both also take no argument to check the whole tree, which is
  how `just skills-spec`, `just skills-policy` and `just check` call them.

  **Running only one validator is the mistake the pair exists to prevent.** The specification validator passes
  a file that breaks every repository policy, and the policy validator does not check frontmatter shape at
  all. Report them separately; never describe one as covering the other.

  A cold cache needs pinned dependencies from PyPI. If it fails on dependency download or DNS, request
  network-enabled execution for the same command; report the failure as an environment limit, not a package
  defect.

## Archive Without Losing Structure

- Keep every package file intact. Leave its `SKILL.md`, references, scripts, attribution, and upstream license
  files byte-identical to the last deployed version.
- Move an individual package to `archived/<skill>/`. When archiving an entire shared domain, preserve the
  domain as `archived/<domain>/<skill>/` instead of flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md` and `skills-review-notes.md`.
- If a shared domain becomes empty, remove its entry from `kasetto/base.yaml` in the same source commit. Git
  cannot preserve an empty directory, and Kasetto rejects a configured domain that is absent on a fresh clone.
- Prune deployed copies with `./scripts/kasetto-deploy.sh`, then inspect all four destinations. A clean
  worktree or a green hook does not prove that a deployed copy disappeared.

## Verify Moves and Removals Explicitly

**Do not trust the post-commit redeploy hook to have deployed anything.** It reports `Passed` whether it
selected a scope or not, so its success tells you nothing about the destinations. Verify by inspecting them.

The hook maps the commit's changed paths — `git diff --no-relative --name-only HEAD~1 HEAD` — onto Kasetto
scopes. Only one row below has been observed since the hook was repaired on 2026-09-04, so treat the rest as
what the code is meant to do rather than as measurements. Re-measure a row before relying on it.

| Change                                                            | Expected behavior                                          | Verified   |
| ----------------------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| Edit, add, or delete within a deployed group                      | Selects that group                                         | 2026-09-04 |
| Move between domains inside `shared/`                             | Selects all shared destinations                            | never      |
| Move from `shared/` to `archived/` with no recognized config edit | Reported as selecting nothing                              | pre-fix    |
| Move between deployment groups                                    | Reported as selecting the destination, possibly not source | pre-fix    |
| Edit `kasetto/base.yaml`                                          | Selects Claude, OpenCode, Copilot, and Codex shared scopes | never      |

The two `pre-fix` rows were reproduced on `84cd615` (2026-08-27) and around `ab8baac` (2026-09-02), both while
the hook was selecting nothing for any change at all. Their stated cause — Git rename detection reporting only
the destination of a 100% rename — is therefore unconfirmed. `TODO.md` tracks the re-measurement.

Kasetto 3.8.0 does not prune a deployed directory when a source edit removes its last file. Reproduced on
2026-09-02 by deleting every file under `chezmoi-dotfiles/references/`: redeployment reported the skill
unchanged, while `just skills-deployed` found `Only in <destination>: references`. Removing the empty source
directory and redeploying did not repair the destination. Keep a meaningful file when the directory still
serves the skill; otherwise resolve the stale directory through Kasetto and verify all destinations. Never
edit the deployed copies directly.

After any move, archive, or removal:

1. Commit source changes separately from generated locks.
2. Run `./scripts/kasetto-deploy.sh` even if the post-commit hook reported success.
3. Confirm the removed name is absent from Claude, OpenCode, Copilot, and Codex skill directories.
4. Run `just skills-sync` for the required lock-only follow-up commit.
5. Run `just skills-deployed`; require zero drift, pending files, stray backups, and unresolved entries.

### Why the hook cannot be trusted on its exit status

A user-level `diff.relative = true` disabled it completely, for every kind of change, until 2026-09-04. The
hook pins its diff with `git -C "$SCRIPT_DIR"`, and `SCRIPT_DIR` is `scripts/` rather than the repository root,
so that setting made `git diff --name-only` report only paths under `scripts/`, relative to it. No changed path
could start with `skills/`, no scope was ever selected, and the hook exited 0 in 0.01s while pre-commit
reported `Passed` — so every skill commit silently depended on someone running `./scripts/kasetto-deploy.sh` by
hand. Repaired with `--no-relative`; `git diff-tree` ignores `diff.relative`, so the root-commit branch was
never affected. **The lesson outlives this one flag: a `-C` into a subdirectory combined with root-relative
pattern matching is a latent defect that any path-relative Git setting can trigger.**
