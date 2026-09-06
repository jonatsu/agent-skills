# The Walk Test

The behavioral acceptance gate for a context system: can a cold-started agent orient, act, and report using
only the files present? Structure checkers prove reachability; only this test measures whether the system
actually routes a working agent. Run it after initializing a layout, after any structural change, and
periodically against drift. Without it, every efficiency claim about the system is a hypothesis.

The name and core idea come from the Interpretable Context Methodology's walk test; this protocol adds the
metrics and the failure-mode mapping.

## Protocol

1. **Select tasks.** Three to five representative tasks that real work would bring: at least one
   navigation question ("where/how is X wired"), one change task ("add/modify X"), and one diagnosis task
   ("why does X fail"). Reuse the same task set across runs and clients so results stay comparable; version
   the set in the record.
2. **Cold-start per client.** For each target agent, start a fresh session with no carried context beyond
   what the client always loads. Give the task verbatim, with no hints about which documents exist.
3. **Observe, do not steer.** Let the agent run until it takes its first materially correct action (right
   file edited, right command proposed, right diagnosis stated) or clearly commits to a wrong path. Only
   intervene to stop, never to redirect.
4. **Score.** Record per task, per client:
   - **Tokens to first correct action** — the headline efficiency number.
   - **Wrong loads** — documents opened that a correct route would not touch.
   - **Missed loads** — documents the task needed that were never opened (judged against a pre-written
     answer key of which documents each task requires).
   - Verbatim notes on where the agent hesitated, grepped fruitlessly, or asked the user.
5. **Record.** Write a dated file in the repository's evaluations genre: task set version, client and model
   versions, the scores, and the defect list below. A walk test that ends only in conversation is unmeasured
   by the next session.

## Failure-Mode Mapping

Each observation indicts a specific layer; fix that layer, not the symptom:

| Observation                                                   | Defect                                                                | Fix at                              |
| ------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| Missed load: needed doc never found                           | Read-when line absent, topical, or missing the task's vocabulary      | Routing entry / doc header phrasing |
| Wrong load: irrelevant doc opened confidently                 | Trigger overlap or over-broad description                             | Trigger ownership dedup             |
| Fruitless grep: agent searched the right terms, found nothing | Search surface: paraphrased symptoms, missing literals                | The target document's wording       |
| Token blowout before first action                             | Floor too heavy, or hub index too large to hold                       | Floor accretion / shard the hub     |
| Agent acted on stale or wrong fact                            | Truth maintenance: missing stamp, unowned duplicate, unpruned finding | The fact's owning document          |
| Agent asked the user something the repo answers               | Fact exists but unreachable, or authority unclear                     | Routing or authority line           |
| Correct route on client A, failure on client B                | Reliance on a client capability without files fallback                | Cross-agent invariants              |

## Interpreting Results

- Compare against the previous record, not an absolute bar: the test's value is direction under change.
- One client's clean run does not generalize — client discovery and loading differ; every untested client is
  a coverage limit, not a supported claim.
- A structural change that improves no metric did not earn its maintenance cost; consider reverting it.
- Repetition costs real tokens: add repeat runs only when variance would change a decision, and note the
  spend in the record.
