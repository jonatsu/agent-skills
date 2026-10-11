# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## Third-party Sources

### Jake Van Clief and David McDermott — Interpretable Context Methodology

- Source: <https://arxiv.org/abs/2603.16021> ("Folder Structure as Agentic Architecture") and its companion
  repository <https://github.com/RinDig/icm-architect>
- License: `CC-BY-4.0 AND MIT`
- Version: arXiv:2603.16021, submitted 2026-03-17

The sources supplied the walk test (this skill adds
the metrics and the failure-mode mapping), the framing of workspace state as files, and routing files over
orchestration code. Nothing was copied.

### Anthropic — Effective context engineering for AI agents

- Source: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- License: `LicenseRef-Proprietary`
- Version: published 2025-09-29

Nothing was copied due to the license. It supplied the attention-budget and context-rot framing,
just-in-time retrieval through lightweight identifiers, the smallest-set-of-high-signal-tokens heuristic, and
compaction tuned for recall before precision.

### Agent Skills for Context Engineering Contributors — Agent Skills for Context Engineering

- Source: <https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering>
- License: `MIT`
- Version: read on or before 2026-09-06

The repository supplied degradation detection and restart as a designed loop, success-predicate task briefs, and
treating the harness itself as an optimization target gated on evaluation. Nothing was copied.

### OpenAI — Cookbook, "Context personalization"

- Source: <https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization>, repository
  <https://github.com/openai/openai-cookbook>, `examples/agents_sdk/context_personalization.ipynb`
- License: `MIT`
- Version: page dated 2026-01-05

The example supplied the memory lifecycle (distill, inject, trim, consolidate) with forgetting as a first-class
stage, declared precedence between knowledge scopes, and injection hygiene, which reads stored text as data rather
than as instructions. Nothing was copied.

### Addy Osmani — `documentation-and-adrs` skill

- Source: <https://github.com/addyosmani/agent-skills>, `skills/documentation-and-adrs/`
- License: `MIT`
- Version: read 2026-09-09

The skill suggested auditing a repository for significant decisions that were never recorded, which the Audit branch
asks as a coverage question. Nothing was copied.

### Matt Pocock — "A Complete Guide To AGENTS.md"

- Source: <https://www.aihero.dev/a-complete-guide-to-agents-md>
- License: `LicenseRef-Proprietary`
- Version: updated 2026-01-18

Nothing was copied due to the license. It supplied nested progressive
disclosure and the correction from one direct floor entry per skill to a floor-reachable intermediate index.

### IWE — "Inclusion Links"

- Source: <https://iwe.md/docs/concepts/inclusion-links/>, repository <https://github.com/iwe-org/iwe>,
  `docs/inclusion-links.md`
- License: `Apache-2.0`
- Version: read 2026-09-11

The page supplied the distinction
between standalone structural links and inline references, the option of a document appearing under several useful
parents, and the placement of relationship context in the parent. Nothing was copied.

### Addy Osmani — "How to write a good spec for AI agents"

- Source: <https://addyosmani.com/blog/good-spec/>
- License: `LicenseRef-Proprietary`
- Version: published 2026-01-13

Nothing was copied due to the license. It supplied
version-controlled specifications as durable intended-behavior context and modular retrieval for large
specifications, which shaped the genre authority and lazy layout rules.

### agentydragon — `ducktape` skills `knowledge_hygiene` and `verify_docs`

- Source: <https://github.com/agentydragon/ducktape>, `skills/knowledge_hygiene/` and `skills/verify_docs/`
- License: `AGPL-3.0-only`
- Version: `4ad338af25ea537dc7f817390b2e25c2a7a903f0`

The truth audit in `references/truth-audit.md` adopts its claim-to-owner map, claim verification against sources,
problem classes for stale and misleading documentation, and ranking by load frequency. No text was copied or
adapted due to the license.

### Leonardo Flores — `crafting-effective-readmes` skill

- Source: <https://github.com/softaworks/agent-toolkit>, `skills/crafting-effective-readmes/`
- License: `MIT`
- Version: `011baf4acea99174acb5486a9b662a7e084be63b`

The truth audit carries over this skill's list of README claims to check (commands, paths, capabilities and
versions, links) and its rule to decide whether the document or the implementation is right before correcting
either.
