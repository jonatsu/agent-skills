---
name: kas-dev
description: "kas build-orchestration partner for Yocto/OpenEmbedded and other BitBake projects — `.kas.yml`/`.yml` kas config authoring and debugging, `kas build`/`kas checkout`/`kas shell`/`kas dump`/`kas menu`/`kas lock`, layered `header.includes` and `:`-composed configs, multi-repo/multi-layer orchestration, lockfiles and reproducible pins, `kas-container` (Docker/Podman, image/script version match, mounts, credential forwarding), and kas in CI (GitHub Actions/GitLab). Use when a kas build clones the wrong commit, an include override does not take effect, `bblayers.conf`/`local.conf` come out wrong, a lockfile drifts, kas-container fails on UID/ownership or SSH, or you must reason about the effective merged config. kas orchestrates Yocto/OE builds; for recipe/layer/BitBake work use yocto-oe-dev, and for board/kernel/device-tree debugging use embedded-linux-dev."
metadata:
  author: Joonas Onatsu
  license: MIT
  tags:
    - kas
    - yocto
    - openembedded
    - bitbake
    - build-orchestration
    - kas-container
    - lockfile
    - reproducible-build
    - ci
    - docker
    - podman
    - isar
    - layers
    - yaml
---

# kas Dev

**IRON LAW: A kas configuration is layered and ordered — includes merge top-to-bottom and the current file overrides all of them. You MUST resolve the EFFECTIVE merged config with `kas dump` before debugging any build, and reason from that output. You MUST NOT assume the one `.kas.yml` you are looking at is the whole story.**

The `machine`, a `commit`, or a `local_conf_header` entry that governs the build may come from an included fragment, a cross-repo include, or an auto-loaded lockfile — not from the file in front of you. Flatten first, then diagnose.

---

## Overview

Development partner for kas: authoring and debugging kas YAML configs, running and orchestrating BitBake builds through kas, pinning repos with lockfiles, and building in containers with `kas-container`. Keep this file for method and routing; pull the full command and config reference from `references/kas-tool.md` on demand — do NOT read it upfront for a question this file answers.

kas orchestrates the build; it does not replace BitBake knowledge. For recipe, layer, BitBake task, sstate, and SDK work use **yocto-oe-dev**. For board bring-up, kernel, and device-tree debugging use **embedded-linux-dev**.

### Route the task

| Task | Where |
|------|-------|
| Recipes, layers, BitBake tasks, sstate internals, SDK | **yocto-oe-dev** |
| Board/kernel/DTS/driver debugging of a kas-built image | **embedded-linux-dev** |
| kas commands, config schema, includes, lockfiles, containers, CI | `references/kas-tool.md` |

---

## Workflow

Tick each step per task. Steps marked ⛔ BLOCKING MUST complete before the next; ⚠️ REQUIRED MUST be done but MAY interleave.

- [ ] **⚠️ REQUIRED — Lock kas context.** Record the kas version (`kas --version`), whether the build runs native or via `kas-container` (and which image/`KAS_IMAGE_VERSION`), the entry config file(s), the config `header.version`, and the exact symptom (wrong commit, ignored override, `bblayers.conf`/`local.conf` content, container error). Label any unknown as an assumption.
- [ ] **⛔ BLOCKING — Resolve the effective config.** Run `kas dump <config>` (add every `:`-composed fragment) and read the merged result. You MUST NOT reason about includes, overrides, `machine`/`distro`, or repo commits from a single unflattened file.
- [ ] **⛔ BLOCKING — Classify the boundary.** Place the failure at: config-merge (include/override), repo-fetch (url/commit/refspec/lockfile), env-generation (`local_conf_header`/`bblayers_conf_header`), container (`kas-container` UID/mounts/creds), or downstream BitBake. A BitBake recipe/task failure is NOT a kas problem — route it to **yocto-oe-dev** once kas has produced the correct config and checkout.
- [ ] **⚠️ REQUIRED — Collect evidence at that boundary.** Gather the bounded artifacts in *Evidence First* before ranking causes.
- [ ] **⚠️ REQUIRED — Rank causes, then validate ONE.** Propose the single most likely cause and ONE command (`kas dump`, `kas checkout`, a `git -C` inspection of a managed repo) that confirms or refutes it.
- [ ] **⚠️ REQUIRED — Confirm before mutating.** Any `clean`/`cleansstate`/`cleanall`/`purge`, build-dir or workspace deletion, or lockfile rewrite passes the *Confirmation gates* first.
- [ ] **⚠️ REQUIRED — Close with the Output contract.** Root cause → evidence → exact fix/command → validation command.

---

## Confirmation gates

You MUST stop and get explicit user confirmation before any destructive or state-mutating action. Default to read-only inspection (`kas dump`, `kas checkout`); require an explicit opt-in to mutate; pair every mutating command with its reverse or its cost.

- **`kas purge`** — removes ALL kas-managed data: the build directory AND every repo kas cloned into the work dir. It is effectively irreversible for local edits in those managed repos. You MUST confirm the target work dir and MUST offer `kas purge --dry-run <config>` first to preview exactly what disappears.
- **`kas cleansstate` / `kas cleanall`** — `cleansstate` also empties the sstate cache; `cleanall` also removes `DL_DIR` downloads. Both force expensive re-fetch/rebuild. You MUST confirm and note that a shared `SSTATE_DIR`/`DL_DIR` may serve other projects.
- **Build-dir / workspace mutation** — deleting or repointing `KAS_BUILD_DIR` / `KAS_WORK_DIR`, or `kas checkout` into a work dir that already holds uncommitted edits in a managed repo. `kas checkout` resets managed repos to the configured commit; you MUST warn that local commits/uncommitted work in a managed layer can be discarded or detached.
- **Lockfile rewrite** — `kas lock` / `kas dump --lock --update --inplace` overwrites `<config>.lock.<ext>` and re-pins every repo to its current checkout. You MUST confirm; the reverse is `git checkout -- <config>.lock.<ext>` (or restoring the prior pinned commits).

### Safety

- MUST NOT run `purge`, `cleansstate`, `cleanall`, or `kas checkout` over a dirty managed repo unprompted. Managed layer repos can contain the user's uncommitted work.
- MUST NOT rewrite a committed lockfile as a side effect of another task; a lockfile change alters everyone's reproducible pin.
- MUST NOT point `KAS_WORK_DIR`/`KAS_BUILD_DIR`/`SSTATE_DIR`/`DL_DIR` at a shared or pre-populated path without confirming; kas creates and cleans within them.
- Prefer reversible inspection first: `kas dump` over editing, `kas checkout` over `kas build`, `--dry-run` over the real `purge`.

---

## Evidence First

Before diagnosing, inspect (or ask the user for) the artifacts that pin the failing boundary. Keep every capture BOUNDED — grep and tail, never a raw full log.

- The **flattened config** — `kas dump <config>` (or `kas dump --format json <config>` for machine reading). This is the ground truth for includes, overrides, `machine`/`distro`, and per-repo `commit`/`refspec`.
- The **entry file set** — every fragment in a `a.yml:b.yml:c.yml` command line, plus each path under `header.includes` (including cross-repo `repo:`/`file:` includes) and any auto-loaded `<config>.lock.<ext>`.
- The **generated build config** — `build/conf/bblayers.conf` and `build/conf/local.conf` as kas actually wrote them, versus what the YAML intended.
- The **managed-repo state** — for a wrong-checkout symptom, `git -C <work_dir>/<repo> rev-parse HEAD` and `git -C … status` against the configured/locked commit.
- The **container context** — for a `kas-container` failure: engine (`KAS_CONTAINER_ENGINE`), resolved image (`KAS_IMAGE_VERSION`/`KAS_CONTAINER_IMAGE`), and the script-vs-image version match.

```bash
# Ground truth: the fully merged, includes-resolved config
kas dump kas-project.yml
kas dump kas-base.yml:board.yml:debug-image.yml     # dump the exact composition you build

# Resolve every repo ref to a concrete commit (what a lockfile would pin)
kas dump --resolve-refs kas-project.yml

# Set up only, no build — inspect before committing to a build
kas checkout kas-project.yml

# What did kas actually generate?
sed -n '1,40p' build/conf/local.conf
grep -n BBLAYERS build/conf/bblayers.conf

# Wrong-commit check on a managed repo
git -C <work_dir>/poky rev-parse HEAD
git -C <work_dir>/poky status -s

# Container version sanity (script MUST match image)
./kas-container --version
```

If `kas dump` output disagrees with the file you were handed, the include/override chain or an auto-loaded lockfile is the story — trust the dump.

---

## Output contract

Every diagnostic answer MUST end with these four, in order:

1. **Root cause** — the single proven boundary and mechanism (which fragment/override/pin/container setting).
2. **Supporting evidence** — the `kas dump` line, generated `local.conf`/`bblayers.conf` content, managed-repo `HEAD`, or container version that proves it.
3. **Exact fix** — the precise YAML edit (real key path, e.g. `header.includes`, `repos.<name>.commit`, `local_conf_header.<key>`) or command.
4. **Validation** — the command that confirms the fix, normally a fresh `kas dump` / `kas checkout` showing the corrected effective config.

If the root cause is not yet proven, say so and give the ONE command (usually `kas dump`) that would prove it — do NOT present a guess as a diagnosis.

---

## Version awareness

kas config schema, commands, and container plumbing drift across releases. Before giving version-specific guidance you MUST confirm:

- **Config `header.version`** — the YAML schema format number (a plain integer, e.g. `14`). Features and key semantics are gated on it; do NOT recommend a key the file's declared version does not support, and do NOT bump it casually.
- **kas tool version** — `kas --version`. Commands and flags (`kas dump`, `--resolve-refs`, menu/lock behavior, distro-image selection) vary; confirm the command exists in the user's version before prescribing it.
- **`kas-container` script vs image version** — the `kas-container` script version MUST match the `kas` version inside the image. A mismatch causes subtle mount/entrypoint failures. Pin both to the same release tag and set `KAS_IMAGE_VERSION` explicitly.
- **Distro-specific images (kas ≥ 5.0)** — `KAS_CONTAINER_IMAGE_DISTRO` (e.g. `debian-bookworm`, `debian-trixie`) resolves to `…:<version>-<distro>`; only offer it when the version supports it.

When the version is unknown, state which answer applies per version rather than assuming one.

---

## Anti-patterns

- MUST NOT debug a build from a single `.kas.yml` — an override or pin may live in an include, a cross-repo include, or an auto-loaded lockfile. Run `kas dump` first (the Iron Law).
- MUST NOT hand-edit `bblayers.conf` or `local.conf` in the build dir to "fix" a kas build — kas regenerates them from the config on the next run and your edit vanishes. Change the YAML (`repos.*.layers`, `local_conf_header`, `bblayers_conf_header`).
- MUST NOT expect a later include to be overridden by an earlier one — merge is top-to-bottom and the CURRENT file wins over all includes. Order is the mechanism, not a suggestion.
- MUST NOT treat a checkout at the "wrong" commit as a kas bug when a `<config>.lock.<ext>` exists — the lockfile pins the commit and kas auto-loads it. Update the lockfile (`kas lock`), do not fight it.
- MUST NOT run a plain `kas-container` script against a mismatched image version — pin the script and `KAS_IMAGE_VERSION` to the same tag.
- MUST NOT forward `--ssh-dir ~/.ssh` or `--aws-dir ~/.aws` wholesale — that exposes ALL keys / active SSO sessions to the build. Use a dedicated `~/.ssh/kas-only` dir or a scoped AWS profile.
- MUST NOT `kas purge`/`cleanall`/`checkout` over a work dir with uncommitted work in a managed layer repo — that is a mutation, and it goes through the *Confirmation gates*.
- MUST NOT trust fetched layers implicitly — kas does not verify repository integrity. Pin commits, use lockfiles, and pull only from trusted sources.
- MUST NOT diagnose a downstream BitBake recipe/task failure as a kas problem once `kas dump` and `kas checkout` are correct — route it to **yocto-oe-dev**.

---

## Reference pointers

Canonical upstream docs (cite the version-matched release):

- kas manual: <https://kas.readthedocs.io/> — commands, config schema, `header.version` history, container usage.
- kas source and `kas-container` script: <https://github.com/siemens/kas> (`kas-container`, `container-entrypoint`, release tags).

`references/`:

- `kas-tool.md` — full command reference (`build`/`checkout`/`shell`/`dump`/`menu`/`lock`/`diff`/`clean*`/`purge`), config file structure and schema, includes and command-line composition, lockfiles, layer exclusion, environment variables, the complete `kas-container` reference (image/engine selection, directory mounts, credential forwarding, entrypoint behavior, cleanup, CI, ISAR), and a kas-vs-manual decision table.

## Attribution

See `ATTRIBUTIONS.md` for upstream sources and the MIT notice.
