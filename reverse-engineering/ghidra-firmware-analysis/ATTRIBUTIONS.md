# Attributions

- Author: Joonas Onatsu
- License: `MIT`

Keep `LICENSE.symbol-recovery` with the adapted symbol and structure recovery material.

## First-party Sources

### National Security Agency: Ghidra documentation

- Source: <https://github.com/NationalSecurityAgency/ghidra>, headless analysis, scripting, FunctionID (including\
  `building_fid.txt`), C-parser and data types, the GhidraClass advanced course on improving disassembly and\
  decompilation, the API Javadoc, the bundled scripts, and the PyGhidra package source
- License: `Apache-2.0`
- Version: Ghidra 12.0 PyGhidra guide, 12.1.4 headless/PyGhidra guides, help, course, and API Javadoc, the\
  `Ghidra_12.2_build` source tree, and PyGhidra 3.1.0

The documentation grounds installation discovery, script providers, saved-program processing, and metadata operations.\
The API Javadoc and the framework classes ground the scripting recipes' signatures and the project path and owner\
checks. The PyGhidra source grounds the `pyghidra` command's exit status, project layout, and save behaviour. The\
advanced course and the FunctionID help supplied the decompiler-repair techniques and the FunctionID donor and\
false-positive guidance; the 12.2 source confirmed the script, API, and reference-type names. Guidance is independently\
expressed; no implementation or documentation prose is copied.

## Third-party Sources

### LaurieWired: GhidraMCP

- Source: <https://github.com/LaurieWired/GhidraMCP>, README, `src/ghidra_mcp`, and the extension's\
  `GhidraAnalysisService.java` and `BackendHttpServer.java`
- License: `Apache-2.0`
- Version: GhidraMCP 2.0, `1e980252087b2479a21b9ca6d82d5829538651a7`

The integration documentation and source informed GUI/MCP capability discovery, optional Python execution, mutation\
verification, and persistence checks. They also supplied the `ghidra-mcp` GUI and headless modes, the `/health` probe,\
and the limits of the edit tools: type names resolve only in the program's own data type manager, and the\
local-variable tool reaches only decompiler locals. No code or prose is copied.

### mitsuhiko: agent-stuff Ghidra skill

- Source: <https://github.com/mitsuhiko/agent-stuff>, `skills/ghidra`
- License: `Apache-2.0`
- Version: historical consultation revision and date not recorded

The source informed Java GhidraScript export and the headless invocation pattern. The bundled exporter is independently\
implemented; no upstream code is adapted.

### akiselev: ghidra-cli skill

- Source: <https://github.com/akiselev/ghidra-cli>, `.claude/skills/ghidra-cli`
- License: `GPL-3.0`
- Version: historical consultation revision and date not recorded

The source influenced the description's capability and trigger structure. No prose or code is copied.

### Und3rf10w: ai-ghidra-tools

- Source: <https://github.com/Und3rf10w/ai-ghidra-tools>, `plugins/ghidra`
- License: `LicenseRef-No-License-Declared`
- Version: historical consultation revision and date not recorded

No redistribution license was declared for the consulted material, so its expression was not copied. It informed the\
idea of querying existing analyzed programs rather than importing again.

### r00tedbrain-backup: symbol and structure recovery references

- Source: <https://github.com/r00tedbrain-backup/skills/tree/365240cc0f35>, reverse-engineering references
- License: `MIT`
- Version: `365240cc0f35`

The recovery reference adapts the source's symbol and structure inference approach to Ghidra notation and ABI-qualified\
examples. The upstream notice is preserved in `LICENSE.symbol-recovery`.
