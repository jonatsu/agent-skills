# Attributions

## Current skill

- Skill: `kas-dev`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original synthesis distilled from the upstream kas documentation, with
  one adapted source acknowledged below

This skill is an original synthesis authored for this repository. The method,
workflow, Iron Law, confirmation gates, and routing are new writing. The command
and configuration reference (`references/kas-tool.md`) is distilled from the
upstream kas project's own documentation; no prose was carried over verbatim, and
the content was rewritten and reorganized in original words.

## Adapted from (MIT — mandatory attribution)

- Original author: Siemens AG and kas contributors
- Upstream project: <https://github.com/siemens/kas>
- Upstream documentation: <https://kas.readthedocs.io/>
- Source material: the kas command, configuration-schema, lockfile, and
  `kas-container` documentation
- Source commit: not pinned (tracked against the current release line; commands
  and `header.version` semantics are version-gated — see the SKILL.md "Version
  awareness" section)
- Upstream license: MIT

The kas reference material informed and seeded `references/kas-tool.md`, which has
since been distilled, reorganized, and materially rewritten (the Contents table,
the dedicated `kas dump` section, and the safety framing are original to this
skill). MIT permits this reuse and modification; this notice preserves the
required attribution.

## Upstream license

The upstream kas project is licensed under the MIT License. MIT requires that its
copyright notice and permission notice be preserved in copies and substantial
portions. The upstream notice is reproduced here to satisfy that requirement:

```
MIT License

Copyright (c) Siemens AG, 2017-2024

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

### Note on the upstream license

The port brief described the kas documentation as Apache-2.0 and asked for an
Apache-2.0 NOTICE to be preserved. Primary-source verification of the upstream
repository shows kas is in fact **MIT-licensed**: `siemens/kas/LICENSE` is the MIT
License ("Copyright (c) Siemens AG"), the source headers declare
`__license__ = 'MIT'`, and the repository contains no `NOTICE` file and no
Apache-2.0 material. This file therefore preserves the applicable MIT notice
instead of an Apache-2.0 NOTICE.
