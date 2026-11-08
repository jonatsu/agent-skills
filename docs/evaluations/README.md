# Evaluations

Each dated file records one evaluation of candidate or authored skills. skill-forge's
`references/full-evaluation.md` defines the method; this page covers running a behaviour evaluation here with
Claude Code subagents.

## Running a Behaviour Evaluation

Each case is a small standalone project with one defect, a README describing the intended behaviour, and a
grading script that builds the project and probes it from outside. Keep the grading script and any reference
fix outside the workspace the agent sees.

1. Prove the grader before any model run: every graded outcome fails on the unfixed fixture and passes on a
   reference fix.
2. Copy the fixture into one workspace per case, model, and arm under `/var/tmp`, which is disk-backed. Vendor
   or pre-fetch dependencies so builds run offline.
3. Dispatch one general-purpose subagent per workspace with the `model` set. The brief gives the workspace, the
   defect as a user would report it, offline build commands, a rule to keep every write and temporary file in
   the workspace, no questions, and a report of at most 250 words. The control arm is told not to read the
   skills under evaluation; the skill arm is told which `SKILL.md` files to read first.
4. Run at most three subagents at once, the harness limit, and grade each workspace as its run finishes.
5. Keep each run's transcript with its result, then read the code as well as the grades.
6. Delete every workspace when the record is written.

## Designing Cases That Separate the Arms

A case with one well-known defect measures what the model already knows: both arms pass, and only reading the
code shows the skill's effect. Grade the gaps a control leaves open instead, such as work that outlasts a
shutdown deadline, a child that escapes its process group, or input a lenient parser accepts. Grade behaviour,
never one convention where the skill allows alternatives, such as exiting 128 plus the signal number versus
re-raising the signal.
