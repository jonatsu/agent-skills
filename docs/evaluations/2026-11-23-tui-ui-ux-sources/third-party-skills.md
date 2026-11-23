# TUI skill candidates: research notes (read 2026-11-23)

Question: which published Agent Skills cover TUI design, and can any be adopted or adapted into an MIT repository?
Success criterion: each named candidate read at a pinned commit with its licence from LICENSE; wider search done; top
eight reported.

Route notes: `gh` was denied in this lane (read-only Bash), so GitHub data came from `api.github.com` and
`raw.githubusercontent.com` through docs-mcp `fetch_url`. `gh search code` was unavailable (code search needs auth);
`gh_grep` with `path: SKILL.md` stood in. The proxy dropped mid-run, so some checks used WebFetch.

## Reading depth (honest limits)

- hyperskills `tui-design`: SKILL.md, LICENSE and all three references read in full.
- wimpysworld `tui-design`: SKILL.md, header.toml, LICENSE read in full; references read as outlines plus the
  accessibility, responsive, reserved-keys, mouse, confirmation and OSC sections. Not read line by line: ecosystem-\*.md,
  cli-basics.md, exemplar-apps.md.
- gfargo (upstream of wimpysworld): SKILL.md in full; terminal-protocols.md in full; visual-patterns (accessibility, responsive,
  clutter audit, states) and interaction-patterns (reserved keys, quit ladder, stolen keys, focus, live data, mouse,
  confirmation, pitfalls) in full; ecosystem-\*, cli-basics, exemplar-apps by outline only.
- pageton: SKILL.md, terminal-compatibility.md, stability-and-robustness.md in full; other references by file list only.
- Others: ratacat, TheDecipherist, existential-birds SKILL.md in full; castle-x, podo, msmps, NVIDIA, warp, dagger,
  hatchet, loomkin, buildhaus, egregore, pymc, qf-studio: first lines, size, licence only.

## Candidate 1: hyperb1iss/hyperskills, skills/tui-design

- Repo <https://github.com/hyperb1iss/hyperskills>; path `skills/tui-design/` (SKILL.md 13.8 KB; references/app-patterns.md,
  evidence.md, visual-catalog.md).
- Pinned commit 8fe9ceb124c3aeaf5050b9ddcc5cd14f8795151b (repo HEAD, 2026-11-21T01:08:12Z). Last commit touching the
  skill path: bf6f91770d7d70367873b5a894971a29a3a9721f, 2026-10-27T22:24:43Z.
- Licence (LICENSE, repo root only, no per-directory licence): MIT, "Copyright (c) 2025 Stefanie Jane". Claimed MIT: confirmed.
- Frontmatter: name, description only. Valid.
- Scope: design and review guidance, framework-neutral (names Ratatui, Crossterm, Ink, Textual, Bubble Tea in passing).
  No implementation recipes, no per-framework API, no test harness. Covers layout choice, input and focus, state and async,
  terminal capability policy, visual hierarchy and accessibility, rendering and lifecycle, verification, anti-patterns.
- Rules worth taking (F = fact claim, O = opinion/convention):
  - F: A non-empty `NO_COLOR` must be resolved before colour detection; disabling colour need not disable bold or underline.
  - F: Terminal queries share the input stream with keystrokes; one parser correlates replies and waiting is bounded.
  - F: Do not mix crossterm `EventStream` with `read`/`poll` (one input owner). (not independently verified here)
  - F: Ctrl+I equals Tab and Ctrl+M equals Enter in the legacy encoding; negotiate enhanced keyboard protocols, keep fallbacks.
  - F: Raw mode disables the terminal's signal handling for Ctrl+C and Ctrl+Z; implement them deliberately.
  - F: Pasted newlines must not submit; treat bracketed paste as a text event.
  - F: Control sequences in untrusted strings (filenames, logs) must be escaped before raw output (cursor moves, OSC).
  - F: SIGKILL cannot run cleanup; restore raw mode, alt screen, cursor, mouse, paste, keyboard state on every other path.
  - O: Track selection by stable identity, not row index; tag async results with request identity and drop stale ones.
  - O: Separate event, update, effect and render; render never starts I/O.
  - O: Follow mode is explicit; scrolling back stops auto-follow; a paused view shows a pending count.
  - O: Do not claim formal accessibility compliance from a palette; WCAG 4.5:1 is a target, not a guarantee, in a terminal.
  - O: Test one real PTY session; snapshots do not exercise terminal modes.
- Defects / gaps:
  - No screen-reader guidance beyond "provide a plain or linear presentation" (no append-do-not-repaint, no opt-in rule).
  - No resize mechanics (no SIGWINCH, no breakpoint ladder, no too-small state design), only "test narrow, ordinary, wide".
  - No multiplexer or SSH environment table; no escape or quit ladder; no reserved-key table.
  - Embeds the maintainer's personal "SilkCircuit Neon" palette as a named identity; the skill says to follow project identity.
  - visual-catalog.md is glyph reference (box drawing, braille, Nerd Font table), large and cheap to rewrite.
  - Contains a graphviz `dot` block (renders nowhere in agents; harmless).
  - Lineage: widely copied. `pedronauck/skills` `skills/curated/tui-design/SKILL.md` is byte-identical to this commit's
    file (compared). Older 19,989-byte versions with the same description sit in `buildhaus/workbench` and
    `pass-agent/loomkin`.
- Adaptation: MIT, adaptable with the copyright notice kept. Ideas are separable; the evidence.md citation list is reusable.

## Candidate 2: wimpysworld/nix-config, home-manager/\_mixins/agentic/assistants/skills/tui-design

- Repo <https://github.com/wimpysworld/nix-config>. Pinned commit 71b8078e28f7e114f1785372f80b6a00b2dc5020 (HEAD,
  2026-11-23T19:35:09Z).
- Licence: repo-root LICENSE is Blue Oak Model License 1.0.0 (confirmed). The skill directory has its own `LICENSE`:
  MIT, "Copyright (c) 2026 gfargo", and `header.toml` says `license = "MIT"`. So the "claimed BlueOak" is true for the
  repository but NOT for this skill: the skill is MIT and is a derivative of gfargo/tui-design-skill.
- Provenance (header.toml): `upstream = https://github.com/gfargo/tui-design-skill`, `revision = f8eab1afba9f545fbb3969d01ba54e8f6aceac4d`,
  version 1.7.2, `source = plugins/tui-design/skills/tui-design`. local-changes: frontmatter mapped to header.toml,
  "adapted ... to house style", references got contents lists, vhs-cli-demos made optional.
- Spec shape: SKILL.md has no frontmatter in the repository; the Nix build generates it from `header.toml`
  (name, description, license, metadata.version/upstream/revision/source/local-changes; codex.interface separately).
  Not an installable SKILL.md package as published.
- Scope: design, build, review of TUIs and CLIs; Go, Rust, Python, TypeScript ecosystems; 8 references (~170 KB).
- Rules worth taking: same as gfargo's SKILL.md (it is a condensed rewrite): classify product by output contract first
  (one-shot, summon-choose-exit, full-screen); clutter audit; test 80x24 and 60-column floor; prioritised review order
  (needs full-screen? exit path leaves modes on? blocking/resize/width? discoverability? clutter? floor? streams/NO_COLOR?
  test layers?). Reserved-keys table notes raw mode.
- Defects versus current upstream:
  - Snapshot of v1.7.2; upstream is at 1.9.0 and has since added terminal-protocols.md, a screen-reader section,
    the quit ladder and keys-stolen-by-multiplexers table. The wimpysworld copy has none of these.
  - Its "Accessibility" is a colour-blindness note ("About 8% of males have red-green colour vision deficiency");
    no screen-reader guidance at all in references (grep: only Huh `WithAccessible` and Ink aria props).
  - Reserved-keys text says Ctrl+S binding "requires flow control disablement, such as stty -ixon", which upstream later
    corrected (raw mode already clears IXON; flow control only matters in cooked mode). Treat wimpysworld's wording as stale.
  - Includes an unverified dated claim ("Windows Terminal added a similar focus check in February 2026").
  - Frameworks are hard-wired into the routing table (Go/Rust/Python/TS).
- Adaptation: MIT via gfargo's copyright, plus house-style rewrite by the repo owner (header.toml licenses it MIT).
  Better to take from gfargo directly than from this stale derivative.

## Additional discovered candidate (strongest): gfargo/tui-design-skill

- Repo <https://github.com/gfargo/tui-design-skill>; skill at `plugins/tui-design/skills/tui-design/`.
- Pinned commit 716633c308ac847f96741fac37c5c11bb234df8e (HEAD, 2026-11-23T20:08:48Z). Plugin version 1.9.0.
- Licence: LICENSE MIT, "Copyright (c) 2026 gfargo".
- Frontmatter: name, description only (plus agents/openai.yaml for Codex display fields). Valid.
- Scope: SKILL.md 12.6 KB routes to 9 references (~295 KB): ecosystem-go/rust/python/typescript, cli-basics,
  visual-patterns, interaction-patterns, terminal-protocols, exemplar-apps. Design, build, review, testing; Bubble Tea,
  Ratatui, Textual, Ink, OpenTUI.
- Evidence of engineering: CI builds and tests the reference code samples (`.github/workflows/samples.yml`, tests/samples/{go,rust,python,typescript});
  `validate-release.sh` fails on a broken `file.md -> *Heading*` pointer; weekly reference-freshness audit; evals with graded
  runs (CHANGELOG: Claude 77.2% -> 94.4% of assertions, Codex 63.5% -> 87.7%; design-review sets show least gain; grader
  kappa 0.83); Claude plugin validate in CI. Self-reported, not re-run by me.
- Rules worth taking:
  - F: Raw mode delivers Ctrl+C/Ctrl+Z/Ctrl+S as ordinary keys; no SIGINT, SIGTSTP or XOFF unless the app produces it.
  - F: tmux default `escape-time` dropped from 500 ms to 10 ms in 3.5. VERIFIED against tmux CHANGES ("CHANGES FROM 3.4
    TO 3.5": "Reduce default escape-time to 10 milliseconds").
  - F: Alacritty supports the kitty keyboard protocol (0.13.0), CSI 2026 synchronized updates and OSC 52 writes (paste-back
    disabled by default). VERIFIED against Alacritty CHANGELOG.
  - F: Windows has no SIGWINCH/SIGTSTP/SIGCONT; resize arrives as console events. (consistent with pageton's note)
  - F: Kitty-keyboard and extended keys: Shift+Enter, Ctrl+Enter, Ctrl+Tab are accelerators only; keep a legacy binding.
  - F: Terminal capability queries (OSC 11, DA1, DECRQM) need a bounded wait and a rendered default; SSH makes each one
    a round trip.
  - F: Always send synchronized-output end sequence, error paths included.
  - O: Esc quit ladder: cancel, close, clear, go back, then nothing; Esc never quits. q goes back or quits at root.
    Ctrl+C cancels then quits.
  - O: Plain-mode contract: reaches every action, results to stdout, explicit opt-in (flag/env/config), auto when stdout
    is not a TTY; do not rely on screen-reader detection.
  - O: Screen-reader rules (append do not repaint; flatten tables; number choices; label lines; keep cursor on focus).
    Cited to CHI '21 study; not checked by me.
  - O: Clutter audit: border-nesting depth, signals per state (budget one colour cue plus one non-colour cue), always-on
    markers, chrome-to-data ratio.
  - O: Floor test: say what happens at 80x24, 60 columns and below the declared minimum; every multi-column design needs
    a single-pane fallback.
  - O: States table: initial, loading, empty, partial, success, error, stale, too small, each with next action.
  - O: Live data: stable-ID selection, nearest-neighbour on removal, no scroll under cursor, freeze key.
- Defects / gaps:
  - Size: 295 KB across references; a new skill cannot copy it whole. Much is ecosystem API detail that ages (pinned
    framework versions).
  - Several fast-moving claims (tmux 3.7/3.8, kitty 0.38.1, Windows Terminal 1.25) I could not check; they sit in tables
    that need dated pins.
  - cli-basics.md overlaps the sibling `cli-ui-ux` skill.
  - Evals are the author's own; grader is a model.
- Adaptation: MIT, adaptable with attribution. The plain ideas are separable; the repository's own AGENTS.md rule
  (`file.md -> *Heading*` pointers checked by script) is a pattern this repo already has an analogue for.

## Additional discovered candidate: pageton/tui-design-skill

- Repo <https://github.com/pageton/tui-design-skill>; `skills/tui-design/` (SKILL.md 27 KB, 14 references, 4 framework docs,
  6 screen patterns, runnable `projects/dbview-go` and `projects/log-monitor-rust`, 4 starter templates).
- Pinned commit 03e76c06caa83f5c1c606cf28d46b92f6e129ef0 (HEAD; commit feed updated 2026-11-15T10:19:44Z).
- Licence: LICENSE MIT, "Copyright (c) 2026 pageton".
- Frontmatter: name, description only. Independent of gfargo/hyperskills (different text and structure).
- Scope: design, build, review, convert CLI to TUI, testing, Unicode and RTL/Arabic, terminal compatibility, stability.
  Bubble Tea, Textual, Ratatui, Ink.
- Rules worth taking: restore as ordered checklist (leave alt screen, show cursor, disable raw mode, disable
  mouse/paste, flush, then print errors), idempotent, panic hook first (O/F); one in-flight request per resource with
  generation counter and timeout; bounded channel and visible dropped count; errors are overlays not view replacements;
  fail closed before entering full screen; second Ctrl+C force-quits; RTL: never reverse strings, emulator decides (O).
- Defects (checked):
  - Capability matrix marks Alacritty as no kitty keyboard, no OSC 52, no synchronized output. Alacritty CHANGELOG
    contradicts all three (0.13.0 kitty keyboard; CSI 2026 sync; OSC 52 with paste disabled by default). The matrix is
    wrong for one of its eight columns.
  - "Wrap frames in 2026 unconditionally; harmless no-op" conflicts with gfargo/hyperskills (query first; an unpaired
    begin sticks).
  - "NO_COLOR set -> mono" omits the non-empty rule (hyperskills and no-color.org say non-empty).
  - Screen readers: only "document the limitation"; weaker than gfargo.
  - Persona prose ("expert terminal product designer ... premium product") and "Every TUI ships a README.md" are scope
    creep for a design skill.
  - 27 KB SKILL.md exceeds a lean entrypoint; installation and Nix sections are off-topic.
  - Debounce resize ~50 ms as default (gfargo: coalesce only when layout is expensive).
- Adaptation: MIT, with attribution. Use for the stability and testing ideas, not the capability matrix.

## Other discovered skills (ranked by relevance; fewer details)

3. TheDecipherist/claude-code-mastery-project-starter-kit `.claude/skills/tui-builder/SKILL.md`, commit 61fbb99d (feed
   updated 2026-06-29), MIT. Ink-only resize rules: alt screen, register clear handler before `render()`, width as React
   state. Frontmatter has `when_to_use`, which is not an Agent Skills spec field. Claims `process.once('exit')` restores
   "even on crash" (does not cover SIGINT/SIGTERM). Ideas only on resize ordering; framework-locked.
4. existential-birds/beagle `plugins/beagle-go/skills/review-tui/SKILL.md`, commit d1a74899 (feed updated 2026-08-10),
   Apache-2.0. Bubble Tea review workflow with gates and severity-tiered output; links to sibling skills that must be
   loaded; `disable-model-invocation: true` (a Claude Code field, not spec). Go-only. Ideas only; Apache-2.0 is
   adaptable with notices.
5. msmps/opentui-skill `skill/opentui/SKILL.md`, commit 0d61d6d8 (feed updated 2026-08-27), MIT. OpenTUI framework
   usage; not design.
6. castle-x/skills-x `skills/tui-design/SKILL.md`, commit 3fb98d42, MIT. A single product's page-layout spec
   (four-section layout), 20 KB; generic-looking but project-specific.
7. ratacat/claude-skills `skills/terminal-ui/SKILL.md`, commit d4b471d0, no LICENSE found (raw fetch empty).
   Aesthetic-only ("BOLD aesthetic", ASCII art, animation); no resize, accessibility, lifecycle; opposite of what we
   want. Ideas only, none worth taking.
8. warpdotdev/warp `.agents/skills/tui-ui-guidelines` and siblings, AGPL-3.0: product-specific; ideas only. Also seen:
   NVIDIA/OpenShell `tui-development` (Apache-2.0, ratatui, product-specific), dagger `tui-console`/`tui-qa`
   (Apache-2.0, drive Dagger's TUI), hatchet `build-tui-view` (MIT, product-specific), gitbutler `tui-tests`, fedexist
   `testing-ratatui-tuis`, microsoft/inshellisense `tui-test`, google-gemini `tui-tester` (testing skills for specific
   apps).

- Catalogue copies, no new content: `pedronauck/skills` (identical to hyperskills), `buildhaus/workbench` and
  `pass-agent/loomkin` (older hyperskills copy), `podo/design-agent-skills` (a stub pointing at gfargo; independent sign
  gfargo is the recognised upstream).
- Marketplaces: skills.sh lists gfargo, hyperskills copies, pageton, podo, ratacat; anthropics/skills has 19 folders,
  none about terminals (checked: no TUI entry; includes `frontend-design`, which ratacat's text mirrors in style).

## Hypotheses and outcome

- H1 "a single published skill covers TUI design well enough to adopt whole": refuted. gfargo is the broadest and best
  engineered but is 295 KB and bundles ecosystem API detail and CLI material that `cli-ui-ux` should own.
- H2 "wimpysworld is an independent BlueOak skill": refuted. It is an MIT derivative of gfargo v1.7.2; BlueOak applies
  to the repo root only.
- H3 "hyperskills and gfargo are the same lineage": refuted by content; hyperskills is a separate, shorter,
  state-and-lifecycle-focused skill.
- Confidence: licence facts high (read from LICENSE files). Provenance of wimpysworld high (header.toml). Content
  quality of gfargo/hyperskills medium-high (read key sections; two claims cross-checked against primary sources, the
  rest not). Wide-search completeness medium (gh_grep indexes only some repos; code search via `gh` not run).

## Open questions

- gfargo ecosystem-\*.md, cli-basics.md, exemplar-apps.md and the rest of visual/interaction patterns not read line by line.
- tmux 3.6 to 3.8, kitty 0.38.1, Windows Terminal 1.23/1.25 version claims in gfargo's terminal-protocols.md unchecked.
- NO_COLOR non-empty rule and Crossterm EventStream rule asserted by hyperskills unchecked by me.
- hyperskills provenance (whether derived from another skill) not examined.
