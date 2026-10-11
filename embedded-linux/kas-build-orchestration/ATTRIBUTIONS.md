# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts documentation from kas, whose MIT license requires its notice to travel with the material; the
notice appears below, and `LICENSE.upstream` stays with the skill.

## First-party Sources

### Siemens AG and kas contributors — kas

- Source: <https://github.com/siemens/kas>, documentation at <https://kas.readthedocs.io/en/5.3/>
- License: `MIT`
- Version: `5.3`

`references/kas-tool.md` was seeded from the kas command, configuration schema, lockfile, and `kas-container`
documentation, then reorganized and rewritten. The guidance in `SKILL.md` and that reference on composition, include
paths, locking, cleanup, credentials, and container behavior is built on the 5.3 sources, chiefly
`kas/includehandler.py`, `kas/config.py`, `kas/repos.py`, `kas/plugins/`, and `kas-container`. The skill adapts
documentation and bundles no upstream executable.

## Upstream License Notice

```text
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
