---
name: writing-for-humans
description: "Copy-edit supplied prose, match an established style, or diagnose AI-style patterns."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing for Humans

Use this skill to copy-edit supplied prose that reads formulaic, padded, promotional, or unlike its author.
Follow active global and repository writing policy. This skill does not set document structure or generic prose
style; use `technical-writing` for document-level decisions.

## Preserve Meaning and Scope

Preserve every supported claim, distinction, and intended qualification. Do not invent facts, actors, dates,
numbers, causes, sources, opinions, or personality.

Do not silently remove an unsupported assertion, ambiguity, missing prerequisite, or factual gap. Flag it for
the author or state what cannot be established.

When editing a file, change prose only. Preserve code blocks, inline code, frontmatter, link targets, table
syntax, identifiers, commands, and quotations unless the user explicitly asks to change them.

## Match the Author

Use a supplied writing sample as the voice target. Preserve its appropriate level of formality, person, and
degree of personality.

Do not flatten a distinctive voice into generic prose. Do not add a viewpoint, familiarity, humor, or personal
stance the source does not contain.

## Adapt to an Established Style

Use this branch when the user asks to match a supplied author or house style.

Require representative exemplars from the same document type. One sample supports voice matching; use two or
more before inferring repeatable conventions. Do not treat an isolated preference as a rule.

Extract a compact style profile:

- scope: the document types and audience it covers;
- observed conventions: repeated structure, register, formatting, and terminology choices;
- evidence: the exemplar passages supporting each convention; and
- boundaries: voice, rhythm, humor, and choices the profile does not govern.

Apply only conventions supported by the profile. For each material change, identify the convention it follows.
Leave a preference alone when no exemplar supports it.

Global and repository writing policy still applies. A style profile may refine those rules, but cannot override
them. Preserve the source author's voice wherever the profile is silent.

## Diagnose Before Rewriting

Treat a lone style signal as a prompt to inspect, not a defect. Rewrite for style only when two or more
independent symptoms occur in the same passage.

Useful symptoms include:

- chat residue, such as greetings, offers to continue, or answers addressed to a conversation rather than the
  document reader;
- meta-commentary that announces the document instead of advancing it;
- promotional language that substitutes importance for a specific claim;
- repeated rhetorical setups or manufactured revelations across a passage; and
- unnamed or false agency that hides an actor the source can establish.

For source accuracy, act on one signal immediately: a dropped claim or unsupported new detail requires
correction even when no style pattern accompanies it.

## Deliver the Edit

For a rewrite, return the edited text or requested file change. For a review, separate:

- proposed prose edits;
- factual, structural, or missing-context issues that require author input; and
- passages left unchanged because the evidence or intended voice is unclear.

Load `references/diagnostics.md` only for a long draft or a difficult AI-style diagnosis. Do not use a
blocklist mechanically.
