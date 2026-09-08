# Attributions

## Current skill

- Skill: `yocto-openembedded-development`
- Current author: Joonas Onatsu
- Declared license: MIT — **see "Unresolved licensing question" below before relying on this field**
- Status: mixed. Substantial original material, plus a best-practices reference established as a structural
  adaptation of a CC BY-SA source.

## Unresolved licensing question

**A 2026-09-07 provenance investigation established that `references/yocto-best-practices.md` is a structural
adaptation of a CC BY-SA 3.0 source, not an independent synthesis.** The previous version of this file asserted the
opposite — that rewriting in original words meant no CC BY-SA material was redistributed and attribution was a
courtesy. That conclusion was not supported, and the evidence below contradicts it.

Rewriting text in original words does not, by itself, end an adaptation. Selection and arrangement of material is
protectable, and CC BY-SA's BY and SA terms attach to a derivative work regardless of whether wording was changed.
Removing source-attributing framing does not help; it removes the attribution that BY requires.

The MIT declaration in `SKILL.md` therefore sits unresolved against the ShareAlike term of the adapted portion. This
is recorded, not decided: resolving it is a licensing decision for the repository owner, and no relicensing has been
performed. **No infringement finding is made here** — this file records an established source relationship and an open
question, not a legal conclusion. The realistic options are to license the affected reference compatibly, to replace
its structure with an independently derived organization, or to obtain a determination that the overlap is
uncopyrightable fact. Until one is chosen, treat the MIT field as covering the original material only.

## Established adaptation (CC BY-SA 3.0)

### Bootlin — Belloni, "OpenEmbedded and Yocto Project best practices"

- Author: Alexandre Belloni, Bootlin
- Edition inspected: Embedded Linux Conference Europe 2020; PDF created 2020-10-26; 30 slides
- Notice carried by the source: © Copyright 2004-2020, Bootlin. Creative Commons BY-SA 3.0 license.
- Upstream: <https://bootlin.com/> training and conference materials

The correspondence is systematic across selection, sequencing and specific technical choices, and is documented here
so a later reader does not have to re-derive it:

| Skill material                                        | Corresponding source material                                                                                        |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| "Where Does a Setting Belong?" scope decomposition    | consecutive slides `local.conf`, `local.conf - site.conf`, `local.conf - image recipes`, `- machine`, `- distro`     |
| distro-policy row contents                            | the distro slides' item list (toolchain/libc, init, `DISTRO_FEATURES`, `PREFERRED_PROVIDER*`, `PACKAGE_CLASSES`)     |
| "write your own image recipe … parse-order-safe"      | "core-image-\*.bb recipes are not enough anymore" + "not even easy for beginners due to parse order"                 |
| "Poky Is a Reference, Not a Product Base"             | the Poky and "Creating your own distribution" slides                                                                 |
| release capture sequence (phases 1–2)                 | the Network access slide: no `AUTOREV` → mirror tarballs → fetch all → archive `DL_DIR` → `PREMIRRORS`/`own-mirrors` |
| sstate sharing bullets                                | the "Sharing the sstate-cache" slide's four points, in the same order                                                |
| `sstate-cache-management.sh --remove-duplicated …`    | reproduced essentially verbatim from the "Cleaning the sstate-cache" slide                                           |
| `${LICENSE_DIRECTORY}/${IMAGE_NAME}/license.manifest` | the "Listing licenses" slide                                                                                         |
| `COPY_LIC_DIRS` / `COPY_LIC_MANIFEST` pairing         | the "Providing license text" slide                                                                                   |
| `INHERIT += "archiver"` shown with `configured`       | the "Providing sources" slide, including the same non-default mode as the worked value                               |

Two further pieces of evidence support adaptation over coincidence:

- **An inherited defect.** The skill carried `bitbake -c fetchall` — a Dunfell-era command the source uses — forward to
  a Scarthgap baseline where that task no longer exists. An independently written reference checked against a current
  release would not reproduce a stale command from a 2020 deck. (Corrected under F2 in the 2026-09-07 repair.)
- **The port brief said so.** The skill family's introducing brief (`26cc26d`, `docs/embedded-linux-port/port-brief.md`)
  instructed: if prose was "lifted (verbatim OR **structurally — same fact selection/sequencing**)" from the CC BY-SA
  learning sources, rewrite it in original words and remove source-attributing framing such as "Bootlin highlights…".
  That instruction concedes the structural lifting and prescribes exactly the two steps that produced this file's
  earlier, unsupported claim. It is historical evidence of what happened, not authority for the conclusion it reached.

## Informed by

### Yocto Project documentation

- Source: the Yocto Project manuals (Reference, BitBake, BSP, Kernel, Security, Development Tasks, Migration Guides)
- Upstream: <https://docs.yoctoproject.org/>
- Upstream license: CC BY-SA 2.0 UK

The manuals informed the BitBake-syntax, task-lifecycle, recipe-anatomy and compliance material, and are the primary
source for the 2026-09-07 technical corrections. Facts are stated generically and in original words; the
`references/official-doc-map.md` routing table is this skill's own organization.

This includes the Yocto Project's "What I wish I'd known about Yocto Project" document, which `SKILL.md` and
`references/official-doc-map.md` both point readers to by name. It carries the manuals' license and is recorded here
because the skill routes to it, not because passages were taken from it.

### awesome-yocto-ai-agent-skills (coverage gaps only)

- Author: Prashant Divate
- Upstream: <https://github.com/prashantdivate/awesome-yocto-ai-agent-skills>
- Upstream license: MIT (compatible with this package's declaration)
- Inspected 2026-09-08 at commit `0e268dc`

Reading that skill set on 2026-09-08 surfaced four subjects this package did not cover: packaging and the
`installed-vs-shipped` QA failure, `PACKAGECONFIG`, the collection-vs-directory distinction in `LAYERDEPENDS`, and the
assumption that build output sits under `tmp/`. The **selection of those gaps** is the influence and is recorded here
under this repository's policy that an external source is attribution-bearing whenever reading it changes what a skill
contains.

No wording, structure, examples or command choices were taken. Each subject was written from pinned Poky `yocto-5.0.12`
sources — `meta/lib/oe/package.py`, `meta/conf/bitbake.conf`, `meta/classes-global/{base,insane}.bbclass`,
`meta/conf/distro/defaultsetup.conf`, `meta-poky/conf/distro/poky.conf`, and `bitbake/lib/bb/cooker.py` — which state
mechanisms the upstream skill set does not (the `PACKAGES` first-match-wins ordering, `installed-vs-shipped` being an
`ERROR_QA` rather than a warning, `PACKAGECONFIG` declaring the whole enabled set, `TCLIBCAPPEND` as the actual reason
for `tmp-glibc/`). Its compliance, SBOM, CVE and bundled-script material was reviewed and not adopted.

### Verification-only sources

The 2026-09-07 review and repair verified behavior against pinned Poky `yocto-5.0.12` sources — `data_smart.py`,
`sstate.bbclass`, `package.bbclass`, `buildhistory.bbclass`, `bitbake.conf`, `knotty.py`, `devtool/deploy.py` — and the
Honister 3.4 migration guide. The 2026-09-08 packaging additions used the further pinned sources listed above.
These confirmed public facts and are cited near the affected claims. Under this
repository's provenance policy, verification-only use does not create an attribution obligation; they are listed for
traceability.

## Present but not established

`/home/user/src/embedded-linux/docs/yocto-project/` also holds Jérémie Dautheribes, "10 best practices for Yocto"
(Bootlin, Toulouse meetup 2024, CC BY-SA 3.0). It shares themes with this skill — "don't overuse `local.conf`", "don't
use Poky in production" — but the investigation found no distinctive correspondence in wording, sequencing, examples or
command choices beyond what the Belloni deck already accounts for. Shared subject matter between two decks by the same
organization is not evidence of copying, so **no source relationship is asserted here.** It is recorded only so a later
reader knows the file was inspected and why it was not listed above.

The skill's `Common Traps` table (the `# CONFIG_X is not set` spacing rule, `kernel-module-*` with a built-in symbol,
`UNPACKDIR`, `def` in a `.conf`, the `dlopen` plugin case, the `buildhistory` `MACHINE_ARCH`/`MACHINE` mismatch) has no
counterpart in any inspected deck and appears to be independent material.

## Scope of this investigation

Bounded, and complete enough to establish the relationship above but not a comprehensive copyright audit. Three PDFs
were converted to text and compared against the package by topic, sequence and command; the Yocto manuals were not
compared passage by passage; no other editions of the Belloni deck were located or checked; and no legal advice was
sought or given. A later reader should treat "no correspondence found" as a bounded negative result, not proof of
independence.
