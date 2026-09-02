# Attributions

## Current skill

- Skill: `embedded-linux-dev`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original synthesis, with one adapted-base component and one learning
  source acknowledged below

This skill is an original synthesis authored for this repository. The bulk of the
method, workflow, and reference material is new writing. Two upstream sources are
recorded for courtesy and completeness: one MIT-licensed skill that served as a
starting base for the camera/V4L2 workflow (mandatory attribution), and one
CC BY-SA learning source that informed some content (courtesy attribution). No
prose was carried over verbatim; content traceable to the CC BY-SA source was
rewritten in original words, and source-attributing framing was removed.

## Adapted from (MIT — mandatory attribution)

- Original author: heyu-233
- Upstream project: <https://github.com/heyu-233/linux-embedded-dev>
- Source path: camera / V4L2 bring-up material; on re-review also the capture
  performance material and one host-networking trap (see below)
- Upstream license: MIT, Copyright (c) 2026 heyu-233 — read from the repository's
  `LICENSE` file on 2026-08-25
- Source commit: `53e7526e3ba3ffe4018845a58af328f897ffd60a`, resolved 2026-08-25.
  **This is the commit the re-review read, NOT the one the first adoption used** —
  that one was never recorded and cannot be recovered. Upstream last pushed
  2026-05-04, so the two are likely the same tree; likely is not verified.

The camera/V4L2 bring-up workflow (`references/camera-v4l2.md`) used this project as
a starting base. It has since been restructured and materially rewritten and
expanded — investigation-order layering, `media-ctl` graph wiring, `v4l2-compliance`
validation, `yavta` low-level capture, the failure-bucket table, and the buffer
lifecycle are original to this skill. MIT permits this reuse and modification; the
notice reproduced at the end of this file preserves the required attribution.

## Informed by (CC BY-SA — learning source, courtesy)

- Source: Bootlin embedded Linux and debugging training materials
- Upstream project: <https://bootlin.com/training/> (materials published under
  Creative Commons BY-SA)
- Upstream license: CC BY-SA

Bootlin's freely published training materials informed the general shape of some
cross-compilation and kernel-debugging content. Any text that tracked a CC BY-SA
source in fact selection or sequencing was rewritten in original words for this
skill, and framing that attributed statements to the source was removed. This entry
is a courtesy acknowledgement of the learning source; the skill itself ships under
MIT as original work.

## Re-review, 2026-08-25

The upstream was read again in full to check what the first adoption left behind.
Two things had been, both taken:

- **Capture performance triage**, now a section of `references/camera-v4l2.md`. The
  bisection between a minimal `v4l2-ctl`/`yavta` capture and the application, the
  seven-step tuning order, the honest verdict on edge-triggered `epoll`, and the
  profile-interpretation list come from upstream's `perf-tuning-checklist.md` and
  `profiling-playbook.md`. This file previously stopped at the buffer lifecycle and
  blocking-vs-poll, so it named the tools and none of the interpretation. Restated
  in this skill's own words and table form; no prose was carried over.
- **The multi-NIC SSH trap** in `references/cross-compilation.md`: two host
  interfaces in the board's subnet, where `ping` succeeds while every TCP connection
  stalls, fixed with `BindAddress` in the SSH config. From upstream's
  `full-link-debug-pipeline.md`. Recorded because a successful ping sends the
  investigation one layer too high.

Declined, and recorded so the same ground is not re-reviewed a third time:

- **The teaching-mode / efficiency-mode duality**, its fixed per-turn response
  template (Mode, Current goal, Principle in brief, Do this now, Send back, Check
  your understanding), the question-back rules and the stage-summary rule. That is a
  tutoring product; this skill is a debugging partner whose Iron Law is
  classify-the-boundary-then-prove-it, and a comprehension-check turn would compete
  with the Output contract rather than extend it.
- **`debugctl`**, upstream's SSH/SCP evidence-collection CLI with a target YAML
  schema. Building a board-connection tool is a project, not a skill adoption, and
  the evidence-bundle discipline it encodes is already this skill's *Evidence First*
  and the deploy-verify script in `references/deploy-and-iterate.md`.
- **`common-bus-debugging.md`** — five generic bullets per bus, against the per-bus
  sections of `references/device-tree-driver-bringup.md`.
- The learning roadmap, repo reading list, project-note and board-case-template
  files, which are curriculum rather than method, and a Windows-specific note about
  writing non-ASCII project notes through PowerShell here-strings.

Upstream ships **no confirmation gate of any kind** — nothing on flash writes,
`devmem` pokes or boot-config edits. Nothing to take, and it is the reason the first
adoption stayed narrow.

## Upstream license

The `heyu-233/linux-embedded-dev` starting base is used under the MIT license,
reproduced here in full as that license requires:

```text
MIT License

Copyright (c) 2026 heyu-233

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Until 2026-08-25 this section asserted that the file "provides that attribution"
while reproducing neither the copyright line nor the permission notice. Recorded
rather than silently corrected, because the defect was a claim of compliance, not an
omission.

Bootlin training materials are published under CC BY-SA. They are acknowledged here
as a learning source; no CC BY-SA-licensed text is redistributed in this skill.
