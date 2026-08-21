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
- Source path: camera / V4L2 bring-up material
- Source commit: not pinned
- Upstream license: MIT

The camera/V4L2 bring-up workflow (`references/camera-v4l2.md`) used this project as
a starting base. It has since been restructured and materially rewritten and
expanded — investigation-order layering, `media-ctl` graph wiring, `v4l2-compliance`
validation, `yavta` low-level capture, the failure-bucket table, and the buffer
lifecycle are original to this skill. MIT permits this reuse and modification; this
notice preserves the required attribution.

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

## Upstream license

- The `heyu-233/linux-embedded-dev` starting base is used under MIT. MIT requires
  that its copyright and permission notice be preserved; this file provides that
  attribution.
- Bootlin training materials are published under CC BY-SA. They are acknowledged
  here as a learning source; no CC BY-SA-licensed text is redistributed in this
  skill.
