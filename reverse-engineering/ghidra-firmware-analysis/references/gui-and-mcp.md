# GUI and MCP operation

## Select and verify the interface

Discover an already configured Ghidra server through the client's tool catalog before proposing installation. Confirm\
extension, bridge, Ghidra, Java, and Python compatibility from their supplied versions and documentation. The preferred\
integration is [LaurieWired/GhidraMCP][laurie]. Another supplied integration can be used after inspecting its\
capabilities; tool names and mutation semantics are not interchangeable across projects or releases. If no bridge\
exists, describe the required extension and client configuration and use an available script/GUI route. Configuring or\
connecting a new service requires the user's applicable authority; existing authorization persists.

For the GUI route, open the intended program in CodeBrowser and enable the compatible GhidraMCP extension. GhidraMCP\
runs as the `ghidra-mcp` command. In GUI mode it connects to the plugin's HTTP server, set with `--ghidra-server`; in\
headless mode it imports and analyses one binary itself through PyGhidra. Probe a plugin with `GET /health`, which\
reports the GhidraMCP and Ghidra versions, the mode, and the open program, and check the program identity before\
querying sample data. The plugin has no authentication, so keep it on loopback unless remote access is explicitly\
required and configured with appropriate protection. Headless mode keeps edits only when started with `--project DIR`.\
For a stdio server, keep protocol stdout separate from logs. The server needs its declared Python dependencies;\
PyGhidra is required only by routes that embed Ghidra through Python. Use installation guidance from the selected\
release rather than blindly installing an unpinned default branch.

## Query narrowly

Read the advertised schema and use program information to establish the active binary, language, and image base.\
Correlate program identity with the saved input hash and project inventory; a program name alone is insufficient.\
Prefer address-based function selection when names collide. Paginate enumeration and retrieve focused instructions,\
references, and decompilation before exporting an entire program.

At upstream revision `1e980252087b2479a21b9ca6d82d5829538651a7`, the server declares program information, function\
lookup/decompilation, disassembly, references, memory reads, renaming, comments, prototypes, and local types. This is a\
documented capability reference, not proof that an installed server exposes all those operations. Discover the live\
schema and inspect returned errors, addresses, and truncation. Archive construction or FunctionID operations may\
require GUI services or scripts even when queries work through MCP.

## Mutate with evidence and recover

Before the first mutation, preserve analysis and record the old declaration/name/type at every affected address.\
Validate proposed names, prototypes, structure layouts, and target identity before applying them. Avoid concurrent GUI\
edits to the same function while an agent applies metadata. A connection error after a mutation leaves completion\
uncertain: read back the address's state before retrying. If the expected change exists, continue validation; if state\
differs, resolve the conflict before overwriting it. Read back each accepted change and redecompile affected callers.\
Return values alone do not establish persistence.

An MCP edit tool can apply only types the program already holds, and the local-variable tool reaches only decompiler\
locals. Bring a missing structure into the program from its archive first, then retype. A global is listing data, which\
the local-variable tool cannot reach; retype it in the listing or with a script. When an edit is not possible over MCP,\
leave the variable unchanged and queue the edit for a script; a placeholder byte array in place of a known structure\
hides the layout and must be undone later.

Use the integration's supported save path or the GUI's save action; verify reopening after closing the session. Do not\
assume successful HTTP mutation saved the underlying project to disk. Headless server modes may use temporary projects\
or conditional save defaults: inspect flags and project selection before relying on persistence. Preserve a consistent\
copy before switching between GUI and headless access. Never defeat a project lock to open a second writer.

## Upstream reference

[laurie]: https://github.com/LaurieWired/GhidraMCP/tree/1e980252087b2479a21b9ca6d82d5829538651a7
