# Attributions

- Author: Joonas Onatsu
- License: `MIT`

Keep `LICENSE.upstream` with this adaptation.

## First-party Sources

### angr contributors: angr documentation

- Source: <https://docs.angr.io/en/latest/>, states, gotchas, and state options
- License: `BSD-2-Clause`
- Version: read 2026-10-18

The documentation grounds state selection, environment modeling, and exploration limitations. The guidance is\
independently expressed; no documentation prose or code is copied.

### Jonathan Salwan and Triton contributors: Triton

- Source: <https://github.com/JonathanSalwan/Triton>, README and Python API documentation
- License: `Apache-2.0`
- Version: read 2026-10-18

The library's documented capabilities informed the bounded instruction-analysis branch and dependency distinction. No\
implementation or example code is copied.

## Third-party Sources

### VillanCh: hack-skills symbolic execution tools

- Source: <https://github.com/yaklang/hack-skills>, `skills/symbolic-execution-tools`
- License: `MIT`
- Version: `6fbf0bc8d5c71830d62543a308d8744606c43d7c`

The skill adapts targeted exploration, input-boundary selection, and model-summary workflow ideas from the source.\
Examples and correctness constraints are independently expressed; the upstream notice is in `LICENSE.upstream`.
