# REVIEW: the tests, the ladder, the grades

Load at REVIEW Step 2. These are the tables the branch applies; `SKILL.md` holds
the workflow, the blocking first step and the reporting rules.

---

### Step 2: Apply the tests in order

Each test names what settles it. A line that fails one is a finding.

| Test | The question | Settled by |
|---|---|---|
| **Retention** | Does this line change a decision the model makes? | Naming the decision and what changes. A line that is correct, well-written and changes nothing is overhead — and is obeyed anyway, costing reasoning every session |
| **Verifiability** | Could a reviewer tell from the output whether it was followed? | Reading the output. A rule whose *trigger* is subjective — "material", "proportionate", "when appropriate" — fires inconsistently and is worth rewording or cutting |
| **Single home** | Does this rule appear exactly once across everything loaded? | Searching the whole loaded set. Deliberate safety redundancy is allowed and MUST be labelled; everything else drifts apart the moment one copy is edited |
| **Contradiction** | Does any other loaded line disagree with this one? | Reading them together. On at least one tool both texts are in context and neither wins |
| **Currency** | Does every named path, command, tool and file still exist? | Checking each. A stale rule is worse than a missing one — it misdirects, and the model follows it correctly to a wrong result |
| **Mechanism fit** | Is this held by the weakest mechanism that can hold it? | The ladder below |
| **Rank** | Does this line claim authority the prompt does not have? | `SKILL.md` → What a prompt cannot do |
| **Escape hatch** | Does this rule say what to do when it does not fit? | Its own text. See `SKILL.md` → Escape hatches |
| **Plain English** | Is there an everyday word that loses nothing? | Substituting it. Keep genuine terms of art; replace in-house shorthand |
| **Size** | What is the effective size in bytes, including everything pulled in? | Measuring. Never lines — wrapping alone moves that count by a factor of two |

**Mechanism fit is a ladder, weakest sufficient tier wins:**

| Tier | Mechanism | Fits |
|---|---|---|
| 1 | Block or prompt on an exact pattern | Rules reducible to a string or regex |
| 2 | Linter or formatter | Rules an existing tool already checks |
| 3 | Model self-check before yielding | Judgment rules with an observable output |
| 4 | Second-model or human review | Judgment rules where the model is being judged |

A rule too imprecise for tier 1 SHOULD say so rather than be forced down: a check
that fires on legitimate cases trains the model to ignore it. Record why a rule
sits at its tier, or someone later "improves" it into a broken regex.

⚠️ **Cut per rule, never to a target.** Removing a duplicate, a contradiction, an
obsolete fact or an inert line is defensible on its own terms. Cutting to reach a
byte or line count is not — no threshold is established for prompts, and the
evidence that exists is contested. See `evidence.md`.

### Step 3: Grade the prompt's own claims

Every empirical assertion in the prompt under review gets a grade. Higher wins,
and where a measurement or vendor documentation conflicts with practitioner
consensus, the authoritative source decides and the consensus claim is dropped or
marked superseded.

| Grade | Means |
|---|---|
| MEASURED | Observed directly, probe named |
| OBSERVED | Seen live, not under controlled conditions |
| DOCUMENTED | Stated by vendor docs, not exercised |
| CONSENSUS | Independent practitioners converge; no stated method |
| INFERRED | Reasoned from the above |

**Wide repetition is how a wrong number spreads; it is not evidence that it is
right.** An ungraded numeric claim is a finding on its own. NEVER accept a
citation that has not been opened — drop the claim, weaken it to an observation,
or mark it `[UNVERIFIED]`. Attaching a plausible-looking reference is a defect,
not a courtesy.

Within the ranking CONSENSUS is still evidence: where no authority addresses a
question, a position several practitioners reach independently is the best
available input. It is weaker in one specific way — nobody can say what would
falsify it.
