# Attributions

External sources whose reading shaped this skill's content. No text or code was copied from any of them; the
influences below are adopted ideas, named per the repository's provenance policy. Ideas not listed — the genre
taxonomy with per-genre authority declarations, the named default layout (merged from the author's
`nix-config` and `agent-setup` conventions), read-when phrasing, verified-against stamps, and the search-surface
rule — were expressed independently, informed by the general framing below.

- **Van Clief & McDermott, "Interpretable Context Methodology: Folder Structure as Agent Architecture"
  (arXiv:2603.16021)** and its companion repository (RinDig/icm-architect): the walk test (name and core
  idea; this skill's protocol adds the metrics and failure-mode mapping), workspace-state-as-files framing,
  and routing files over orchestration code.
- **Anthropic, "Effective context engineering for AI agents" (anthropic.com/engineering)**: the attention
  budget and context-rot framing, just-in-time retrieval via lightweight identifiers, the
  smallest-set-of-high-signal-tokens heuristic, and compaction tuned for recall before precision.
- **muratcankoylan, "Agent Skills for Context Engineering" (GitHub)**: degradation-detect-and-restart as a
  designed loop, success-predicate task briefs, and treating the harness itself as an optimization target
  gated on evaluation.
- **OpenAI Cookbook, "Context personalization" (Agents SDK example)**: the memory lifecycle
  (distill/inject/trim/consolidate) with forgetting as a first-class stage, declared precedence between
  knowledge scopes, and injection hygiene (stored text read as data, not followed as instructions).
- **addyosmani/agent-skills, `documentation-and-adrs`** (Copyright (c) 2025 Addy Osmani, MIT), read 2026-09-09:
  auditing a repository for significant decisions that were never recorded, added to the Audit branch as a
  coverage question distinct from navigation. The upstream states it as two red flags; the branch wording,
  the decision classes, and the coverage-versus-navigation distinction are this skill's.
- **Matt Pocock, [“A Complete Guide To AGENTS.md”](https://www.aihero.dev/a-complete-guide-to-agents-md)**
  (updated 2026-01-18, read 2026-09-11): nested progressive disclosure and the correction from one direct
  floor entry per skill to a floor-reachable intermediate index. The guidance is independently expressed; no
  prose, examples, or assets were copied, and the page's license is not relied on.
- **IWE, [“Inclusion Links”](https://iwe.md/docs/concepts/inclusion-links/)** (read 2026-09-11): distinguishing
  standalone structural links from inline references, allowing a document to appear under multiple useful
  parents, and placing relationship context in the parent. The checker and guidance implement those ideas
  independently without IWE code, prose, examples, or assets; the page's license is not relied on.
- **Addy Osmani, [“How to write a good spec for AI agents”](https://addyosmani.com/blog/good-spec/)**
  (published 2026-01-13, read 2026-09-11): version-controlled specifications as durable intended-behavior
  context and modular retrieval for large specifications. The genre authority and lazy layout rules are
  independently expressed; no prose, examples, images, templates, code, or assets were copied, and the page's
  license is not relied on.
- **agentydragon/ducktape, skills `knowledge_hygiene` and `verify_docs`**
  ([repository](https://github.com/agentydragon/ducktape), revision
  `4ad338af25ea537dc7f817390b2e25c2a7a903f0`, AGPL-3.0, read 2026-09-30): the truth audit in
  `references/truth-audit.md`. Adopted ideas: a claim-to-owner map; verifying every checkable claim against its
  source; the problem classes for volatile mirrors, self-referential counts, misleading status, missing update
  paths, and knowledge to promote or retire; the "true in any repository using the tool" test; ranking by load
  frequency; the lettered action menu the user selects from; and the owner of a fact being the file touched
  when it changes. The AGPL-3.0 does not fit this MIT skill, so no text was copied or adapted; every sentence
  was written independently. The upstream's priority markers and code-comment sweep were not taken.
- **softaworks/agent-toolkit, `crafting-effective-readmes`** (MIT, Copyright (c) 2026 Leonardo Flores,
  revision `011baf4acea99174acb5486a9b662a7e084be63b`): the README accuracy check that `repo-management`
  adapted from it on 2026-08-25 moved into the truth audit on 2026-09-30. What carries over is its list of
  claims to check (commands, paths, capabilities and versions, links) and its rule to decide whether the
  document or the implementation is right before correcting either; `repo-management`'s `ATTRIBUTIONS.md` holds
  the original record.
