# Official Documentation Map

Problem type → the exact upstream manual and section to read. Use this to answer
from primary sources instead of memory, and to land on the version-matched page.

**Read the map release-first.** The manuals at docs.yoctoproject.org are versioned;
the codename is a path segment in the URL
(`docs.yoctoproject.org/<version>/…`, e.g. `.../scarthgap/…`, `.../kirkstone/…`, or
`.../dev/…` for the tip). Variable behavior, class names, and task lists differ per
release, so confirm the codename (Iron Law) and open the matching version. When a
question is "did this change between releases?", the **Migration Guides** are the
authoritative answer, not the current Reference Manual.

## Contents

- [By Problem Type](#by-problem-type)
- [Manual Quick Description](#manual-quick-description)
- [Release-Sensitive Topics](#release-sensitive-topics)

## By Problem Type

| Problem / question | Manual | Section |
|--------------------|--------|---------|
| What does a variable mean / default to? | Reference Manual | Variables Glossary |
| What does a task do; task order? | Reference Manual | Tasks |
| Which class provides X; how to inherit it? | Reference Manual | Classes |
| A `do_*_qa` / QA error meaning | Reference Manual | QA Error and Warning Messages |
| Recipe/`.bb` syntax, operators, overrides, fetchers | BitBake User Manual | Syntax and Operators; Fetchers |
| `bitbake` command flags, `-e`, `-g`, `-c` | BitBake User Manual | The BitBake Command |
| Writing recipes, `devtool`, layers, images, SDK | Development Tasks Manual | (task-named sections) |
| Adding/porting a machine, `MACHINE`, BSP layout | BSP Developer's Guide | whole guide |
| Kernel recipe, config fragments, `KERNEL_DEVICETREE`, `linux-yocto` | Kernel Development Manual | whole guide |
| CVE workflow, `cve-check`, `CVE_PRODUCT`, status | Security manual | CVE Checking |
| SBOM / SPDX, `create-spdx` | Reference Manual | Classes → `create-spdx`; + Dev Tasks (SBOM) |
| License compliance, `LIC_FILES_CHKSUM`, `archiver` | Development Tasks Manual | Working with Licenses / Maintaining Open Source License Compliance |
| Did syntax/behavior change between releases? | Migration Guides | the release-to-release page |
| First-project pitfalls, hard-won gotchas | "What I wish I'd known" material + this skill's best-practices ref | — |

Device-tree binding validation (`dt-validate`, dt-schema) is not a Yocto manual
topic — see **embedded-linux-dev** and github.com/devicetree-org/dt-schema.

## Manual Quick Description

- **Reference Manual** — the encyclopedia: variables, tasks, classes, image
  features, QA messages. First stop for "what is `X`".
- **BitBake User Manual** — the language and the tool: metadata syntax, assignment
  and override operators, fetchers, and `bitbake` CLI. Note it versions with BitBake,
  not the Yocto codename, though the docs site cross-links the matching pair.
- **Development Tasks Manual** — how-to for real workflows: recipes, `devtool`,
  layers, images, SDK, licensing.
- **BSP Developer's Guide** — board/machine support layout and `MACHINE` mechanics.
- **Kernel Development Manual** — `linux-yocto`, config fragments, kernel patches.
- **Security manual** — CVE checking and the vulnerability workflow.
- **Migration Guides** — the definitive per-release change list; the *only* correct
  source for "when did this change".

## Release-Sensitive Topics

Confirm the codename before answering any of these; the answer is era-specific:

- **Override separator** — `_append`/`_remove` (pre-Honister), both (Honister 3.4),
  `:append`/`:remove` only (Kirkstone 4.0+). → Migration Guides.
- **Class location and names** — the split into `classes-recipe/` and
  `classes-global/`, and renamed/removed classes. → Migration Guides + Reference
  Manual (Classes) for the target release.
- **SPDX / SBOM** — `create-spdx` output layout and SPDX schema version (2.x → 3.x).
  → Reference Manual (Classes) for the release.
- **CVE status metadata** — the flag/variable used to record CVE triage
  (`CVE_STATUS[...]` and its predecessors). → Security manual for the release.
