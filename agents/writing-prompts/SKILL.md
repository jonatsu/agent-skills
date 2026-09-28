---
name: writing-prompts
description: Write or improve a prompt so another model acts correctly on the first pass, from a user's draft or a system or task prompt to the brief an agent hands a subagent when delegating. Use when asked to improve, rewrite, or review a prompt with no recorded failures, or before writing a delegation brief. Not for repairing a prompt from observed failures (prompt-debugging), Agent Skills (skill-forge), or repository instruction files (agents-context-docs).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing Prompts

Write a prompt that a capable model with none of your context acts on correctly the first time. Treat the receiver
as a brilliant new colleague: expert in its craft, blind to your task, your conversation, and your conventions.
Everything it needs and cannot discover is in the prompt, or the prompt says where to find it.

The test is the **cold read**. Read the prompt as someone who has seen nothing else. Wherever that reader would have
to guess, the model guesses too.

## Choose the Branch

- **Improve a user's prompt:** a draft, a system prompt, or a task prompt the user will run or ship. Advise only:
  deliver the diagnosis and the rewritten prompt, and leave the task itself undone. A user who wants the task done
  asks for it as an ordinary request. Follow [Improve a User's Prompt](#improve-a-users-prompt).
- **Write a delegation brief:** the prompt you send a subagent. Write it and send it. Follow
  [Write a Delegation Brief](#write-a-delegation-brief).

Both branches build on the same core.

## The Core Every Prompt Carries

1. **Outcome.** What done looks like, stated so the receiver can check it: acceptance criteria, not an activity.
2. **Reason.** Why the task and each non-obvious constraint exist. A model generalizes from a reason: "the output
   is read aloud, so write numbers as words" also settles cases the rule never named.
3. **Missing context.** The decisions already made, what is already verified or ruled out, and the conventions in
   force. Point to what the receiver can look up itself, a path, a command, a document, rather than pasting it.
   Carry only what it cannot find by looking.
4. **Scope and authority.** What the receiver may change, what it must leave alone, and whether it acts or only
   reports. Say which in plain words: "change this function" gets changes, "suggest changes" gets suggestions.
5. **Result.** The shape, length, and format of what comes back, and where large output goes.

## Write It So It Lands

- **Direct and specific.** Imperative sentences. Number the steps only when order or completeness matters.
- **Separate the kinds of content.** When a prompt mixes instructions, context, examples, and input, give each its
  own tagged or headed block. Put long material first and the ask last.
- **Say what to do.** State the target behavior; a prohibition names the thing and makes it more likely. Keep a
  prohibition only for a hard guardrail, paired with what to do instead.
- **Calibrated emphasis.** Write in normal register. Capitals and "CRITICAL" make current models over-apply a rule;
  keep emphasis for the one guardrail that must not bend.
- **Examples teach the shape.** Use a few, make them varied and close to the real case, and mark them as examples.
  The receiver copies what they share, including what you did not mean.
- **Match the style you want back.** A prompt written in heavy Markdown invites heavy Markdown.
- **Cut the no-ops.** Drop instructions the model already follows by default, such as "be helpful" or "be
  thorough". Length is set by the missing context, never by padding.

## Improve a User's Prompt

1. Read the prompt and where it will run: the target model or tool, and the project it acts on. Recover what the
   environment already answers, such as the conventions file and the stack.
2. Check it against the core. Mark each missing item as recovered from the environment or needed from the user.
3. When the user alone can supply an item that would change the prompt materially, ask at most three questions
   before rewriting. Otherwise state your assumptions in the diagnosis.
4. Deliver, in the user's language:
   - the diagnosis: what the prompt already does well, then each issue with its consequence and fix;
   - the rewritten prompt in one fenced block, ready to paste, in the language its target expects; and
   - the reason for each material change.

Done when every core item is present in the rewrite or listed as an assumption or an open question.

## Write a Delegation Brief

The receiver starts cold. It has not seen the conversation, and it may not load your instruction files or skills.

- **Outcome, reason, and done.** One or two sentences each.
- **What you established.** Paths with line numbers, decisions taken, hypotheses ruled out, so it does not redo them.
- **Rules it must follow.** The instructions that apply to this task and that it may not inherit, such as staging
  rules, writing style, or a required tool. Restate them; a reference to a file it will not read carries nothing.
- **Tools.** The tool or family to use, the fallback, and a reminder to load any tool that loads on demand.
- **Ownership.** The files it may edit, disjoint from any parallel worker, and what it must leave untouched.
- **Stop condition.** When to stop and report instead of pushing on: scope exceeded, a check fails twice, or a
  decision belongs to you.
- **Result.** The report's exact shape and size, verified facts kept apart from inference. Large output goes to a
  file, and the report returns its path.

Keep the judgment calls and send the work. A brief that pastes the transcript hands over noise; a brief that asks the
receiver to decide what you should decide hands over your job.

Done when a cold reader could start without a question back, and the brief states outcome, context, ownership,
tools, stop condition, and result.

## Before Sending or Delivering

Do the cold read once more. Every term the receiver needs is defined or findable, every constraint has its reason
or is a guardrail, and the result is specified. For a prompt that has already failed in use, switch to
`prompt-debugging`: a rewrite without the failure preserved cannot show it fixed anything.
