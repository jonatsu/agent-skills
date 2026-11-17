# Project Goals

Project goals say where a whole project is going: why it exists, what success looks like, and what it will and will
not do. They bind every session's work on scope and purpose, they change only when the owner decides, and they last
as long as the project. Read this file when a user wants to set up, state, retrofit, or tidy a project's goals.

## Contents

- What the goals always record
- What they record on request
- Work it out with the user
- Place the goals
- Wire them in
- Done

## What the Goals Always Record

Fill all three slots before anything is written:

1. **Purpose.** What the project is for, in a sentence or two. When it has several goals, give each its priority and
   the rule for a conflict between them, such as "the primary goal wins".
2. **Success signal.** At least one observation that shows the project is working. Use a binary check or a named
   person's judgment when no honest metric exists. Rewrite an activity, such as "improve the tooling", as the
   outcome it serves.
3. **Scope and authority.** What is in, what is explicitly out, and who decides a change to these goals, named as
   the user names them, such as "the user" or a maintainer's role.

## What They Record on Request

Method, standards, and environment belong in the goals only when the user wants them fixed: the tools, languages,
platforms, quality bar, or ways of working every session must follow. Ask whether the user wants to fix them. When
the user leaves the approach to the agents, record that as a decision, such as "agents choose the approach and tools
as long as the goals hold", because an empty section reads as an oversight and invites each session to guess.

## Work It Out with the User

Read the README, the instruction files, the backlog or roadmap, notes, and the code layout before asking anything.

- **A new project.** The user may not yet know what the project should be. Bring the domain's expertise: propose
  candidate purposes, success signals, and exclusions, with the usual risks of that kind of project, each labeled as
  your recommendation.
- **An existing project.** Reconstruct the goals the repository implies. Name the evidence behind each item, and mark
  as your recommendation anything the repository does not show.

Fit the goals to the kind of project rather than to one template. A product needs promises and limits that every
feature must keep. An exploratory or research workspace often has a concrete primary goal and a longer-term
secondary one, and may leave the approach open on purpose. Personal infrastructure needs what must keep working and
how much upkeep is acceptable.

Mark each item as the user's decision, inferred from named evidence, or your recommendation; only the user's
decisions become goals. Ask one consequential question at a time, with your recommended answer, and keep the
other open items as a short list for later turns. The user is often deciding the project's direction while
answering, so a batch of questions gets rushed answers.

Show the proposed goals in the reply and write nothing until the user confirms their content. Then write the
confirmed wording as it stands; a rule the user did not confirm is a new proposal for the next turn. Goals sit
above specs, designs, and plans; leave features, architecture, and the choice between technologies to those skills.

## Place the Goals

Resolve where the goals live, in this order:

1. a location the user names, including the README or `AGENTS.md`;
2. existing goal documents, kept under their current name;
3. the repository's documented convention; then
4. a dedicated file, named with the user, beside the README when the repository's documentation folders each hold
   a stated kind of document, such as runbooks, that goals are not.

No fixed name is required: "goals", "purpose", or "product" can all fit. Keep one full copy. When the goals are
already stated in more than one place, show where the copies disagree, ask which version holds, and propose one
owner with a pointer from the other files.

## Wire Them In

Goals that no session loads do not steer the work. Propose these changes with the goals, and apply them once the user
confirms:

- `AGENTS.md`, or the repository's always-loaded instruction file, gets a line that points to the goals, states who
  decides a change to them, and tells agents to stop and ask before work that would break them, so a later session
  asks instead of quietly widening the project. Create the file when none exists and the user agrees.
- The README opens with what the project is for, in a sentence or two, and links to the goals when they live
  elsewhere, because a reader who does not find that on the front page moves on.

Report each file you changed.

## Done

The work is done when every always-recorded slot holds the user's decision. Each on-request item is either recorded
or left to the agents by the user's choice. The goals live in one place, `AGENTS.md` points to them, the README
opens with the purpose, and the user has confirmed the result.
