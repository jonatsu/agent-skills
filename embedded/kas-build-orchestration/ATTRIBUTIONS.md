# Attributions

## Current skill

- Skill: `kas-build-orchestration`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original synthesis distilled from the upstream kas documentation, with one adapted source acknowledged below

This skill combines independently written orchestration guidance with a command/configuration reference distilled and
adapted from upstream kas documentation. The 2026-09-07 repairs also use upstream implementation to explain mutation,
merging, locking, cleanup, credentials, and container behavior. Rewriting the expression does not remove that influence.

## Adapted from (MIT — mandatory attribution)

- Original author: Siemens AG and kas contributors
- Upstream project: <https://github.com/siemens/kas>
- Upstream documentation: <https://kas.readthedocs.io/>
- Source material: the kas command, configuration-schema, lockfile, and `kas-container` documentation
- Historical source revision: not recorded by the original adaptation; it remains unknown.
- Verified repair baseline: [kas tag 5.3](https://github.com/siemens/kas/tree/5.3), checked 2026-09-07.
  This identifies the repair source, not an invented pin for the original adaptation.
- Upstream license: MIT

The kas reference material informed and seeded `references/kas-tool.md`, which has since been distilled, reorganized,
and materially rewritten (the Contents table, the dedicated `kas dump` section, and the safety framing are original to
this skill). MIT permits this reuse and modification; this notice preserves the required attribution.

### Repair Source Influence

The 5.3 sources below influenced both `SKILL.md` and `references/kas-tool.md`. Explanations and replacement examples
are independently expressed; the existing adaptation relationship and notice remain. No upstream executable is bundled.

- `docs/userguide/project-configuration.rst`, `docs/format-changelog.rst`, `kas/includehandler.py`,
  `kas/config.py`, and `kas/schema-kas.json`: recursive composition, include path bases, lock discovery,
  selection overrides, format-version limits, local repository and layer semantics.
- `kas/plugins/{dump,checkout,lock,diff,menu,clean}.py`, `kas/libcmds.py`, and `kas/repos.py`: resolving side effects,
  dirty-checkout handling, lock creation versus refresh, external lock ownership, parser contracts, and deletion scope.
- `kas-container`, `container-entrypoint`, `docs/userguide/kas-container.rst`, and the credential documentation:
  wrapper/image distinctions, mount aliases and ownership, rootless restrictions, AWS cache exposure, and supported
  credential options.
- `kas/keyhandler.py`, `kas/repos.py`, and the signing schema: optional Git signature enforcement, dependencies,
  and the distinction between pins and publisher authentication.

The repair's command fixtures were written for this repository from those contracts, outside the deployed package.
Bootlin's local Yocto training PDF was consulted during review for context only; no material was adopted from it.
No third-party project wrapper supplied adopted guidance. The MIT license is unchanged.

## Upstream license

The upstream kas project is licensed under the MIT License. MIT requires that its copyright notice and permission notice
be preserved in copies and substantial portions. The upstream notice is preserved below and verbatim in
[LICENSE.upstream](LICENSE.upstream), copied from the verified 5.3 source:

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

The port brief described the kas documentation as Apache-2.0 and asked for an Apache-2.0 NOTICE to be preserved.
Primary-source verification of the upstream repository shows kas is in fact **MIT-licensed**: `siemens/kas/LICENSE` is
the MIT License ("Copyright (c) Siemens AG"), the source headers declare `__license__ = 'MIT'`, and the repository
contains no `NOTICE` file and no Apache-2.0 material. This file therefore preserves the applicable MIT notice instead of
an Apache-2.0 NOTICE.
