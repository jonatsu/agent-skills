# Attributions

## Current Package

- Skill: `embedded-linux-bringup`
- Current author: Joonas Onatsu
- Package license: MIT, unchanged by the 2026-09-07 repair
- Composition: original runtime guidance, retained MIT adaptation, and historical training-material influence

The records below distinguish adapted material, independently expressed source influence, and interface verification.
Changing words or removing source framing does not eliminate attribution or determine whether expression is independent.

**These records are permanent.** A source entry is not closed by a later repair that replaces the material it
describes. Independent replacement changes what the current revision contains; it does not retract the revisions that
carried the adapted material, and those remain in this repository's history. Keep every entry — in the past tense once
the material is gone — so that a reader who reaches an older revision can still establish what the relationship was.

## Retained MIT Adaptation

- Author: heyu-233
- Project: [linux-embedded-dev](https://github.com/heyu-233/linux-embedded-dev)
- Reviewed revision: `53e7526e3ba3ffe4018845a58af328f897ffd60a`
- License: MIT, Copyright (c) 2026 heyu-233
- License artifact: [LICENSE.upstream](LICENSE.upstream), reproduced verbatim from that revision

The 2026-08-25 re-review recorded this revision; the first adoption revision was not recorded and remains unknown.
Do not assume they were the same tree. The license and relevant paths were checked again on 2026-09-07.
No separate upstream NOTICE file was present in that revision's tree inventory.

| Upstream path                                                                | Retained influence and treatment                                                                                                                                                         |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/camera-v4l2-workflow.md`                                         | Starting base for camera investigation. The local `camera-v4l2.md` changes its organization and adds media graph, capture, and diagnostic detail. Retained as an MIT adaptation.         |
| `references/perf-tuning-checklist.md` and `references/profiling-playbook.md` | Minimal capture versus application comparison, tuning order, readiness tradeoffs, and profile interpretation. Retained with corrected limits on what those observations prove.           |
| `references/full-link-debug-pipeline.md`                                     | The case of two host NICs on the board's subnet and successful ping with stalled SSH. Retained as a hypothesis to verify; source binding is not presented as a universal routing repair. |

The 2026-09-07 repair removes capture against sub-device nodes, qualifies compliance and performance evidence, and
adds hardware ownership and access requirements. The upstream MIT notice previously embedded in this file is preserved
in `LICENSE.upstream`; no notice text was discarded.

Earlier decisions retained for continuity: the upstream teaching modes, fixed tutoring response template, learning
roadmap, Windows writing advice, generic bus checklist, and `debugctl` CLI were not adopted.
The previous local deploy-verification script was removed because it could report success after a failed comparison.
Its removal does not justify adopting `debugctl` or another board-management framework.

## Historical Bootlin Influence and Independent Replacement

The earlier package acknowledged Bootlin embedded-Linux and debugging training as influences on cross-compilation and
kernel-debugging coverage. It incorrectly treated that attribution as courtesy after rewording and removal of source
framing. This record preserves the influence and removes that rationale.

Exact supplied sources were identified on 2026-09-07. Their original adoption revisions remain unknown.
Publisher/author: Bootlin, copyright 2004–2026. Both slide decks below declare CC BY-SA 3.0 and a 2026-06-09 update.

| Source                                                                                             | Relevant correspondence                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Embedded Linux slides](https://bootlin.com/doc/training/embedded-linux/embedded-linux-slides.pdf) | Local `full-embedded-linux-slides.pdf`, pages 62/64 and 396, 400–402: libc/static-linking choices, target dependency inspection, cross-host selection, prefix and staging. These subjects remain, expressed through the target ABI and build-interface diagnosis task. |
| [Debugging slides](https://bootlin.com/doc/training/debugging/debugging-slides.pdf)                | Local `full-debugging-slides.pdf`, pages 198, 200–204, 207–208: perf selection/probes and flame graphs. Page 208 contains the former `perf record -g -- sleep 30` example, which was corrected to explicit subject selection.                                          |

SHA-256 of the supplied embedded-Linux slides:
`dc5547daee08b315c6fb004a42d40d9611d11e7d3556fb339c80470e953480a3`.
SHA-256 of the supplied debugging slides:
`5caad435377baa735a9ff653e60c0c2dc793c8915e7e6541285eb92284906977`.
Online URLs may now serve different revisions; the hashes identify the inspected local documents.

The repair independently replaces the source-corresponding cross-compilation and debugging exposition with procedures
organized around artifact identity, actual command semantics, failure reporting, and runtime trust boundaries.
It does not adapt the slides' prose, teaching sequence, lab templates, or code into the replacement.
Training influence on retained subject selection remains acknowledged. Shared command syntax is checked as an interface
fact, not used as proof of either copying or independence. The unknown original authoring chain remains an evidence limit.

The local QEMU lab guide, dated 2026-06-08 and licensed CC BY-SA 3.0, was inspected at its identifying/setup pages.
It describes Cortex-A9 Versatile Express, not arbitrary real-board DTBs on `virt`. No lab content was adopted.
Its SHA-256 is `bbf32849ba984d523fc0dc4f4e569c6588dd19942ef50d48e69944e54f101cdf`.

## Removed Binding Example

The previous calibration example claimed an upstream i.MX thermal-binding origin but omitted a referenced cell.
The [Linux v6.12 binding](https://github.com/torvalds/linux/blob/v6.12/Documentation/devicetree/bindings/thermal/imx-thermal.yaml)
provides the relevant cell-name contract. The copied-style partial DTS example is removed; the reference now links
to the binding and asks the agent to resolve the actual SoC providers. No binding example code is retained.
The calibration-cell concept remains acknowledged as source influence; no Linux license is changed.

## First-party Interface Verification

The repair checks public interfaces and behavior against the sources linked at the relevant procedures:

- Linux v6.12: DT availability, devtmpfs, clock/reset behavior, regmap read side effects, V4L2 sub-device interface,
  module checks, perf, overlays, and dm-verity. Live kernel documentation links require matching the target release.
- QEMU v10.1.0: `virt` device model and generated DTB, explicit storage/network attachment, snapshot and debugger options.
- U-Boot v2025.10: post-verification FDT/bootargs modification; this skill does not implement FIT security policy.
- dtc v1.7.2: file-buffer growth and DT tooling behavior; native verification also exercises Ubuntu's dtc 1.7.0.
- RAUC v1.14: U-Boot attempt and confirmation semantics. SWUpdate's documentation supplies its own handler/verification
  contract; no framework-specific boot script is copied.
- GDB's server documentation: SSH stdio transport and TCP hostname/binding limitations.
- Yocto 4.3 documentation and OE's `nanbield` toolchain-environment implementation: SDK variables and flag preservation.
- Autoconf, CMake, Meson, cryptsetup, Valgrind, musl, libgpiod, i2c-tools, and NXP documentation: the specific interfaces,
  license caveats, and hardware-access constraints cited in the references.

No source implementation was vendored or translated into the skill during this repair.
The explicit DT conversion/comparison shell example is original code written to satisfy the local failure-reporting
requirement; `dtx_diff` was inspected to determine why empty output was not a sufficient verification condition.

No new guidance was taken from the local LKMC, Linux Lab, or Mastering Embedded Linux Programming collections in this
repair. Their separate Buildroot survey is not an attribution source for this package's new content.

## Debugging Reference Moved Out, 2026-09-30

`references/debugging.md` moved to the `embedded-linux-debugging` skill as `references/tracing-and-profiling.md`, with
its kgdb, oops, crash-dump, and gdbserver sections folded into that skill's other references. The Bootlin debugging
slides entry above, and any retained heyu-233 profiling influence, describe material that now lives there; that skill's
`ATTRIBUTIONS.md` repeats the relationship. The entries stay here because this package's earlier revisions carried the
material.
