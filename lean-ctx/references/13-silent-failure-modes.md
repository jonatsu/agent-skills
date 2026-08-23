# Silent failure modes

Each item below returns a plausible-looking success. Treat the result as wrong,
not as a finding. Observed on lean-ctx 3.9.x.

**Verification status.** Re-exercised against a running 3.9.18 on 2026-08-23:
the search result cap (reported "20 matches" where the true count was 22) and
the absence of brace expansion in `ctx_glob` (`**/*.{md,json}` matched none of
three present files, with no error). The `outline` entry was corrected in the
same pass — the fallback is real, the warning is not. Every other entry stands
on its original measurement and has not been re-run. When lean-ctx updates,
re-run the two confirmed probes first: they are cheap, and if either has changed
the rest of this file is suspect.

## Contents

- Reads that omit
- Redaction rewrites what you read
- Searches and globs that truncate
- Caches that answer for a stale tree
- Shell calls that mislead
- Arguments that are silently reinterpreted
- Retrieving what was archived

## Reads that omit

- **Compression can drop syntax.** A compressed read has been observed omitting
  an `else`, presenting an inverted control flow as if it were the file. NEVER
  assert branch structure, guard conditions, or control flow from a compressed
  mode. Re-read with `full`, `raw`, or a line slice first.
- **`ctx_read` degrades under context pressure**, stepping `full` → `map` →
  `signatures`. It warns, but the warning is easy to skim past. `raw` and
  `anchored` are exempt — ask for those when verbatim bytes matter.
- **`mode="map"` can be overridden to `full` on a large file**, announced as
  `[mode overridden: map -> full, reason=bounce-prevention]`, and the resulting
  full read is then truncated. The orientation call costs thousands of tokens
  and returns no map. Measured normal at ~18 KB / 294 lines and overridden at
  ~51 KB / 902 lines; the threshold sits between. On a large file, reach for
  `ctx_search` or `start_line`+`limit` instead.
- **`mode="lines:N-M"` on a file already read in full can collapse to an
  `[unchanged …]` stub**, returning no window at all. Use `start_line`+`limit`,
  or `fresh=true`.
- **No mode recovers everything.** Invalid UTF-8 is lossily replaced at read
  time and redacted content is removed before any mode sees it — `raw` included.
  Use the host's native read tool for those two.
- **`outline` is not a mode.** It falls back to a full read — so an orientation
  call silently costs a whole file. Re-exercised 2026-08-23 on 3.9.18: the
  fallback happened, but **no warning was emitted**, so do not expect one to
  tell you. Use `signatures` or `map`.
- **`raw` truncates at a fixed output cap**, so a mid-size file comes back partial
  even though `raw` promises exact bytes. The cut is labelled
  (`[… truncated at ~N of M tokens …]`) and the notice suggests a `lines=`
  parameter — pass `start_line`+`limit` and page instead. The cap is on output,
  not a fraction of the file: two `raw` reads of one 426-line file both stopped at
  ~4182 tokens, one reading a 7479-token whole and one a 4660-token tail.
- **Read-dedup is cross-agent, so a file a SUBAGENT read comes back as a stub in
  your own context.** The reply is `[unchanged NL · lean-ctx read-dedup]` plus
  "already in this conversation above" — but it is not, and no content is
  returned. This intercepts the host's NATIVE read tool too, not only `ctx_read`.
  Recover with `fresh=true`, or by copying the file into the project and reading
  the copy. NEVER re-issue the identical read.

## Redaction rewrites what you read

Secret redaction runs on the way out of every `ctx_*` read and shell call, and
`mode="raw"` does NOT bypass it. It fires on ordinary text that merely looks
credential-shaped, and the substitution is not a clean swap: an
`Authorization: Bearer <value> and …` line came back as
`Authorization: Bearer [REDACTED:Authorization header] token] and …`, injecting a
stray ` token]` that was never in the file. The altered span can therefore be
longer than the marker and can carry invented text.

**The transform is display-layer, not a write.** After two `ctx_patch` edits to
unrelated lines of a file containing redaction-triggering text, the file on disk
held zero markers, every credential span was intact, and the byte count moved by
exactly the size of the intended edits.

**On-disk corruption comes from ROUND-TRIPPING.** Content obtained through a
`ctx_*` read and then written back by any tool persists the marker, and the
original is gone. NEVER reconstruct or re-emit a file from a `ctx_*` read of it.
Patch it in place, or re-read it with the host's native read tool first.

**Seeing a marker is not evidence the file is damaged.** This is the most
expensive part of the failure mode, because the natural reading of invented text
in a read is "something corrupted my file", and investigating that burns far more
time than the redaction cost. Diagnose in this order: re-read the span with the
host's native read tool, and if it is clean, the marker was a display artifact and
there is nothing to fix. Only if the native read also shows the marker has
anything been written to disk. NEVER run that check through `ctx_shell` — it
redacts its own stdout with the same heuristic and will re-confirm a phantom.

**Absence of a marker proves nothing.** The heuristic is context-dependent:
`TOKEN=old` and a bare 13-digit epoch passed through untouched in one file while
comparable shapes are redacted elsewhere. When the exact bytes matter, verify with
a native read — never with `ctx_shell`, which redacts its own stdout and so cannot
confirm itself.

## Searches and globs that truncate

- **`ctx_search` stops at `max_results` (default 20) and prints "N matches" with
  no truncation marker.** "20 matches" means "at least 20". `ctx_glob` does the
  same at 200. NEVER read a capped count as a complete inventory.
- **`ctx_glob` has no brace expansion.** `**/*.{rs,ts}` matches nothing and does
  not error. Issue one glob per extension. `ctx_search(include=…)` does expand
  braces.
- **`ctx_search` also under-reports from a STALE INDEX**, which is a separate
  failure from the result cap. It searches its own index, which lags recently
  created or edited files: a regex search reported "20 matches in 6 files" while
  omitting ten further matches in three files that a plain recursive grep found.
  A count under the cap is therefore not proof of completeness either.
- **`ctx_shell` output compression drops whole lines with no marker.** A
  `git status --short` returned twelve entries where the raw run returned
  thirteen, and a `jq` query listing names returned twelve where the real answer
  was twenty-nine. The clipped list looks complete and plausible. Defend against
  it by asking for the count in the same call (`| wc -l`, `jq '… | length'`) and
  checking it against the lines you can actually see — a count is one token and it
  is the only thing that makes clipping visible. Pass `raw` whenever completeness
  is the point rather than the gist.
- **`ctx_git_read`'s grep is `git grep` BRE and always case-insensitive.**
  Alternation, `+`, and `?` are literal characters there, so `foo|bar` searches
  for the string `foo|bar` and finds nothing. Character classes and anchors do
  work. Every failure — bad pattern, missing path — is reported identically as
  `No matches for '<query>'` with stderr discarded, so a broken query is
  indistinguishable from a real absence. Search one simple term per call, and
  confirm any absence a second way. Output caps at 200 lines with no notice.

## Caches that answer for a stale tree

- **A repeated identical `ctx_search` returns a cache stub instead of results**,
  and its key uses the ROOT directory's mtime — which does not change when a
  nested file is edited. Edit a file three levels down, re-run the search, and
  get the pre-edit answer. Vary the pattern or `max_results` to bust it.
- **A partially-repeated `ctx_search` returns only the NEW matches**, keyed on
  the pattern alone — so the same pattern run against a different directory is
  diffed against the previous directory's results. This one is labelled: read
  the header before trusting the count.

## Shell calls that mislead

- **`ctx_shell` detaches any command still running at the foreground cap** (~110s)
  and returns a job id immediately. A `sleep 300` used as "wait for the build"
  therefore returns at once, so a poll-after-sleep loop fires far faster than real
  time. The symptom reads as a hang: a background job polled ten times still says
  `running`. Check elapsed time against a clock — a file mtime versus `date` — not
  against how many polls you have made. To actually block, keep the sleep under
  the cap and do not request background execution.
- **`ctx_shell` runs inside the long-lived MCP server process and keeps the
  environment that process was launched with.** A variable exported into a shell
  profile mid-session is invisible to it, and any subprocess it spawns inherits
  the stale environment too, so an env-dependent check can report a false negative
  while the change is correct. Variables that existed before the host launched are
  visible normally. Verify env-sensitive work with the host's native shell.

## Arguments that are silently reinterpreted

- **`ctx_search` with an unknown `action` does not error** — it falls back to
  regex. If `pattern` is missing, the first unrecognized string argument becomes
  the pattern, so a typo'd key silently becomes the search string.
- **`ctx_tree` silently caps `depth` at 10.**
- **`ctx_shell`'s `cwd` persists across calls.** After one call with a `cwd`
  outside the project, every later call keeps running there until `cwd` is
  passed again; relative-path commands then run in the wrong tree and look like
  "the tools stopped working". Recovery is a single
  `ctx_shell(cwd=<project root>)`. This is distinct from project-root capture
  (see `12-troubleshooting.md`), which that same call does NOT fix.
- **A `cwd` the path jail rejects still runs the command in the captured root**,
  appending a `[cwd: requested path rejected by project-root jail …]` line to
  the output. Read the tail before trusting the result.

## Retrieving what was archived

`ctx_shell`, `ctx_execute`, `ctx_search`, and `ctx_tree` archive their output
past a token threshold, leaving a `--- retrieve full output ---` marker naming
an id. Retrieve it with `ctx_expand(id=…)` rather than re-running the command:
re-running pays for the work twice and, for searches, can return a cache stub
instead of the results. `ctx_read` is never archived — an explicit read always
returns content. Archives expire, and anything over 10 MB is truncated at store
time.
