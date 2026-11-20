# Adoption Review: human-architect-mindset

Date: 2026-11-20. Source: <https://github.com/bencium/bencium-marketplace>, directory `human-architect-mindset/`, commit
`5de46a39b4640fa419560cd0b67e4c4b50dac802`, MIT (copyright 2026 bencium.io). Read in full: `SKILL.md` (801 lines).
Outlined, with sections read where a finding cites them: `REFERENCE.md` (855), `EXAMPLES.md` (755), `CHECKLIST.md`
(575), and the plugin's `README.md` (320). Cites are `file:line`; skill files are relative to
`human-architect-mindset/skills/human-architect-mindset/`. Compared against `engineering/technical-design`,
`engineering/domain-modeling`, `engineering/implementation-planning`, `engineering/writing-specs`, and an
architecture-reviewer subagent definition that loads `technical-design` and `brooks-audit`. The method is skill-forge
review lite: no model runs.

## Recommendation

Do not adopt the skill. It fails both validators, its three reference files are unreachable from `SKILL.md`, and it
mixes four jobs under triggers broad enough to fire on most engineering requests. Its sound architectural content
(domain first, systems and failure modes, constraint navigation, tradeoffs) is already carried by `technical-design`,
`domain-modeling`, and the architecture-reviewer. Three ideas are worth writing independently: a constraint-fit check
for organizational and contractual limits, a rule that a departure from an existing architectural commitment is named
and justified, and an upstream contract change treated as a failure mode with a detection question. The verdict is
`invalid`.

## Validity

- Specification validator (`skills-ref validate`): fails. The frontmatter carries `when_to_use`, a field outside the
  Agent Skills specification (`SKILL.md:4`).
- Policy validator (`quick-validate.py`): fails. The frontmatter has no `license` field and no author metadata.
  The MIT licence exists only at the repository root.

## Findings

1. **Unjustified scope mixing.** Severity: blocker. Confidence: confirmed. The package combines four jobs that no
   shared task requires. They are an architecture-thinking method (`SKILL.md:126-530`), an argument that AI cannot be
   loyal (`SKILL.md:30-89`, `544-604`), an AI-tooling evaluation list (`SKILL.md:254-358`), and a Spec Driven
   Development framework with constitutions, traceability IDs, and 100% branch coverage (`SKILL.md:634-801`). The
   rubric makes this defect material on its own. Consequence: an architecture request loads all four, and the agent
   applies the AI-tooling and SDD material to designs that need neither. Repair: keep the architecture method only;
   specs and traceability belong to `writing-specs`, task decomposition to `implementation-planning`.

2. **The reference files are unreachable.** Severity: high. Confidence: confirmed. `SKILL.md` never names
   `REFERENCE.md`, `EXAMPLES.md`, or `CHECKLIST.md`; a search for the three names returns nothing. Consequence: 2,185
   lines, including the pre-mortem template (`REFERENCE.md:684-720`) and every checklist, load only if an agent lists
   the directory on its own. Repair: a pointer per file, naming the branch that needs it.

3. **Triggers fire on nearly any request.** Severity: high. Confidence: suspected (heuristic walkthrough, no trigger
   run). The description says to use the skill proactively on "architectural decisions, system design discussions, or
   multi-component planning" (`SKILL.md:3`), and the body lists keywords such as "design", "system", "security",
   "rust", and "MCP" (`SKILL.md:97-103`). Every match then pays for a 30 KB body and an announcement line
   (`SKILL.md:26`). Consequence: false triggers on ordinary coding work, and a scripted interruption on each one. The
   keyword list sits in the body, where it arrives too late to affect routing. Repair: narrow the description to
   design and architecture decisions, and drop the announcement.

4. **The AI-tooling list steers designs toward named products.** Severity: high. Confidence: confirmed. Questions
   15 to 20 ask "before proposing ANY architecture" whether claude-flow, agentdb, Rust/WASM, edge LLMs, the Claude
   Agent SDK, or self-learning loops would help (`SKILL.md:455`, `479-485`). The tool table names specific products
   and small models as defaults to evaluate (`SKILL.md:317-325`), and an example records "Always use claude-flow"
   (`EXAMPLES.md:705`). Consequence: an agent raises these tools in designs where nothing calls for them, which is
   the trend-chasing the skill's own loyalty section warns against (`REFERENCE.md:31-34`). The model list also dates
   fast. Repair: drop the list; a design weighs a new dependency against the problem, as `technical-design` already
   requires.

5. **The quality bar contradicts sound engineering.** Severity: medium. Confidence: confirmed. The SDD section sets
   100% branch coverage, a requirement ID on every function, and structure "so rigid that manual editing feels
   wrong" as the target (`SKILL.md:728-735`), and promises "deterministic assembly" (`SKILL.md:801`). Consequence:
   an agent that follows it adds traceability comments and coverage tests where they cost more than they protect.
   Repair: remove the section; our planning and testing skills set proportionate bars.

6. **Leftover conversation and stale counts.** Severity: low. Confidence: confirmed. "Your payment pipeline broke
   because a provider released a breaking SDK change" addresses the author's own incident (`SKILL.md:163`), "Before
   the four pillars" follows a list of five (`SKILL.md:17-22`, `32`), and the README keeps dated session notes
   (`README.md:151-288`) and lists a six-phase process the skill does not have (`README.md:307-313`). Consequence: the
   agent reads another user's history as context. Repair: rewrite in general terms.

7. **Related skills that are not shipped.** Severity: low. Confidence: confirmed. The skill points to
   `superpowers:*`, `relationship-design`, and `scientific-critical-thinking` (`SKILL.md:608-619`), none of which the
   package carries. Consequence: dead routing outside the author's environment.

## What Our Skills Already Cover

`technical-design` covers domain-first discovery, investigation of dependencies, compatibility obligations and prior
decisions (`SKILL.md:60-64`), checking upstream claims against a pinned source (`SKILL.md:74`), alternatives with
cost, failure mode, and reversibility (`SKILL.md:96-99`), and observability, rollout, and rollback (`SKILL.md:134`).
`domain-modeling` owns domain vocabulary and bounded contexts. `implementation-planning` owns decomposition into
independently verifiable units, which is the useful core of the "AI-aware decomposition" pillar. `writing-specs`
owns requirements, acceptance, and owners. The architecture-reviewer's six lenses already cover proportionality,
blast radius, hidden coupling, failure modes, trust boundaries, and unstated assumptions.

## Ideas Worth Writing Independently

These are written fresh if adopted; nothing is copied, and the source gets an `ATTRIBUTIONS.md` entry in whichever
skill takes an idea.

- **Constraint fit.** A design can be sound in isolation and still unable to ship: it needs a change from a team that
  does not own the system, an approval nobody has, or a break in a contract or deprecation timeline already
  promised. The source's constraint taxonomy (`SKILL.md:170-205`) names this; neither `technical-design` nor the
  reviewer asks who owns and approves what the design touches, or what cannot change even if it is wrong. Owner:
  `technical-design`'s investigation section, and the reviewer's soundness lens.
- **Departing from a commitment.** When a design abandons an existing decision, pattern, or stack, it states what the
  departure gains over evolving the current one and how the transition runs. The source frames this as loyalty
  (`SKILL.md:76-87`, `REFERENCE.md:48-90`); the usable rule is the justification, not the framing. Owner: the same
  two places.
- **Upstream contract change as a failure mode.** A dependency can change its interface without notice, as well as
  go slow or down, and the design should say how the change would be detected and by whom (`SKILL.md:162-168`,
  `REFERENCE.md:684-720`). Owner: the reviewer's failure-modes lens; `technical-design` already lists observability.

## Not Worth Taking

The loyalty philosophy and its claims about AI character (`SKILL.md:34-50`), the SDD extension, the AI-tooling list,
the announcement line, the 20 fixed questions asked before every architecture, and the role matrix that assigns
"achieve 100% test coverage" to AI (`SKILL.md:771`).
