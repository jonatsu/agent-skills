# <System or change> Design

Status: \<proposed or accepted, with date and acceptance evidence; once implemented, the code wins
and this design is updated to match>
Design basis: \<governing requirements revision, scope, baseline and documentation convention>
Open items: \<links to the questions register and task ledger>

<!-- Authoring scaffold: replace prompts, remove these instructions, retain attribution.
Keep the section numbers and order; delete a section that would carry nothing. Tailor depth and
subsections. Do not invent missing facts. -->

## 1. Introduction and Goals

### 1.1 Requirements Overview

Explain the reader's problem, intended outcome and scope. Link accepted requirements.

### 1.2 Quality Goals

Identify the few accepted qualities that drive the architecture, with concrete scenarios.

### 1.3 Stakeholders

Identify relevant roles and what they need from this design; link an existing stakeholder record.

## 2. Architecture Constraints

Describe the constraints on design choices and their sources.

## 3. Context and Scope

Show the boundary, external participants, and exchanged inputs and outputs.
Distinguish domain interactions from protocols when that helps the reader.

## 4. Solution Strategy

Explain the principal choices, why they serve the goals, and where their details are defined.

## 5. Building Block View

### 5.1 Overall Structure

Show the components and relationships. Explain the decomposition and each component's
responsibility and interfaces. Refine only components whose internals need explanation.

## 6. Runtime View

Describe representative success, failure and recovery scenarios using components from section 5.
Explain the notable interactions shown by each diagram.

## 7. Deployment View

Map components to execution environments. Explain relevant connections and operational constraints.

## 8. Crosscutting Concepts

Explain applicable shared mechanisms once, such as identity, data ownership or error handling.
State where each concept applies and its limits.

## 9. Architecture Decisions

Record consequential choices and their rationale or link existing decision records.
Distinguish proposals from accepted decisions and avoid repeating section 4.

## 10. Quality Requirements

Reference accepted quality requirements and describe concrete scenarios where needed.
Keep their source authority explicit; do not invent metrics to complete this section.

## 11. Risks and Technical Debt

Describe known risks, consequences and possible mitigations in priority order.
Distinguish unresolved questions from accepted debt.

## 12. Glossary

Define domain and technical terms whose meaning matters to this design.

## Planning Handoff

Identify settled obligations, sensitive invariants, failure and recovery behavior, and any
remaining questions with owners. Keep implementation order, commands and review scheduling in the plan.

---

Format adapted from arc42 by Gernot Starke and Peter Hruschka, under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Changes: condensed Markdown prompts, design-basis and open-items preamble, omission of empty
sections, and planning handoff.
