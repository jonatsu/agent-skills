# Attributions

External sources whose reading shaped this skill's content. No text or code was copied from any of them; the
influences below are adopted ideas, named per the repository's provenance policy. Ideas not listed —
the genre taxonomy with per-genre authority declarations, the named default layout (merged from the author's
`nix-config` and `agent-setup` conventions), read-when phrasing, verified-against stamps, the search-surface
rule, and the checker — were expressed independently, informed by the general framing below.

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
