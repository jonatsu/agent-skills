# Evaluation: Do `c-cpp-style`, `c-cpp-testing`, and `linux-kernel-development` Change What an Agent Writes?

Date: 2026-11-23. A short first behaviour check of the three new skills, one case each, until a dedicated evaluation
tool can run the full case sets in each skill's `evals/behavior.json`.

## Verdict

All three cases sat near the ceiling: the control arm already passed most outcomes, so the runs show little
difference between the arms. They do show that each skill leads the agent to its own rules without harming the
result.

- **`c-cpp-style`, Buildroot Makefile losing its flags: no difference.** Both arms explained that a variable on the
  make command line overrides `CFLAGS +=`, moved the project flags into a separate variable, kept `-std=gnu17`, and
  noted that GCC 15 defaults to C23. Both proved the fix with `make -n`. The skill arm placed its flags after
  `$(CFLAGS)`, as the skill says. The control placed them before, so that the caller's `-O` level wins. Both are
  sound, so the case's outcome was reworded to grade the separate variable, not its position.
- **`c-cpp-testing`, refusal tests for an OTP writer: no difference in outcome.** Both arms replaced the vendor
  library by link-time substitution with a stub that logs each `otp_write` call. Both asserted the exit status, the
  message, and the call count, added a passing control case, and ran ASan, UBSan, and Valgrind as separate builds
  with exit codes distinct from the tool's. Both checked their tests against deliberately broken copies of the tool.
  The skill arm added canary programs proving that each checker fails with its own exit code. Both arms allowed one
  `otp_write` call in the locked-slot case, because the vendor library may be what reports the lock. The case's
  outcome was reworded to accept that.
- **`linux-kernel-development`, reviewing a driver for a 6.6 tree: small gain.** Both arms found the wrong `.remove`
  callback for 6.6, the leak, `BUG_ON` on allocation failure, and the braces. Only the skill arm told the user to read
  the tree's own process documents and to build through the vendor's wrapper. It also gave the version facts
  correctly, while the control said `.remove_new` arrived in 6.2 instead of 6.3. The skill arm listed a check per
  change type, including the Kconfig option on and off and `CHECK_DTBS`.

## Method

Claude Code `general-purpose` subagents on Sonnet ran each case once per arm, six runs in all, in fresh contexts.
Each prompt was self-contained, with the Makefile or driver source inline and no fixture repository. The skill arm
was told to read the skill's `SKILL.md` at agent-skills `d6b7fa3` and the references that applied. The control arm
was told to load no skill and read no skill files. Runs could write and compile scratch code but change nothing
else. The outcomes graded are those in each skill's `evals/behavior.json` for the cases below.

| Skill                      | Case                             | Skill arm | Control arm                                   |
| -------------------------- | -------------------------------- | --------- | --------------------------------------------- |
| `c-cpp-style`              | `buildroot-makefile-loses-flags` | 4 of 4    | 4 of 4 with the reworded outcome              |
| `c-cpp-testing`            | `otp-refusal-tests`              | 4 of 4    | 4 of 4                                        |
| `linux-kernel-development` | `vendor-6-6-driver-review`       | 4 of 4    | 3 of 4; the tree's process documents not read |

## Limits

Each case ran once per arm on one model, so a single difference may be noise. The prompts were self-contained, so
no run had to find a fact in a real tree, which is where the skills' "read the tree first" rules matter most. The
second case of each skill was not run. Grading was by reading the answers, without a grading script. The cases are
well-known defects that the model already knows, which is the ceiling `README.md` warns about; the next round should
grade gaps the control leaves open, such as a kernel API that exists only in the tree in hand.
