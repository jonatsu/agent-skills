# Failure Diagnosis

These patterns came from controlled prompt and skill evaluations. Treat each cause as a hypothesis until the trace and
fixture support it.

| Observation                                                                                          | Likely layer               | Diagnostic action                                                  | Repair direction                                                                                      |
| ---------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| The agent cannot read the candidate outside its workspace.                                           | Harness permission         | Inspect the denial and client path policy.                         | Grant the narrow source read; do not edit the prompt.                                                 |
| The agent states every branch is blocked, then emits a conditional plan.                             | Under-compliance           | Confirm the prompt's stop condition is conditional or weak.        | Make the all-blocked branch terminal and retain an explicit independent-branch exception.             |
| An early confirmation is applied to decisions introduced later.                                      | Under-compliance           | Reconstruct the turn order and decision timestamps.                | Require confirmation after the complete synthesis; continue only on the next clear response.          |
| A small task becomes one unit per file or gains universal TDD.                                       | Fixture or over-compliance | Verify the repository and requested behavior exist in the fixture. | Supply real context; then narrow any workflow rule that still over-applies.                           |
| The agent asks for a value the case expected it to infer.                                            | Fixture ambiguity          | Identify whether the value changes public behavior.                | Put the value in the fixture or make user confirmation an expected outcome.                           |
| A validation command fails because its executable is absent.                                         | Harness dependency         | Run every advertised command during preflight.                     | Bundle a deterministic validator or declare and provision the dependency.                             |
| Turn 1 uses a confirmation intended for turn 2.                                                      | Fixture isolation          | List every readable workspace file before the run.                 | Keep future turns outside the workspace until sent.                                                   |
| A resumed session refuses an allowed write.                                                          | Harness continuation       | Compare first-turn and resume sandbox policy.                      | Restore narrow workspace-write through a supported client option; do not request unrestricted bypass. |
| The final answer looks correct but the trace shows retries, skipped context, or unauthorized writes. | Prompt or harness          | Grade trace and filesystem evidence separately.                    | Repair the layer that caused the hidden behavior; do not pass on final prose alone.                   |
| The output follows the rule exactly and is worse because of it.                                      | Over-compliance            | Name the obeyed rule and the displaced user intent.                | Remove, narrow, or add an escape hatch; rewording alone is insufficient.                              |

## Common Prompt-Level Hypotheses

- **Prompt delivery:** the intended text never loaded, was truncated, or lost precedence.
- **Buried obligation:** the rule is present but loses to nearer or more specific text.
- **Competing instructions:** both actions appear authorized and the model selects one unpredictably.
- **Missing terminal branch:** the model recognizes a blocker but no instruction tells it to stop.
- **Temporal ambiguity:** confirmation or state is not tied to the decisions it covers.
- **Missing fallback:** the model must choose between invention and an unhelpful stop.
- **Overbroad default:** a safety or quality workflow consumes cases that need a lighter path.
- **Wrong authority:** the prompt attempts to grant permissions or decide product behavior owned elsewhere.

Change one mechanism per hypothesis. If the rerun still fails, return to classification rather than accumulating more
instructions.
