# System and hardware requirements

The contract and the operations are domain-neutral: nothing about a lock, a fork, or a length ceiling
changes because the subject is a PCB. What changes is content vocabulary, and this file is it. Load it
when the requirements are hardware or system-level rather than software.

**Read the source-confidence table at the end before citing anything here.** Some of it is quoted from
primary sources, some is secondary-only because the standard is paywalled, and two things are marked
as gaps rather than filled in.

- [Verification methods](#verification-methods)
- [Requirement classes for hardware](#requirement-classes-for-hardware)
- [Environmental and mechanical](#environmental-and-mechanical)
- [Reliability](#reliability)
- [Regulatory and compliance](#regulatory-and-compliance)
- [System-level material](#system-level-material)
- [Source confidence](#source-confidence)

## Verification methods

Every requirement carries a Verification field. For non-software requirements the vocabulary is the
four-method taxonomy, defined here by the NASA Systems Engineering Handbook (NASA/SP-2016-6105 Rev 2),
section 5.3. That document is US government work and in the public domain, so it is quoted directly.

| Method | NASA's definition, abridged |
|---|---|
| **Analysis** | "The use of mathematical modeling and analytical techniques to predict the suitability of a design to stakeholder expectations based on calculated data or data derived from lower system structure end product verifications." Used when no built article is available; includes modelling and simulation |
| **Demonstration** | "Showing that the use of an end product achieves the individual specified requirement." A basic confirmation of capability, "differentiated from testing by the lack of detailed data gathering" |
| **Inspection** | "The visual examination of a realized end product." Used for physical design features or manufacturer identification; includes inspection of drawings and records |
| **Test** | "The use of an end product to obtain detailed data needed to verify performance." Produces "data at discrete points for each specified requirement under controlled conditions" and is "the most resource-intensive verification technique" |

The umbrella definition, from the handbook's glossary: *"Verification (of a product): Proof of
compliance with specifications. Verification may be determined by test, analysis, demonstration, or
inspection or a combination thereof. (Answers the question, 'Did I build the product right?')"*

**Variants exist and the taxonomy is not universal.** NASA folds verification by similarity into
Analysis explicitly — "Analysis can include verification by similarity of a heritage product" — while
several organisations treat **Similarity** as a fifth standalone method. SEBoK lists a different fifth
technique, **Sampling**. Do not present the four as the only possible set; state which set the project
uses in the contract declaration, alongside the types.

**No selection rule is quoted here, because none was found in the primary source.** The handbook lists
cost, schedule and risk as trade-off factors without a preference order. The widely repeated rule of
thumb — inspection cheapest, escalating through analysis and demonstration to test — is plausible and
unverified against a primary source. Treat it as a heuristic and say so if you rely on it.

What SEBoK does state is the failure mode, and it is worth carrying: relying on Test alone is a
documented pitfall, because analysis and inspection are cheaper and surface faults earlier.

**The rule for this skill.** Every non-software requirement names exactly one primary method. A
document whose every requirement says "Test" has not thought about verification; say so as an
incident, and propose the specific requirements that inspection or analysis would cover more cheaply.

## Requirement classes for hardware

The identifier classes in `references/authoring.md` — `FR`, `NFR`, `IF`, `CON` — carry over unchanged.
What follows is where hardware content lands within them.

| Class | Hardware content |
|---|---|
| `FR` | Processing and memory, storage, power supply and consumption, signal I/O |
| `NFR` | Mechanical and physical, environmental tolerances, reliability and lifetime |
| `IF` | Wired buses, wireless protocols, debug interfaces, and the data and timing across them |
| `CON` | Regulatory and compliance, imposed component choices, imposed form factors |

Three things belong in a hardware or system corpus that a software-derived typology omits entirely:

- **Interface requirements distinct from the physical channel.** "I2C at up to 400 kHz" describes a
  channel; the interface requirement is what crosses it — data, timing, electrical levels, error
  behaviour. A corpus that only names buses has documented its connectors, not its interfaces.
- **Operational concept, states and modes.** How the hardware behaves across standby, active, fault
  and degraded operation. Static specifications do not capture it, and it is where most integration
  surprises live.
- **Decomposition and traceability.** System-to-subsystem allocation, and bidirectional traceability
  from a subsystem requirement back to the system requirement that justifies it. This is a
  documentation-process category rather than a hardware property, and it is what makes the rest
  auditable.

Manufacturability and testability are sometimes listed as a further category. No standards-body source
was found for them during this research, so they are noted as a possible addition rather than a
verified omission.

## Environmental and mechanical

A tolerance with no range and no condition is not a requirement. Each of these needs a figure, a unit,
and the circumstances under which it holds.

| Concern | Vocabulary | Standard |
|---|---|---|
| Dust and water ingress | IP code — first digit solids, second digit liquids | IEC 60529 |
| Mechanical impact | IK code, IK00 to IK10 (IK10 is 20 J) | IEC 62262 |
| Temperature, humidity, altitude, shock, vibration | Named test methods rather than pass/fail limits | MIL-STD-810H |

MIL-STD-810 is a **tailoring framework, not a specification**: the standard's own position is that it
does not impose design or test specifications. A requirement citing it must name the method and the
tailored levels, never the standard alone. Its relevant methods are 500.6 (low pressure / altitude),
501.7 (high temperature), 502.7 (low temperature), 503.7 (temperature shock), 514.8 (vibration),
516.8 (shock).

## Reliability

A reliability figure without its conditions is unverifiable, and this is the single most common defect
in hardware requirements.

- **MTTF** — mean time to first failure under specified experimental conditions, computed as total
  device-hours divided by failures. Applies to non-repairable items.
- **MTBF** — the repairable-item counterpart. Under the constant-failure-rate assumption used for
  steady-state semiconductor work the two are numerically equal, though the concepts differ.
- **FIT** — failure rate scaled to failures per billion device-hours.

**Reject any MTBF, MTTF or FIT figure that does not state all three of these:**

1. **Temperature.** The effect is large, not marginal: one vendor worked example moves the same part
   from 2.26 FIT at 55 °C to 19.88 FIT at 85 °C.
2. **Statistical confidence level**, typically 60% or 90%. The same test data yields a materially
   different number depending which is chosen.
3. **The basis** — the activation energy used in the acceleration calculation, and the standard the
   figure was computed against.

A related documented mistake: taking the worst-case FIT and applying it as the overall failure rate.
The figure must be aggregated over a temperature-weighted mission profile instead.

## Regulatory and compliance

A compliance requirement names the regime, the class within it, and the applicable limit. "Must be
compliant" names nothing and cannot be verified.

| Class | Regime |
|---|---|
| Restricted substances | RoHS — Directive 2011/65/EU, restricting ten named substances; REACH — Regulation EC 1907/2006 |
| Electromagnetic compatibility | Generic emission IEC 61000-6-3 / -6-4, generic immunity IEC 61000-6-1 / -6-2, under EMC Directive 2014/30/EU. Generic standards apply only where no product-specific standard exists |
| Product safety | IEC 62368-1, the hazard-based standard superseding IEC 60950-1 and IEC 60065 |
| Radio type approval | Radio Equipment Directive 2014/53/EU in the EU; FCC Part 15 in the US |

RoHS's ten substances, from the European Commission's own text: lead, cadmium, mercury, hexavalent
chromium, polybrominated biphenyls, polybrominated diphenyl ethers, and the four phthalates DEHP, BBP,
DBP and DIBP.

## System-level material

Distinct from both hardware and software, and quoted from the NASA handbook.

**Concept of operations.** *"Developed early in Pre-Phase A, the ConOps describes the overall
high-level concept of how the system will be used to meet stakeholder expectations, usually in a
time-sequenced manner. It describes the system from an operational perspective and helps facilitate an
understanding of the system goals."*

**Baselines**, the standard vocabulary for physical and functional decomposition:

| Baseline | What it fixes |
|---|---|
| Functional | Top-level performance and interface requirements |
| Allocated | Those requirements allocated down to a configuration item, in enough detail to begin manufacturing or coding |
| Product | The as-built configuration during production |

**A NASA baseline is not this skill's `locked` flag, and conflating them will cause real errors.** A
baseline fixes a *configuration* at a level of decomposition; `locked` gates whether an agent may edit
*one document*. A corpus can hold a locked document describing an un-baselined design, and an
allocated baseline spread across four unlocked documents.

**Traceability**, again from the handbook, "provides bidirectional traceability back to the top
product layer requirements and manages the changes to established requirement baselines over the life
cycle."

The Interface Requirements Document and a functional, timing and state analysis are the standard
artifacts for the remaining system-level content. They are named here because they are the right
artifacts to ask for; their internal structure was not read and is not described.

## Source confidence

| Claim | Status |
|---|---|
| The four verification methods and their definitions | Primary — NASA/SP-2016-6105 Rev 2 §5.3 and glossary, read directly, public domain |
| ConOps, the three baselines, traceability | Primary — same handbook, read directly |
| MTTF, failure rate and FIT definitions; the conditions a figure needs | Primary — vendor reliability application notes, read directly. Copyrighted, so cited rather than reproduced |
| RoHS scope and the ten substances | Primary — European Commission page, read directly |
| IP codes, IK codes, MIL-STD-810H method numbers | **Secondary only** — the standards themselves are paywalled and were not read. Consistent across several independent compliance-lab sources |
| IEC 61000-6-x, IEC 62368-1, REACH | **Secondary only**, same reason |
| A rule for choosing among the four verification methods | **Gap.** No prescriptive rule found in the primary source. Do not invent one |
| Internal structure of the Interface Requirements Document and the states-and-modes analysis | **Gap.** Named in the handbook's contents but not read |

This table is the honest state of the research behind this file. When a project needs one of the
secondary-only items to be load-bearing, buy or borrow the standard and read it — do not promote a
compliance-lab summary to a citation.
