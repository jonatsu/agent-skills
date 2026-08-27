# API and Task Prompts

Load when the target is the prompt behind a single API call rather than an agent:
few-shot sets, prefill, temperature, stop sequences, caching. Skip it for system
prompts, agent definitions, tool descriptions and global rule files.

Everything in `SKILL.md` applies. This file is the extra surface a single call
has and an agent prompt does not.

---

**Anatomy, and the order is load-bearing:** role and task -> long context and
data -> numbered instructions -> few-shot examples -> output format -> prefill
and stop. Long data goes BEFORE the instructions, so the instructions are the
most recent thing the model read. Delimit each section so boundaries are findable.

**Few-shot sets.** 2–5 diverse examples in the exact target format. Cover the
edge cases. AVOID over-fitting: a model given near-identical examples parrots
them. On a strong model with an already-clear task, few-shot may add noise rather
than signal — see [Measured claims](#measured-claims).

**Prefill** the assistant turn to force a format and skip preamble. **Stop
sequences** end generation at a known boundary. **Temperature** trades diversity
against format stability; lower it when the shape matters more than the wording.

**Explicit fallbacks beat silent failure.** "If X is missing, respond Y", and
permit "I don't know" — a model with no escape hatch invents one.

**Static context belongs in the cache**, and cache-busting content belongs after
it. NEVER put timestamps, request IDs or volatile state at the start of a
cacheable prompt.

⚠️ Confirm exact model IDs, parameter names, prefill mechanics and caching
behavior against the `claude-api` skill. MUST NOT guess them.
