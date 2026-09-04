# Archived: nix-dendritic-pattern

**Archived 2026-09-03**, at the user's direction, immediately after its skill review completed. Renamed from
`dendritic-pattern` in the same move, because the old name did not say Nix and read as neural or graph
terminology; the new name matches its former siblings `nix-flakes`, `nix-packaging` and `nix-secrets`.

Last deployed as `dendritic-pattern` from `skills/shared/nix/` to Claude Code, OpenCode, Copilot CLI and
Codex.

## Why it was archived

The review found no defect in the pattern knowledge itself. It found that the skill has exactly one consumer,
`~/src/nix-config`, and that the consumer already ships nine repository-local `dendritic-*` skills covering
this package's whole surface: aspect authoring, class authoring, policy authoring, schema authoring, pipes,
entity scaffolding, package authoring, debugging, and a den capability lookup. Those nine total about 1 800
lines, split one skill per task, and they live in the repository they govern, so they are reachable at the
moment the work happens and cannot drift from the flake they describe.

A globally deployed 25 KB skill duplicating that set costs discovery budget in every session on four agents
while adding nothing for the one repository that needs it. Nothing else in the setup uses den.

Archived rather than deleted because the package holds source-verified corrections that den's own published
documentation still contradicts, and re-deriving them is expensive.

## The exception to the byte-identical rule

`skills/archived/README.md` requires an archived `SKILL.md` to stay byte-identical to what was last deployed.
**This package deliberately does not.** The user asked for the skill to be repaired to a usable state before
archiving, so the reference copy is the corrected version rather than the deployed one. The exact deployed
bytes remain recoverable from git history at the commit before this one.

The repairs, all made 2026-09-03:

- The revision pin moved from `2040b613` (2026-08-10) to `e8e8de1e` (2026-08-11), which is what
  `~/src/nix-config/flake.lock` actually pins. Under the skill's own rule the old pin left every API claim
  formally unverified from the day it was written.
- The required verification step named `ctx_git_read`, a lean-ctx tool removed from this machine on
  2026-08-27, and forbade the local clone that the global tool rules prescribe. It now gives a shallow
  blobless scratch-clone recipe.
- Four claim sets were re-verified against `e8e8de1e` and now cite how they were measured: the 15 batteries
  by enumerating every `den.batteries.<name> =` assignment site; the auto-activated integrations by reading
  `os-class.nix`, `os-user.nix`, `wsl.nix`, `home-manager.nix`, `hjem.nix` and `maid.nix`, none of which
  assigns a battery; the absence of `validators`; and the pipe-then-class-then-nested key order in
  `classifyKeys`.
- The `oneOfAspects` and `meta.adapter` citation was corrected. Both survive only in a docstring at
  `modules/context/has-aspect.nix` and in `templates/example/modules/aspects/hasAspect-examples.nix`, not in
  the example template path the skill previously named.
- A version boundary was added to "multiple files can contribute to the same aspect". Before `e8e8de1e` a
  nested aspect key defined as a parametric function in one file and a plain attrset in another silently lost
  one side; `e8e8de1e` is the commit that fixed it.
- The description dropped below the 512-character repository budget, and the bare trigger tokens `den` and
  `aspect` were removed as too generic to route on.

## What was found but deliberately not repaired

These are real findings, left in place because they do not impair usability and the package was on its way to
the archive. Fix them if it is ever restored.

- The `policyInspect` two-blind-spots paragraph is duplicated near-verbatim in `references/policies.md` and
  `references/debugging.md`, and neither is loaded before the other.
- Three checklists overlap: the Workflow progress block, Step 5 Verify, and the Pre-Delivery Checklist, in a
  522-line always-loaded entrypoint.
- The five Silent Failures bullets are carried forward from `2040b613` rather than re-traced at `e8e8de1e`;
  the section says so.
- No behavioral evaluation has ever run against this package.

## Successors

- `~/src/nix-config/.agents/skills/dendritic-*` and `CONTEXT-MAP.md` are where den guidance lives now.
- `nix-flakes`, `nixos-config`, `home-manager` and `nix-secrets` each carried a pointer telling the agent to
  load this skill. All four were rewritten in the archiving commit to point at the configuration repository
  instead, because a pointer to an undeployed skill is a dead instruction.

**Later the same day the rest of the `nix` domain followed**, for the reason this review found, and this
package moved from `skills/archived/nix-dendritic-pattern/` to `skills/archived/nix/nix-dendritic-pattern/`
so the domain is archived in one restorable piece. Those four rewritten pointers are therefore archived too;
they are still correct, and they are what a restore should keep. See the `nix` domain entry in
`docs/evaluations/2026-09-shared-skill-review.md`.
