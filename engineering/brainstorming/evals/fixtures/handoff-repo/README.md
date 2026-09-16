# Tool Library Handoff Fixture

This fixture is a disposable repository for the `handoff-fidelity` behavioral case. An evaluation runner copies the
directory to a fresh temporary workspace for every candidate and baseline run. It may write only
`docs/plans/tool-library-draft.md`, inspect that artifact and its execution trace, then delete the workspace.

The fixture remains unchanged. It gives the run a documented draft convention and a governing overview. The saved draft
cannot alter the source repository or another case's state.
