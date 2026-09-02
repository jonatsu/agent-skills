# Measured Claims

Every claim this skill makes about model or tokenizer behavior, with what backs
it. Load once when a claim here is load-bearing for a decision, or when reviewing
whether a prompt cites its own evidence. `SKILL.md` links here from each claim.

---

Everything here that asserts model or tokenizer behavior, with what backs it.

**Positional attention.** Liu et al., *Lost in the Middle: How Language Models
Use Long Contexts*, TACL 2023 ([arXiv:2307.03172](https://arxiv.org/abs/2307.03172)),
abstract read 2026-08-27: performance "is often highest when relevant information
occurs at the beginning or end of the input context, and significantly degrades
when models must access relevant information in the middle of long contexts, even
for explicitly long-context models." Measured for
**retrieval** in multi-document QA and key-value tasks. Extending it to
instruction adherence in a system prompt is an inference, not a result. This
skill previously cited a "~20%" degradation figure; that number is not in the
abstract and was removed rather than sourced.

**Keyword tokenization.** Measured with `tiktoken` 0.14.0 on 2026-08-27:

| Text | cl100k_base | o200k_base |
|---|---|---|
| ` NEVER` mid-sentence | 1 | 1 |
| ` MUST NOT` mid-sentence | 2 | 2 |
| ` AVOID` mid-sentence | 2 | 2 |
| ` SHOULD NOT` mid-sentence | 2 | 2 |
| `NEVER` at line start | 2 | 2 |
| `MUST NOT` at line start | 3 | 3 |
| `AVOID` at line start | 2 | 2 |
| `SHOULD NOT` at line start | 3 | 4 |

**The saving is real but position-dependent and tiny.** Mid-sentence, `NEVER`
saves one token against `MUST NOT` and `AVOID` saves none against `SHOULD NOT`.
At line start both aliases save one, and `AVOID` saves two under `o200k_base`.
Prefer the aliases for readability and house consistency; a token argument in
either direction is worth less than the sentence spent making it.

Two corrections are recorded here rather than quietly applied. This skill first
claimed both aliases were single-token, which is false in every position except
` NEVER` mid-sentence. The correction that replaced it published only the
mid-sentence rows and concluded `AVOID` "saves nothing" — true for those four
rows and false at line start, which is the same one-sided reading in the opposite
direction. The full eight rows are above so neither claim can be made again from
half the data.

These are OpenAI tokenizers. A prompt targeting a different vendor's model is not
measured by them at all.

**Whether prompts of this kind help is contested, and that shapes the Iron Law.**
Two controlled studies, both preprints, both narrow, and they disagree.
arXiv:2602.11988 compared whole instruction files against none across four
agent/model pairs: developer-written files improved task success ~4%, generated
files reduced it ~3%, cost rose ~20% either way — and crucially the instructions
*were* followed, so the missing benefit is "not due to a lack of
instruction-following". arXiv:2604.11088 injected individual rules on SWE-bench
Verified: rules beat no rules by 6.9–13.8pp, **random rules performed as well as
curated ones**, and pass rates stayed flat from 0 to 50 rules. Its polarity
finding — that every individually beneficial rule was a negative constraint —
weakens from p=0.029 to p=0.25 across effect-size thresholds, and the authors
call it directional, not confirmatory.

**What survives both: presence appears to matter more than content.** Random
rules performing like curated ones, and instructions being followed without
producing benefit, both point at priming rather than literal
instruction-following. That is why the Iron Law asks whether a line should exist
before it asks how the line is worded. Neither study licenses confidence, and
neither supports aggressive pruning as evidence-backed — treat *inclusion* as the
thing needing justification, and cut per rule with a named reason.

**No size or instruction-count threshold survives.** Published ceilings range
from 60 to 300 lines with no agreement and no stated method; the only
vendor-documented figure is under 200 per file. The circulating "models follow
~150–200 instructions" claim is absent from the paper it is attributed to. Do NOT
write a threshold into a prompt, and do NOT cut to reach one.

**Unmeasured here, widely repeated.** Carried because they cost nothing to
follow, NEVER as established results: that "be efficient with tokens" invites
premature task abandonment; that few-shot examples add noise on a strong model
given an already-clear task; that self-critique without external feedback rarely
finds what the first pass missed. Treat each as a hypothesis. Where one is
load-bearing for a decision, test it against the target model rather than citing
this line.

**Provenance.** The two studies, the instruction-count correction, the size-ceiling
survey and the emphasis-keyword correction come from a rules-audit merge that
traced each to its primary source on 2026-08-27; every numeric claim it traced
had arrived distorted. The arXiv identifiers and their findings are recorded here
as reported by that audit and have NOT been re-verified against the papers in
this skill — grade them DOCUMENTED-at-one-remove, and open the source before
repeating a number from them.
