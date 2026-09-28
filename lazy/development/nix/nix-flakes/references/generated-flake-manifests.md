# Generated Flake Manifests

Use this branch only when the repository generates `flake.nix`, or an equivalent dependency manifest, from a
separate source module. Most repositories hand-maintain `flake.nix`; a framework or flake style does not imply
generation by itself.

The source module and the repository's documented regeneration command are authoritative. The generated file
is completion evidence only after its complete diff has been inspected. A successful generator exit does not
prove that the result preserved earlier changes.

## Workflow

### 1. Confirm the generated-manifest relationship

Inspect the generated file's header for language such as "auto-generated" or "do not edit past this point."
Locate the source module, commonly named `flake-file.nix`, and the current regeneration command in the
repository's development shell, task runner, or documentation. Stop if the source or command cannot be
identified reliably.

### 2. Change only the authoritative source

Add, remove, pin, or update the input in the source module. Change any `follows` relationship there as well.
Do not hand-edit the generated region, even as a temporary fix.

### 3. Regenerate from the documented command

Run the repository's current regeneration command. If it is interrupted or its completion is uncertain,
inspect the source module, generated file, and working-tree diff before deciding whether it is safe to run
again.

### 4. Inspect the complete result

Read every hunk in the generated file's diff, not only the expected input change. Determine whether any hunk
reverts content rather than applying the intended change.

If regeneration would discard an earlier hand-edit, stop. Recover the original intent, incorporate it into
the source module, and regenerate again. If the intent cannot be established from repository evidence, report
the conflict instead of choosing which behavior to discard.

### 5. Verify an affected target

Evaluate or build at least one target that depends on the changed input. Completion requires the intended
source change, a generated result with no unexplained reversion, and a successful check of an affected target.
