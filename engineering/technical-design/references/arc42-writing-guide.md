# Writing an arc42 Design

Use this guide with [the template](../assets/arc42-design-template.md).
The [worked design](arc42-example.md) demonstrates the intended depth for a small system.

The twelve sections give readers stable places to find information. They do not prescribe equal
lengths. Keep the section numbers and their order; omit a section that would carry nothing rather
than filling it with an applicability line, and tailor the subsections. Missing evidence or an
unresolved requirement stays visible in the questions register rather than becoming invented content.

## Establish the Reader's View

Start with the problem and boundary so readers understand what the system does before meeting its
internals. Name the governing requirements and distinguish the observed baseline from the proposed
design. For a bounded change, explain affected behavior and link unchanged context.

Within a view, show the structure, explain its relationships and rationale, then develop only the
details readers need. A diagram cannot explain an unlabeled arrow or an unexplained responsibility.
Keep names consistent across diagrams, tables and prose. Introduce a domain concept before a scenario
depends on it.

Use paragraphs for reasoning and consequences. Use tables when readers compare responsibilities,
constraints or alternatives. Use numbered steps for an ordered interaction, naming the component
responsible for each action. Keep implementation task sequences out of runtime scenarios.

## Choose Content and Depth

| Section                      | Reader's question                                                | Useful form and stopping point                                                                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Introduction and Goals    | What problem does this solve, for whom, and what matters most?   | Brief requirements summary and source links; a few prioritized quality scenarios; relevant stakeholder roles. Do not reproduce a specification or invent names and targets.    |
| 2. Architecture Constraints  | Which choices are constrained, and why?                          | A compact table of constraints, sources and implications. Separate imposed constraints from chosen approaches.                                                                 |
| 3. Context and Scope         | What is inside the system and what crosses its boundary?         | Context diagram with a table explaining participants and exchanges. Keep internal components in section 5; link detailed external contracts.                                   |
| 4. Solution Strategy         | Which choices make the goals achievable?                         | A short explanation or goal-to-approach table. Connect choices to requirements and constraints, then link details instead of repeating them.                                   |
| 5. Building Block View       | What are the parts, their responsibilities and their interfaces? | Overall diagram, decomposition rationale and responsibility table. Explain selected internals where complexity or risk justifies it; avoid a file inventory.                   |
| 6. Runtime View              | How do the parts cooperate in important situations?              | Representative scenarios, including important failure and recovery paths. Use components from section 5 and explain the interactions. Stop before routine call-by-call detail. |
| 7. Deployment View           | Where do the parts run and communicate?                          | Component-to-environment mapping with relevant constraints. A local tool may need only a paragraph; deployment architecture is distinct from rollout task order.               |
| 8. Crosscutting Concepts     | Which mechanisms apply across components?                        | Explain each relevant concept once, including its scope, rationale and limits. Do not fill an exhaustive catalogue of possible topics.                                         |
| 9. Architecture Decisions    | Why were consequential alternatives resolved this way?           | Link existing ADRs or record the decision, status, rationale and consequences. Use section 4 for the short strategic overview.                                                 |
| 10. Quality Requirements     | What observable conditions define the required quality?          | Reference accepted requirements; expand scenarios with context, stimulus and response measure when needed. Keep proposals provisional and reuse existing identifiers.          |
| 11. Risks and Technical Debt | What could go wrong, and what remains unresolved?                | Prioritized risks with consequences and mitigation options. Do not manufacture risks or disguise unresolved acceptance as technical debt.                                      |
| 12. Glossary                 | Which words need a shared meaning?                               | Brief definitions or links to the existing glossary. Define a term at first use as well when the explanation depends on it.                                                    |

## Preserve Authority and Coherence

Sections 1 and 10 provide architecture readers with requirements context; the governing specification
continues to own intended behavior and acceptance. If quality goals are missing, label proposed
scenarios as assumptions for confirmation. Do not silently choose service levels or product policy.

Keep each full explanation in one place. A brief summary plus a link helps orientation; repeating
the same contract in several chapters creates opportunities for disagreement. Reference existing ADRs
and repository conventions rather than creating parallel sources of truth.

Before handoff, trace an important scenario across context, components and deployment. Check names,
interfaces, states and numerical claims against one another and the governing requirements. Ask
whether a reader can explain who owns each action and why the main design choices were made.

## Upstream Guidance and Examples

- [Section guidance](https://docs.arc42.org/home/) explains content, motivation and form.
- [Tailoring](https://faq.arc42.org/questions/K-2/) favors a recognizable top-level structure.
- [Economical documentation](https://faq.arc42.org/questions/B-16/) explains how to choose useful depth.
- [HtmlSanityCheck](https://examples.arc42.org/systems/htmlsc/) pairs structural views with rationale
  and responsibility tables, then traces checking and reporting at runtime.
- [status.arc42.org](https://examples.arc42.org/systems/status.arc42.org/) gives short operational
  explanations. Treat examples as illustrations of form, not verified implementations or permission
  to import their requirements. Check their cross-view consistency before imitating a passage.

Adapted guidance: Gernot Starke and Peter Hruschka's arc42, with independently written workflow
integration by Joonas Onatsu. This reference is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
See [attribution and source revisions](../ATTRIBUTIONS.md).
