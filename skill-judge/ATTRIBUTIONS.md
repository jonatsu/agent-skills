# Attributions

## Current skill

- Skill: `skill-judge`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially trimmed

## Original author and source

- Upstream project:
  [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit),
  skill `skill-judge`.
- Upstream license: MIT.

## Adaptation note

Kept the evaluation instrument: the eight scored dimensions (D1–D8), the
120-point total and grade scale, the Expert/Activation/Redundant knowledge-ratio
scan, the evaluation protocol, the report template, and the failure-pattern
catalog.

Material changes from the upstream skill:

- Cut the ~40-line philosophy preamble ("what is a Skill", training-cost tables,
  hot-swappable-LoRA analogy) — it restates concepts this repo's
  `writing-great-skills` already owns. Replaced with a two-line intent plus
  cross-references, so those concepts have a single source of truth.
- Removed the ASCII-art boxes (activation-flow diagram, quick-check panel),
  folding their content into tables and prose.
- Neutralized provider-specific framing ("Claude" → "the agent/model") so the
  skill is agent-agnostic.
- Mapped the failure patterns onto `writing-great-skills` vocabulary (no-op,
  sprawl, duplication) instead of re-explaining them.
- Rewrote frontmatter to this repo's conventions (`metadata.author` /
  `metadata.license`) and added an Iron Law.

## Upstream license (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
