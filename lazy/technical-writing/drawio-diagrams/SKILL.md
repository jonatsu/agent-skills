---
name: drawio-diagrams
description: Create, edit, and export draw.io (diagrams.net) diagrams as .drawio files or editable .drawio.svg and .drawio.png images. Use when a request names draw.io or diagrams.net, a file has one of those extensions, or a diagram must stay editable in draw.io; not for Mermaid kept in Markdown (mermaid-diagrams).
license: MIT
compatibility: Python 3 for the bundled checker. Mermaid conversion, auto-layout, and image export need the draw.io desktop app's command-line interface.
metadata:
  author: Joonas Onatsu
---

# draw.io Diagrams

A draw.io diagram is XML: an `mxfile` holding one `diagram` per page, each with an `mxGraphModel` of cells. You write
that XML, or have the draw.io command-line interface (CLI) convert Mermaid into it, then check it and export it.

Current known: draw.io desktop 31.5.3, checked 2026-09-29. `drawio --version` and `drawio --help` confirm what the
installed build supports; the help text is the flag reference.

`<skill-dir>` in a command means this skill's directory.

## 1. Settle the Deliverable

- **`.drawio`**: the editable source, plain XML that diffs cleanly. The default.
- **`.drawio.svg`**: an SVG image with the diagram embedded, so it renders in Markdown on GitHub and in docs and
  still reopens in draw.io. Prefer it whenever the diagram is shown inside a document.
- **`.drawio.png`**: the same idea as a PNG. Choose it only when the target cannot show SVG.

When editing an existing file, keep its format and its name unless the user asks for a change.

## 2. Find the CLI

Run `command -v drawio`. On WSL2 without a Linux install, the Windows app at `/mnt/c/Program Files/draw.io/draw.io.exe`
is the fallback. It accepts paths relative to the current directory; convert an absolute path with `wslpath -w`.

The CLI is an Electron app, and two things decide whether a call finishes:

- **Give it a display.** On a headless Linux machine, run it as `xvfb-run -a drawio ...`. WSLg already provides one.
- **Pass `--disable-gpu` and wrap the call in `timeout 120`.** Under WSLg and in virtual machines the GPU process
  crashes, and an image export then hangs forever instead of failing. Stderr fills with GPU, Vulkan, and driver-path
  lines; they are noise. Success is the `input -> output` line and the output file.

The CLI silently ignores an unknown flag, so a misspelled option does nothing rather than failing. Check the flag
against `drawio --help` when an option seems to have no effect.

Without the CLI, author the XML by hand, check it, and deliver the `.drawio` file. Tell the user that Mermaid
conversion, auto-layout, and image export need the draw.io desktop app.

## 3. Author the Diagram

**Mermaid route**, when the CLI is available and Mermaid can express the diagram (flowchart, sequence, class, state,
entity-relationship): write the Mermaid to `name.mmd`, then convert it. The converter lays the diagram out, which is
more reliable than placing cells by hand.

```bash
timeout 120 drawio --disable-gpu -x -f xml -o name.drawio name.mmd
```

The `.drawio` is the artifact; delete the `.mmd` once the conversion succeeds. Restyle the result by editing its XML.

**XML route** for everything else: architecture with nested containers, custom shapes, exact placement, or no CLI.
Read [references/xml-format.md](references/xml-format.md) before writing the first cell. With the CLI available, give
cells rough positions and let a layout place them, repairing common structural faults on the way:

```bash
timeout 120 drawio --disable-gpu -x -f xml --normalize --layout verticalFlow -o name.drawio name.drawio
```

The presets are `verticalFlow`, `horizontalFlow`, `verticalTree`, `horizontalTree`, `radialTree`, and `organic`. By
hand, keep to a grid: shapes about 120 by 60, 40 to 60 pixels apart side by side and 80 to 120 between rows. Keep
labels short, and give color a meaning, such as one fill per tier, rather than decoration.

## 4. Edit an Existing Diagram

Extract it to plain XML first. A page saved compressed holds Base64 text instead of readable cells, and an image
hides the diagram inside its metadata:

```bash
python3 <skill-dir>/scripts/drawio_check.py extract diagram.drawio.svg -o work.drawio
```

Edit `work.drawio`. Keep every existing cell id, because edges and layers refer to cells by id. A cell inside a
container stays positioned relative to that container. Then write the result back in the original format: export
with `-e` for an image (step 6), or copy the plain XML over a `.drawio` file.

## 5. Check the Diagram

```bash
python3 <skill-dir>/scripts/drawio_check.py check name.drawio
```

It reports missing root cells, duplicate ids, dangling parents and edge endpoints, and vertices or edges without
geometry, then exits 1. Fix every reported defect and run it again until it exits 0. It reads every format in step 1.

The checker proves structure, not appearance. With the CLI, export a PNG and look at it before delivering:
overlapping shapes, clipped labels, and edges crossing through shapes show only in the picture.

```bash
timeout 120 drawio --disable-gpu -x -f png -b 10 -o /tmp/preview.png name.drawio
```

The step is done when the checker exits 0 and, where the CLI exists, the preview shows every label whole and no
shape overlapping another.

## 6. Export

Pass `-e` so the image carries the diagram and stays editable:

```bash
timeout 120 drawio --disable-gpu -x -f svg -e -o name.drawio.svg name.drawio
timeout 120 drawio --disable-gpu -x -f png -e -b 10 -o name.drawio.png name.drawio
```

`-p` picks a page, counting from 1; without it an image export takes the first page. Keep the `.drawio` source
beside an exported image unless the user wants the image alone: image optimizers and some upload paths strip the
embedded diagram, and the source is then the only editable copy. Run the checker on the exported file to confirm
the diagram is inside it.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the draw.io skills whose ideas informed this one.
