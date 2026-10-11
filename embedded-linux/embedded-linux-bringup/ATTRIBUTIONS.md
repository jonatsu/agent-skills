# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts material from linux-embedded-dev, whose MIT license requires its notice to travel with the
material; keep `LICENSE.upstream` with the skill.

## First-party Sources

### The Linux kernel developers — i.MX thermal binding

- Source: <https://github.com/torvalds/linux>, `Documentation/devicetree/bindings/thermal/imx-thermal.yaml`
- License: `GPL-2.0-only OR BSD-2-Clause`
- Version: `v6.12`

Supplied the idea of named calibration cells read from eFuse providers, which `references/device-tree-driver-bringup.md`
cites as one example. Formerly an example device-tree fragment in that reference drew on the binding; the current skill
links to the binding and carries no code from it.

## Third-party Sources

### heyu-233 — linux-embedded-dev

- Source: <https://github.com/heyu-233/linux-embedded-dev>, `references/camera-v4l2-workflow.md` and
  `references/full-link-debug-pipeline.md`
- License: `MIT`
- Version: `53e7526e3ba3ffe4018845a58af328f897ffd60a`

The camera workflow was the starting base for `references/camera-v4l2.md`, which reorganizes it and adds media graph,
capture, and diagnostic detail. The full-link pipeline supplied the case of two host network interfaces on the board's
subnet with a successful ping and a stalled SSH session, kept as a hypothesis to verify. Formerly adapted: earlier
revisions also followed the perf tuning checklist and the profiling playbook; that material now lives in the
`embedded-linux-debugging` skill.

### Bootlin — Embedded Linux system development training

- Source: <https://bootlin.com/doc/training/embedded-linux/embedded-linux-slides.pdf>
- License: `CC-BY-SA-3.0`
- Version: slides updated 2026-06-09

Shaped the selection of cross-compilation topics: C library and static-linking choices, inspecting target dependencies,
cross-host selection, and prefix and staging. The skill expresses them through target ABI and build-interface diagnosis
and copies no slide prose, sequence, lab, or code.

### Bootlin — Linux debugging, profiling and tracing training

- Source: <https://bootlin.com/doc/training/debugging/debugging-slides.pdf>
- License: `CC-BY-SA-3.0`
- Version: slides updated 2026-06-09

Formerly shaped earlier revisions of the perf probe selection and flame graph guidance. The current skill carries none
of it, and that guidance now lives in the `embedded-linux-debugging` skill.
