# Symptom to Cause to Fix

Load on the REPAIR branch only, at Step 2 (diagnose) or Step 4 (apply). On the
AUTHOR branch there is no observed failure, and the fix directions below become a
menu of techniques to apply speculatively — which is exactly what the Iron Law
forbids.

**Contents**
- [The diagnostic table](#the-diagnostic-table)
- [Choosing techniques](#choosing-techniques)
- [Reading the table honestly](#reading-the-table-honestly)

---

## The diagnostic table

Find the symptom. State the hypothesis before editing. One symptom often has two
plausible causes — say which you are betting on, so Step 5 can falsify it.

| Symptom | Likely cause | Fix direction |
|---|---|---|
| Ignores the output format | Format spec buried or vague | Move the format to the end, show the exact template, prefill the assistant turn, delimit with a schema, add a stop sequence |
| Inconsistent structure or malformed JSON | No exemplar of the exact shape | 2–5 few-shot examples in the exact format, prefill the opening token, lower the temperature |
| Hallucinates, or makes unsupported claims | No grounding and no escape hatch | "Answer only from the provided context", permit "I don't know", quotes-first pattern |
| Ignores a mid-prompt instruction | Competing or buried instructions | Move critical rules to the start or end, number them, cut the contradiction |
| Reasoning errors on multi-step work | No room to think | A thinking section before the answer, or the model's own extended reasoning |
| Too verbose, or the wrong tone | No length, audience or omit constraint | Specify length + audience + what to leave out; show one terse exemplar |
| Refuses, or is over-cautious | Missing legitimate context or role | Supply the real use context; frame the role explicitly |
| Too many tokens, or cost too high | Restated or redundant instructions | Dedupe, cut low-value few-shot, move static context into the cache, reference instead of repeat |
| Conflicting instructions | No priority order | Establish an explicit priority; remove the contradiction rather than ranking around it |
| Obeys the prompt but not the user | A rule written above the prompt's rank | Re-rank it. See the Rank calibration in `SKILL.md` |
| Acts without asking on risky work | An authority claim, or a gate that does not exist | See "What a prompt cannot do" in `SKILL.md`. A prompt edit MAY be the wrong fix here |

The last two rows route out of this file deliberately. A prompt that skips an
approval is usually not a wording defect, and fixing it in prose leaves the gap
open.

## Choosing techniques

**The techniques themselves live in `SKILL.md` → "API and task prompts"** —
delimiting, few-shot sets, prefill, stop sequences, temperature, explicit
fallbacks, caching. This file does not restate them. What belongs here is how
many to reach for and which two the main file does not cover.

**Pick the minimum that fixes the diagnosed mode.** Applying three techniques to
one symptom makes Step 5 uninterpretable: when it works you do not know which one
worked, so the other two become permanent cost you can never justify removing.
One technique per hypothesis, then verify.

Two techniques belong to repair rather than to authoring, so they are here:

- **A thinking section**, for a symptom diagnosed as reasoning error rather than
  instruction failure. Keep it separate from the final answer, or the format
  problem you did not have arrives with the fix.
- **Split by durability.** Where a prompt fails intermittently across turns, the
  cause is often a standing constraint living in the user turn, or per-request
  detail frozen into the system prompt. Move each to where its lifetime belongs
  before touching the wording.

## Reading the table honestly

**The cause column is a prior, not a diagnosis.** These are the causes that most
often produce each symptom in prompts of this shape. None of them is measured
here, and a symptom with an unusual cause will match a row and send the repair
the wrong way. That is what Step 5 exists to catch: when the traced output still
misses, the hypothesis was wrong — return to Step 2 rather than stacking a second
technique on top.

**A symptom that matches no row is information.** It usually means the failure is
not in the prompt: a tool returning something unexpected, a truncated context, a
model change, a harness that never delivered the instruction. Say so instead of
forcing the nearest row.
