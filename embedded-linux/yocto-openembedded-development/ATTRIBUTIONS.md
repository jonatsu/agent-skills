# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Yocto Project — Yocto Project documentation

- Source: <https://docs.yoctoproject.org/>, the Reference, BitBake, BSP, Kernel, Security, and Development Tasks
  manuals, the migration guides, and "What I wish I'd known about Yocto Project"
- License: `CC-BY-SA-2.0-UK`
- Version: 5.0 (Scarthgap)

The BitBake syntax, task lifecycle, recipe anatomy, and compliance guidance is built on the manuals, and
`references/official-doc-map.md` routes to them by problem type. Facts are restated in original words; no prose
is copied.

### The Yocto Project — Poky, with OpenEmbedded-Core and BitBake

- Source: <https://git.yoctoproject.org/poky>, chiefly `meta/conf/bitbake.conf`, `meta/lib/oe/package.py`,
  `meta/classes-global/`, `meta-poky/conf/distro/`, and `bitbake/lib/bb/`
- License: `MIT AND GPL-2.0-only`
- Version: `yocto-5.0.12`

The configuration-file precedence, distro selection, sstate, packaging, and `installed-vs-shipped` guidance is
derived from the release's own classes, configuration, and BitBake code. No code is copied.

## Third-party Sources

### Alexandre Belloni, Bootlin — "OpenEmbedded and Yocto Project best practices"

- Source: <https://bootlin.com/pub/conferences/2020/elce/belloni-yocto-best-practices/>
- License: `CC-BY-SA-3.0`
- Version: Embedded Linux Conference Europe 2020, slides dated 2020-10-26

Formerly adapted: earlier revisions of `references/yocto-best-practices.md` followed this deck's selection and
order of topics, covering configuration scopes, distro policy, sstate sharing, release capture, and license
manifests. The current skill carries none of that structure.

### Prashant Divate — awesome-yocto-ai-agent-skills

- Source: <https://github.com/prashantdivate/awesome-yocto-ai-agent-skills>
- License: `MIT`
- Version: `0e268dcbee92c3433054be98617c1e9d0f682f40`

Showed four subjects this skill lacked: packaging and the `installed-vs-shipped` QA failure, `PACKAGECONFIG`, the
collection-versus-directory distinction in `LAYERDEPENDS`, and build output outside `tmp/`. No wording,
structure, examples, or command choices were taken.
