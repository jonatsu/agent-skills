# Platform and Symbol Setup

## Discover the Installed Analyzer

Resolve the actual executable or Python entry point, inspect its version and help, and list supported plugins.\
Volatility 3 plugin namespaces and options evolve. Resolve an advertised short name to the installed plugin and read\
that plugin's help before constructing PID, dump, symbol, renderer, or output options.

A common installed CLI is `vol`, but some environments expose another entry point. Read the version from its help\
banner or installed distribution metadata; do not assume a `--version` option. Before opening an image, inspect\
automatic symbol retrieval and caches. Use an offline symbol set unless the needed network retrieval is already\
authorized. Confirm that the installed CLI advertises `--offline`. For that CLI, inspect help and perform a\
Windows-image check without automatic retrieval:

```bash
vol --help
vol --offline -f memory.raw windows.info
```

The last command applies to a Windows image with the corresponding installed plugin; it is not an OS detector for every\
input. If matching symbols are unavailable offline, preserve the missing-symbol diagnostic and supply an approved\
symbol set or arrange an authorized retrieval before retrying. Preserve complete errors. Missing translation-layer\
requirements and missing symbol requirements have different causes; repeating a process plugin cannot fix either\
prerequisite.

## Match Symbols to the Captured System

For Windows, establish the correct kernel/module identity and matching PDB-derived symbols. Inspect the analyzer's\
automatic symbol behavior and cache. Symbol retrieval can access external servers; arrange an authorized download or an\
offline symbol set when network access is unavailable or out of scope.

For Linux, recover the kernel banner/build identity and obtain matching kernel debug information. Prebuilt symbol\
tables may exist; otherwise compatible DWARF input and a symbol-generation tool such as `dwarf2json` may be needed. A\
similar distribution or version string does not guarantee compatible layouts. Verify the full relevant build.

For macOS, establish the supported target version/architecture and matching symbol data before selecting plugins. Do\
not infer modern platform support from an old command example. Stop and name the unsupported combination where no\
validated reader/symbol path exists.

The Volatility Foundation's [symbol-table guide](https://volatility3.readthedocs.io/en/stable/symbol-tables.html)\
explains symbol generation and discovery; its\
[Linux tutorial](https://volatility3.readthedocs.io/en/stable/getting-started-linux-tutorial.html) covers kernel\
identity and matching symbol requirements. Read documentation matching the installed release when resolving an error.

## Confirm Usable Interpretation

Inspect reported platform, architecture, layer layout, kernel identity, representative process names, addresses, and\
timestamps. Agreement across several coherent objects supports the setup; one plausible string does not. Implausible\
pointers, widespread impossible times, or repeatable field errors can indicate incorrect symbols, incomplete memory, an\
unsupported build, or corrupted data.

Record symbol source/version or kernel build, tool version, settings, cache or offline path, and diagnostics. A\
hand-constructed structure declaration from another build is not a substitute for matched symbols.

## Branch by Available Evidence

For a process-only dump, use a compatible process-dump reader, debugger, or static mapping workflow instead of\
promising system-wide process lists. For an unsupported physical image, preserve format and range facts while reporting\
the higher-level analysis blocker. Raw strings and byte signatures remain leads without process or virtual-address\
attribution; keep that limit with each result.
