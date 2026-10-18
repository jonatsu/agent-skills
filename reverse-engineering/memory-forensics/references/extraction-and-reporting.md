# Extraction and Reporting

## Bound the Extraction

Select the process, mapping, file object, module, or registry artifact needed to answer the question. Confirm the\
installed plugin's output options, destination behavior, required permissions, and overwrite policy. Write to a new\
analysis directory; preserve the original capture and existing outputs.

Record capture hash, process identity, object address, virtual range, physical/file mapping where available,\
plugin/version, options, and output hash. Preserve a manifest linking every artifact to its source. Mark missing,\
zero-filled, reconstructed, or unavailable pages explicitly.

A memory-mapped executable differs from its disk representation: relocations, resolved imports, mutable sections,\
initialization, and missing pages matter. State whether an output is a region dump, reconstructed executable, partial\
cached file, or complete recovered object. A familiar extension does not make it runnable or complete.

## Recover Only Relevant Sensitive Material

Memory can contain credentials, session secrets, personal documents, and unrelated private data. Limit extraction to\
the requested investigation. Recover credentials only when that is part of the authorized task; an image containing\
them does not make them necessary output. Keep values out of public examples and general reports.

For decoded configuration or key material needed to explain behavior, preserve private source references and report the\
role without revealing unnecessary values. Use reserved example values in shareable documentation.

## Prepare for Later Reverse Engineering

Provide architecture, address width, load map, entry/context evidence, backing module relationship, and known\
initialization dependencies with an extracted code artifact. Keep original and rebased addresses distinct. Disassemble\
statically first. Running extracted code requires a separate controlled runtime and scope; a dump cannot be assumed\
safe or self-contained because extraction succeeded.

Validate representative extracted ranges against the source layer. Reopen saved manifests and derived outputs to check\
persistence and mapping. A hash proves output identity, not that reconstruction semantics are correct.

## Report Evidence and Coverage

A useful finding includes the question, observed object/region, evidence locations, interpretation, alternatives,\
corroboration, and confidence. Pair each conclusion with acquisition and symbol limits that affect it. Separate plugin\
success, zero results, errors, and unperformed checks.

Deliver a concise finding narrative plus a reproducibility manifest: capture provenance, tool/plugin and symbol\
versions, commands/settings, extraction records, hashes, missing pages, and unresolved inputs. Do not claim the whole\
system was clean because selected plugins returned no candidates. Completion is bounded by the question and evidence\
available in that capture.
