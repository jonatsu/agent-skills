# Project Goals: Brainstorm Draft

Status: incomplete draft from idea-brainstorming, 2026-11-17; the user confirmed it captures what they want to
refine. Route: straight to authoring with `skill-forge`, because the change lands in one existing skill and its
behavior is stated here; a separate spec would have no reader. Each item is marked as a user decision (U), an agent
recommendation (R), or provisional (P).

## Original Idea

Agents have no way to establish a project's direction when the user lacks a clear vision or deep domain knowledge,
most of all in projects started from scratch. The engineering pipeline (idea-brainstorming, writing-specs,
technical-design, implementation-planning) assumes the user is narrowing a vision they already hold. Without a
robust statement of where a project is going, the quality of work, the methods, and the environments vary from
session to session.

Four of the user's repositories showed the range. A product-style OCR tool states its purpose, core promises, firm
limits, scope, and a fit test for every change in one document, and drifts little. An exploratory
reverse-engineering workspace carries a primary and a secondary goal, written once in its README and again in its
`AGENTS.md`. A personal NixOS configuration describes what it is but never what it is for. A sandbox launcher in
early design has no stated direction yet.

## Desired Outcome

The user and an agent define a project's goals together, interactively, for a new project or retrofitted onto an
existing repository without rerunning the pipeline, and the result is wired into what every session loads. (U)

## Current Direction

- Extend `define-goal` rather than add a skill. It gains a **project goals** mode beside its current **run goal**
  mode, which stays unchanged. A run goal takes its outcome from the project goals when they exist. (U)
- Keep `SKILL.md` lean: it routes between the two modes, and the project goals mode lives in a reference file. The
  description names both branches distinctly, since one word, "goal", now covers two time scales. (R)
- The skill is flexible to adopt and interactive; it is not a fixed procedure. The result is held to the bar of the
  product-style example by default. (U)

## What the Project Goals Always Record

1. The purpose, including several goals and their priority when there are several. (U)
2. At least one observable success signal; a binary or human-judged signal when that is the honest one. (U)
3. What is in scope, what is explicitly out, and who decides a change. (U)

## What They Record on Demand

Method, standards, and environment, per project and only when the user wants them. Leaving the approach to the
agent is a valid choice, recorded as such rather than left as a gap. (U)

## Placement

- No fixed term for the document. Its name follows the repository and is chosen with the user. (U)
- Resolution order: a path the user gives; existing goal documents; the repository's documented convention; else a
  dedicated file. The user may always place the goals in `AGENTS.md` or the README instead. (U)
- `AGENTS.md` always carries a pointer to the goals and the who-decides rule, so every session loads them. (U, R)
- The README's opening always says what the project is, and links to the full goals when they live elsewhere,
  because a human reader who does not find that on the front page moves on. (U)
- A retrofit detects goals written in more than one place and offers to consolidate them under one owner. (R)

## Wiring

The skill owns the wiring: it proposes the changes to `AGENTS.md` and the README, and the user confirms them. (U)

## Knock-on Changes

- context-architecture's default layout gains a genre for project goals: binding on purpose and scope, changed only
  by the owner's decision, and alive for the life of the project. (R)
- `engineering/README.md` places the project goals mode in the pipeline. (R)
- idea-brainstorming's "governing overview" wording recognizes project goals as that overview. (R)
- A trigger evaluation checks that the two-branch description routes both kinds of request. (R)

## Observable Success Signal

The user takes one new project and one retrofit of an existing repository through the project goals mode and
accepts both results. A fresh session in each repository then cites its goals when choosing scope or method,
without being prompted. (U)

## Questions for Authoring

- The exact description wording for two branches. (P)
- How the retrofit reconstructs implicit goals from an existing repository's code and documents. (P)
- How the mode adapts across kinds of project, such as a product, an exploratory workspace, personal
  infrastructure, or a library. (P)
- After authoring, run behavioral evaluation rounds with the headless method used for the pipeline skills. (U)
