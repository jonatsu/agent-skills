# Archived: writing-great-skills

- **Archived**: 2026-08-27
- **Last deployed to**: Claude Code, OpenCode and GitHub Copilot CLI, via the
  `shared` group (`skills/shared/agent-stack/writing-great-skills`)
- **Successor**: none. `skills/shared/agent-stack/skill-forge` is the repo's
  authoring standard, but it does NOT carry this skill's vocabulary — see
  "What is lost" below.

## Why

**Nothing consumed it, and on Claude Code nothing could.** It set top-level
`disable-model-invocation: true`, so no skill could invoke it and Claude Code
could not preload it into a subagent; only the user typing its name reached it.
Its two dependents, both in `skill-judge`, were removed deliberately on
2026-08-27 (`7704d3e`) once that constraint was noticed, and a
`grep -rln "writing-great-skills" skills/ --include=SKILL.md` afterwards matched
only its own `SKILL.md`. OpenCode ignores the key entirely, so the skill was
model-invocable on one of three agents and unreachable on the others — behaviour
that differed per agent for no stated reason.

**It was a second authority on skill authoring, and it disagreed with the
first.** Its "Negation" failure mode argues that steering by prohibition
backfires and that a prohibition should be kept only as a hard guardrail;
`skill-forge` §5.6 and `skill-judge`'s D3 both make an explicit NEVER list a
scored requirement. Both positions are defensible; two deployed skills holding
them without acknowledging each other is not.

**It was never brought up to repo conventions, and its own `ATTRIBUTIONS.md`
half-disclosed why**: "body and `GLOSSARY.md` preserved verbatim from upstream".
Measured 2026-08-27 — zero RFC 2119 keywords across `SKILL.md` (86 lines) and
`GLOSSARY.md` (201 lines), no NEVER list, and `GLOSSARY.md` larger than
`SKILL.md` plus `ATTRIBUTIONS.md` combined (201 against 120), which
`skill-forge` forbids. The three live options were: apply the conventions,
record the verbatim-preservation exemption explicitly, or archive. Archiving was
chosen because the first destroys the provenance property the file claims and
the second keeps a deployed skill nothing reaches.

`SKILL.md` and `GLOSSARY.md` here are byte-identical to what was last deployed.
The Apache-2.0-style obligation does not apply — upstream is MIT — but
`LICENSE.upstream` and `ATTRIBUTIONS.md` MUST stay with this directory anyway,
because MIT's notice requirement travels with the copy.

## What is lost

Four concepts have no home in `skill-forge` today, and this is the record of
that gap rather than a claim it does not matter:

| Concept | Why it is not in `skill-forge` |
|---|---|
| **Leading words** — a pretrained concept the agent thinks with, anchoring behaviour in few tokens | No counterpart. `skill-forge` covers writing techniques but not vocabulary selection |
| **Context load vs cognitive load** — the trade a `disable-model-invocation` skill makes, and the router-skill cure | `skill-forge` states the invocation mechanics but not the cost model behind the choice |
| **Granularity: the two cuts** — split by invocation, split by sequence | `skill-forge` covers when to split `SKILL.md` into references, not when to split one skill into two |
| **Premature completion** and the completion-criterion defence | Adjacent to `skill-forge`'s pre-delivery checklist, but the diagnosis is absent |

Folding these in was deliberately NOT done in the same change: `skill-forge` had
just been through a full review pass and reopening it for unrelated material is
how a reviewed file loses its review.

## Reviving it

Do not restore this directory. If the vocabulary above is wanted, re-derive it
into `skill-forge` (or a new reference under it) as this repo's own prose — the
upstream text is MIT and could be adapted, but adapting it would reintroduce the
same verbatim-preservation claim that blocked bringing it up to conventions in
the first place.
