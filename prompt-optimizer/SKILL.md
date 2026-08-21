---
name: prompt-optimizer
description: "Engineer and optimize LLM prompts against observed failures — system prompts, task/API prompts, agent instructions, few-shot sets, and eval loops. Use when the user says 'optimize this prompt', 'improve my prompt', 'write a prompt', 'my prompt is not working', 'the model ignores the format', 'output is inconsistent', 'reduce prompt tokens', 'make the system prompt better', 'fix these agent instructions', 'design few-shot examples', or 'the model hallucinates/refuses/is too verbose'. Actions: optimize, improve, rewrite, debug, compress, evaluate, design a prompt or system prompt. Does NOT author Claude Code skills — defer to skill-forge for that."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Prompt Optimizer

IRON LAW: EVERY CHANGE MUST TARGET A NAMED FAILURE MODE AND BE CHECKED AGAINST A CONCRETE INPUT/OUTPUT EXAMPLE. Never rewrite a prompt to "sound better" without a failure hypothesis and a way to verify the fix.

Scope: general LLM prompts — system prompts, task/API prompts, agent instructions, few-shot sets. For authoring Claude Code **skills**, use `skill-forge` instead. For Claude model IDs, pricing, parameters, prefill, tool-use format, and prompt-caching mechanics, read the `claude-api` skill — MUST NOT guess these.

## Workflow

```text
Prompt Optimizer Progress:

- [ ] Step 1: Locate prompt + failure ⚠️ REQUIRED
  - [ ] 1.1 Get the actual prompt text and target model
  - [ ] 1.2 Get the failing output vs. desired output (or representative inputs)
- [ ] Step 2: Diagnose — symptom → failure mode, form a hypothesis
- [ ] Step 3: Confirm scope ⚠️ REQUIRED (before a substantial rewrite or token/accuracy trade)
- [ ] Step 4: Apply targeted edits (anatomy + technique catalog)
- [ ] Step 5: Verify against the examples
- [ ] Step 6: Deliver as a diff + rationale
```

## Step 1: Locate prompt + failure ⚠️ REQUIRED

MUST obtain the real prompt, not a paraphrase, and the target model. Ask:
- What did the model actually output, and what did you want instead?
- If no failing sample exists: what are 2–3 representative inputs, including an edge case (empty, null, very long, adversarial)?

NEVER optimize a prompt you have only been described. Read it verbatim first.

## Step 2: Diagnose

Map the symptom to a failure mode, then state the hypothesis before editing.

| Symptom | Likely cause | Fix direction |
|---|---|---|
| Ignores output format | format spec buried or vague | move format to end, show exact template, prefill assistant turn, delimit with XML/JSON schema, add stop sequence |
| Inconsistent structure/JSON | no exemplar of exact shape | 2–5 few-shot examples in the exact format, prefill the opening token, lower temperature |
| Hallucinates / unsupported claims | no grounding, no escape hatch | instruct "answer only from provided context", permit "I don't know", quotes-first pattern |
| Ignores a mid-prompt instruction | competing/buried instructions | move critical rules to start or end, number them, cut contradictions |
| Reasoning errors | no room to think | add chain-of-thought in a `thinking` section before the answer, or use extended thinking |
| Too verbose / wrong tone | no length/audience/omit constraints | specify length + audience + what to omit, show one terse exemplar |
| Refuses / over-cautious | missing legitimate context/role | supply the real use context, frame the role explicitly |
| Too many tokens / cost | restated or redundant instructions | dedupe, cut low-value few-shot, move static context to prompt cache, reference instead of repeat |
| Conflicting instructions | no priority order | establish explicit priority, remove the contradiction |

## Step 3: Confirm scope ⚠️ REQUIRED

Before a substantial rewrite, or any change that trades tokens against accuracy, stop and confirm:
- Rewrite in place, or produce an alternative to compare?
- Optimize for accuracy, latency, or token cost — which wins on conflict?
- Any constraints that MUST be preserved (format contract, tone, downstream parser)?

⚠️ Do NOT silently replace a working prompt.

## Step 4: Apply targeted edits

**Anatomy** (order matters): role/task → long context/data (before instructions) → numbered instructions → few-shot examples → output format → prefill/stop. Delimit each section with XML tags so the model can find boundaries.

**Technique catalog** — pick the minimum that fixes the diagnosed mode:
- XML tags to delimit instructions, data, and examples.
- Few-shot: 2–5 diverse examples in the exact target format; cover edge cases; don't over-fit (the model will parrot).
- Prefill the assistant turn to force format and skip preamble.
- Chain-of-thought / a `thinking` block for reasoning tasks; keep reasoning separate from the final answer.
- System prompt for persona and standing constraints; keep per-request detail in the user turn.
- Explicit fallbacks: "if X is missing, respond Y"; permit "I don't know".
- Temperature, stop sequences, prompt caching as levers — confirm exact params/behavior via `claude-api`.

Prefer restructuring over emphasis. Adding an instruction MUST come with removing the one it conflicts with or duplicates.

## Step 5: Verify against the examples

Trace the revised prompt against the Step 1 inputs — at minimum the failing sample and one edge case — and compare output to the desired result. If it still misses, return to Step 2; do not ship on faith. For prompts with an eval harness, run it and report the delta.

## Step 6: Deliver

Present a diff (old → new), and for each change name the failure mode it targets. State residual risks and any token/accuracy trade-offs. Do not deliver a silent full replacement.

## Anti-Patterns

- Rewriting prose to "read better" with no failure hypothesis or test.
- Piling on emphasis (ALL CAPS, "VERY IMPORTANT") instead of restructuring.
- Adding instructions without removing the ones they contradict or duplicate.
- Cutting tokens by silently dropping edge-case coverage.
- Guessing model IDs, pricing, parameter names, prefill, or caching behavior instead of reading `claude-api`.
- Testing only the happy path while ignoring the input that caused the complaint.
- Over-fitting few-shot examples so the model memorizes them.
- Authoring a Claude Code skill here instead of handing off to `skill-forge`.

## Pre-Delivery Checklist

- [ ] Each change maps to a named failure mode from Step 2.
- [ ] Revised prompt traced against ≥1 failing input and ≥1 edge case; outputs compared to desired.
- [ ] No net instruction contradictions introduced.
- [ ] Token/accuracy trade-offs disclosed.
- [ ] Anthropic specifics (model, params, caching) verified via `claude-api`, not guessed.
- [ ] Delivered as a diff + per-change rationale, not a silent replacement.
