# Trusting the Build Itself

Everything else in this skill assumes the build produced what its metadata says. These are the controls over
that assumption. `yocto-openembedded-development` owns the *mechanics* of sstate, mirrors and fetching; this
file owns their **trust properties** and states them where they differ from the defaults.

## sstate is unauthenticated by default

`sstate.bbclass` at `yocto-5.0.12`:

```bitbake
SSTATE_SIG_KEY ?= ""
SSTATE_SIG_PASSPHRASE ?= ""
SSTATE_VERIFY_SIG ?= "0"
SSTATE_VALID_SIGS ??= ""
```

So out of the box, **sstate artefacts are neither signed nor verified**, and an sstate mirror is a source of
executable content that the build trusts on the strength of a filename hash. That matters more than it sounds:
an sstate hit substitutes a prebuilt artefact for a task you believe you compiled.

To sign and verify:

```bitbake
SSTATE_SIG_KEY = "<gpg key id>"      # on the machine that produces artefacts
SSTATE_VERIFY_SIG = "1"              # on every machine that consumes them
SSTATE_VALID_SIGS = "<key fingerprints or a signature-validation list>"
```

**Prove the negative case.** Verification that has never rejected anything is not evidence: build an archive
signed with a key outside `SSTATE_VALID_SIGS`, put it in the mirror, and confirm the consuming build refuses
it rather than silently falling through to a rebuild.

**Related trap:** `BB_SIGNATURE_HANDLER` is not the setting that does any of this — it selects a task-hash
generator and falls back to `noop` on an unrecognised name. See `misleading-controls.md` §7.

**Upstream documents no integrity or provenance model for sstate mirrors.** Two independent surveys of the 5.0
and 6.0 reference manuals found no signature, integrity or provenance discussion in the sstate and mirror
chapters, while 6.0 turns hash equivalence on by default and ships a fragment pointing at a public CDN mirror.
State this as a **gap** — do not cite a manual section for a control that is not described there, and do not
present the variables above as an upstream-recommended workflow they are not.

## Mirrors disclose what you build

Poky's default `PREMIRRORS` send fetch requests for your components to external hosts, which discloses the
*names and versions* of what a product is built from. For a closed product that is a confidentiality decision,
not a performance setting. Own mirrors plus `BB_NO_NETWORK` or `BB_FETCH_PREMIRRORONLY` make the disclosure
and the reproducibility question the same decision.

The same shape, one step stronger, applies to any tool that uploads a package manifest to a hosted service for
CVE monitoring: it discloses the product's complete software composition with versions to a third party.
Legitimate under a supplier agreement; never something to enable incidentally. Tool selection for that work
belongs to vulnerability management, not here.

## Source integrity

- **`SRC_URI[sha256sum]` is a compromise-detection control**, not a nicety: it is what fails the build when a
  release tarball is replaced on a compromised upstream server. A recipe fetching a tarball with no checksum
  has no such detection.
- **`SRCREV = "${AUTOREV}"` in a release recipe** means the build follows whatever the branch head is at build
  time. It is unreproducible, it defeats air-gapped builds, and it means a compromised upstream branch reaches
  your image without any metadata change to review. Pin a commit SHA.
- **`git://` without `protocol=https`** for a fetch that ends up over an unauthenticated transport is worth a
  second look; the checksum protects a tarball, and a git SRCREV protects a clone, but only if the SRCREV is
  pinned.

```bash
bitbake -e <recipe> | grep '^SRC_URI='
bitbake-getvar -r <recipe> SRCREV
```

## Reproducibility as a security property

Reproducibility is what lets a third party — a customer, an auditor, or you after an incident — rebuild the
shipped artefact and get the same bits, which is the only mechanical way to check that the released binary
corresponds to the released source. Both reference manuals frame it in exactly those terms, with the same
non-guarantee: **adding any layer voids the upstream reproducibility claim**, because the guarantee covers
OE-Core and its own layers, not yours.

OE-Core ships the test:

```bash
oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds
```

It builds twice and diffs the packages, using `diffoscope` for the report. It is slow and it is the real
check; `buildpaths` in `WARN_QA` catches one common cause (host paths in artefacts) far more cheaply, which is
an argument for promoting it to `ERROR_QA` on a product distro.

**`TCMODE` pointing at an external toolchain** trades reproducibility and traceability for convenience: the
compiler that built the product is then not described by the metadata. Say so when it is in use.

## Release-gate shape

The controls above are the ones a release process, not a developer, has to own:

| Question at release time                         | Evidence, not a setting                                                                      |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Did every artefact come from a build we control? | sstate signing verified with a deliberate bad-key rejection                                  |
| Can we rebuild this exact image?                 | a passing reproducibility run, plus pinned `SRCREV`s and archived `DL_DIR`                   |
| Did we disclose the composition to anyone?       | the mirror and monitoring-service configuration, decided explicitly                          |
| Are the sources we must offer actually captured? | `archiver` output — mechanics and licence obligations are `yocto-openembedded-development`'s |

CVE reporting, SBOM generation and the evidence package handed to a customer belong to vulnerability
management, which is a separate skill and a separate cadence.
