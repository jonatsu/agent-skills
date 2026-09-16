# Attributions

## incremental-implementation

Influenced by the `incremental-implementation` skill in
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT License), read on 2026-09-14.

Reading that skill shaped this package's structure and framing: the increment cycle
(implement → verify → commit → advance), the "keep it compilable between slices," feature-flag, safe-default,
and rollback-friendliness rules, and the drift/red-flag section. The guidance here is expressed independently
from the execution-discipline domain rather than copied, adapted, or translated from the upstream text — no
wording or section structure was reproduced — so no upstream license file ships with this package. Slice
selection and task sizing are deliberately delegated to `implementation-planning` rather than reproduced from
the upstream, which covered them inline.
