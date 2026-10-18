---
name: memory-forensics
description: Analyze RAM images and process dumps to recover processes, mappings, modules, network artifacts, and suspicious code. Use when investigating memory captures, corroborating injection or hidden-process indicators, planning acquisition, or extracting mapped artifacts for reverse engineering.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Memory Forensics

Recover artifacts from a capture and correlate them into qualified findings. An unusual object is an indicator; its\
interpretation depends on capture quality, symbol correctness, and independent context.

## Establish the Capture and Question

Record the requested finding, source system/platform if known, capture format, acquisition context, hash, supplied\
metadata, and analysis scope. Preserve the original; write outputs to a separate chosen directory. A process dump, full\
physical capture, crash dump, and VM snapshot expose different evidence. Do not apply a full-system plugin workflow\
blindly to a process-only dump.

Read [acquisition and input verification](references/acquisition-and-input.md) before planning a new capture or\
interpreting completeness. Acquisition changes live state and can require privileges or disrupt a VM. A supplied image\
authorizes analysis, not a new live capture or loading an acquisition driver.

Discover the selected Volatility 3 or alternative analyzer, version, plugin inventory, supported formats, and runtime\
dependencies. Read [platform and symbol setup](references/platform-and-symbols.md) before process analysis. Confirm the\
selected image's translation layers and symbols before interpreting object fields.

Check only needed dependencies. Recommend verified host-appropriate packages, matching symbols, or configuration with\
their purpose. Do not assume sudo, install software silently, or permit unexpected symbol downloads. Continue format\
and byte-level inspection when higher-level analysis is blocked.

## Analyze Through Correlated Views

1. Establish image/platform identity and usable layers/symbols. Preserve diagnostics and stop semantic object\
   interpretation when the prerequisite evidence is unreliable.
2. Survey processes, process trees, modules, mappings, and available network artifacts. Record identities and times,\
   not only PIDs, which can be reused.
3. Read [artifact interpretation](references/artifact-interpretation.md) to investigate discrepant process views,\
   executable private memory, module inconsistencies, persistence leads, or suspicious network context.
4. Corroborate a finding using independent views and, where supplied, disk/network/log evidence. Account for terminated\
   objects, acquisition smear, missing pages, symbols, and legitimate runtime behavior.
5. Read [extraction and reporting](references/extraction-and-reporting.md) before dumping regions or recovering files.\
   Preserve mappings, provenance, holes, and sensitive-data boundaries.

## Finish with Reproducible Findings

Report capture identity, platform/symbol basis, commands/plugins and versions used, relevant objects and addresses,\
supporting and contradictory evidence, extracted artifacts, and limitations. Separate confirmed behavior from\
indicators and unavailable evidence. An empty plugin result is not proof that an artifact never existed.

Completion means the requested question has an evidence-backed answer or a precise missing-input explanation, with\
outputs traceable to the capture. Runtime analysis of extracted code is a separate controlled operation.
