# TUI primary sources (research notes)

Read date: 2026-11-23. Status key: V = verified (read in the cited source), I = inferred (my reading, not stated by source).
Licence column: as stated by the source. All pins are release tags, commit-free page versions, or the page's own date.

## 1. Terminal mechanics

Pins:

- xterm ctlseqs: <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>, "updated for XTerm Patch #411 (2026/08/23)".
  Licence: no licence stated on the page.
- Kitty keyboard protocol: <https://sw.kovidgoyal.net/kitty/keyboard-protocol/> (kitty docs, "Added in version 0.20.0";
  kitty latest release v0.51.1 on 2026-11-23). Kitty source is GPL-3.0 (not re-verified this session: I).
- Synchronized output spec: <https://github.com/contour-terminal/vt-extensions/blob/HEAD/synchronized-output.md> (read at
  HEAD 2026-11-23; no commit SHA pinned). Licence: not read.
- ncurses man pages: <https://invisible-island.net/ncurses/man/> (ncurses 6.6, patch 20261010; curs_initscr/curs_getch
  page dates 2025-08-23 to 2026-09-19). ncurses licence: MIT-style X11 licence (I, not re-read this session).
- tmux manual: <https://raw.githubusercontent.com/tmux/tmux/3.8/tmux.1> (tag 3.8, 2026-10-08). tmux is ISC licence (I).
- termstandard colors: <https://github.com/termstandard/colors> README at HEAD (2026-11-23). No licence found in file.
- termios(3), signal(7): <https://man7.org/linux/man-pages/man3/termios.3.html> and man7/signal.7.html (man-pages project,
  licences per page, not read).

Facts:

01. Alternate screen: mode 1049 = save cursor (DECSC), switch to alternate buffer and clear it; reset = back to normal
    buffer and restore cursor. ctlseqs says "Use this with terminfo-based applications rather than the 47 mode". Can be
    disabled by the `titeInhibit` xterm resource (users may have the alt screen switched off). V (ctlseqs, Patch #411).
02. Bracketed paste = mode 2004; terminal sends `ESC [ 200 ~` before and `ESC [ 201 ~` after pasted text. V (ctlseqs).
03. Mouse: 1000 = press/release, 1002 = cell-motion (button-event), 1003 = any-event (all motion); 1004 =
    FocusIn/FocusOut events; 1006 = SGR encoding (`CSI < b;x;y M|m`, `m` is release, so which button was released is
    known); 1005 UTF-8 and 1006 exist because the original X10 encoding caps coordinates at 223 (255-32); UTF-8 mode
    raises it to 2015. V (ctlseqs).
04. Mode 2026 (synchronized output) is NOT in xterm ctlseqs Patch #411 (searched; no hit). Its spec lives in contour
    vt-extensions: enable `CSI ? 2026 h`, end `CSI ? 2026 l`; probe support with DECRQM `CSI ? 2026 $ p`; reply
    `CSI ? 2026 ; Ps $ y` where 0 or no reply = unsupported, 1 or 2 = supported, 3 = undefined, 4 = not supported. The
    spec says there is "no real consensus" on a timeout. Adoption table lists VTE/gnome-terminal as "not yet" and
    Konsole/st/urxvt as unknown (table is the spec author's, could be stale). V (spec text). tmux 3.8 has a
    terminal-feature `sync` ("Supports synchronized updates") and 3.7a/3.7b CHANGES fix redraw on end of synchronized
    update. V (tmux.1, CHANGES at 3.8).
05. Kitty keyboard protocol: legacy mode cannot tell Esc from the start of an escape sequence ("fragile timing related
    hacks"); ctrl+i is the same as Tab, ctrl+m the same as Enter, ctrl+r the same as ctrl+shift+r. Fix is opt-in
    progressive enhancement. V (kitty docs).
    - Quickstart: push `CSI > 1 u` at start (on entering the alternate screen if you use it), pop `CSI < u` at exit just
      before leaving the alternate screen. Main and alternate screens keep separate flag stacks. Query flags with
      `CSI ? u`; detect support by sending `CSI ? u` followed by DA1 (`CSI c`) and checking which reply arrives. V.
    - Flag bits: 1 disambiguate, 2 event types (press/repeat/release), 4 alternate keys, 8 all keys as escape codes, 16
      associated text. V.
    - With flag 1, ctrl+c no longer raises SIGINT: it arrives as `CSI 99;5u`. Enter, Tab and Backspace keep legacy bytes
      so the user can type `reset` after a crash that left the mode on. V.
    - Implemented by kitty, alacritty, foot, ghostty, iTerm2, WezTerm, Windows Terminal (listed), plus libraries
      crossterm, Textual, Bubble Tea, notcurses, vaxis, tcell (listed in the doc). The doc does not list Terminal.app,
      GNOME Terminal/VTE, Konsole, xterm: I (absence from list).
06. Raw vs cooked: `cfmakeraw()` per termios(3) clears IGNBRK, BRKINT, PARMRK, ISTRIP, INLCR, IGNCR, ICRNL, IXON; clears
    OPOST; clears ECHO, ECHONL, ICANON, ISIG, IEXTEN; sets CS8. So in raw mode Ctrl+C, Ctrl+Z, Ctrl+S/Q and Ctrl+V arrive
    as bytes, not signals (ISIG, IXON, IEXTEN cleared). V (termios.3, man7.org). ncurses `cbreak()` keeps ISIG; `raw()`
    does not (curs_inopts(3x) page read for names only; the ISIG difference is I from the standard curses meaning).
07. ncurses signal handling (curs_initscr(3x), ncurses 6.6): installs handlers on first `initscr`/`newterm`; SIGINT and
    SIGTERM handler "attempts to clean up the screen on exit" with documented async-signal-safety limitations (walks
    SCREEN list, calls endwin which uses stdio); SIGTSTP handler flushes input, repaints and re-saves shell modes on
    resume; SIGWINCH sets a flag so `wgetch` returns `KEY_RESIZE` (even if keypad mode is off) and ncurses calls
    `resizeterm` to update `LINES`/`COLS`. Apps that want their own handlers should install them AFTER initscr. V.
08. Esc timing in curses: `ESCDELAY` (variable or env) is how long ncurses waits after ESC to tell a lone Esc from a
    function-key sequence; users can see "a pause or hang after pressing the escape key"; value is milliseconds.
    `notimeout` makes the delay infinite. V (curs_getch, curs_variables).
09. tmux 3.8: default prefix is `C-b` ("by default"), `C-b C-b` sends the prefix through, `C-b C-z` suspends the client;
    option `escape-time` = milliseconds tmux waits after Esc to decide if it starts a function/meta sequence;
    `extended-keys` and `extended-keys-format` (`csi-u` or `xterm`) control modified-key reporting; `focus-events` option
    passes focus events through; terminal-features include `extkeys`, `focus`, `mouse`, `RGB`, `sync`. V (tmux.1 at tag
    3.8). Screen's default Ctrl+A: not re-read this session (I).
10. Truecolor detection: `COLORTERM=truecolor` (or `24bit`) is the de-facto signal; terminfo `RGB` capability since
    ncurses 6.0-20180121; the colors README warns that env vars are not forwarded over sudo/ssh by default. V
    (termstandard/colors README, HEAD). It is a community document, not a standards body.
11. ECMA-48 / ECMA-35: ctlseqs quotes ECMA-48 saying 7-bit and 8-bit control coding are equivalent; the standard itself
    not fetched. Terminal-wg specs site (gitlab.freedesktop.org/terminal-wg/specifications) is behind Anubis for
    docs-mcp (not read).

## 2. Framework guidance

### ratatui (Rust)

Pin: crate ratatui 0.30.2 (crates.io, updated 2026-06-19; git tag `ratatui-v0.30.2`). Licence: MIT (LICENSE at tag,
"Copyright (c) 2016-2022 Florian Dehau, 2023-... The Ratatui Developers"). Docs site <https://ratatui.rs> (pages read
2026-11-23; source repo ratatui/ratatui-website, licence not read).

- `ratatui::run(|terminal| ...)`, `init()`/`restore()` : init enables raw mode + alternate screen and "installs a panic
  hook that restores the terminal before panicking"; call init AFTER installing your own panic hooks. `restore` prints
  errors to stderr, does not panic. `init_with_options` with inline/fixed viewport enables raw mode but NOT alternate
  screen. V (ratatui/src/init.rs at ratatui-v0.30.2, lines 192-196, 335-342).
- The panic hook is the only restore guarantee in that module; the source has no signal handling (grep for signal: no
  hit). So SIGTERM/SIGHUP restore is the app's job (I, from the grep).
- Layout: constraints `Length`, `Min`, `Max`, `Ratio`, `Percentage`; origin top-left, u16 coordinates. V (ratatui.rs/concepts/layout).
- Resize: events carry resize; the init.rs docs show adding resize-aware redraw to the event loop. V.
- Testing: `TestBackend::new(w,h)` + `Terminal`; `assert_snapshot!(terminal.backend())` with insta. TestBackend
  `Display` prints only each cell's symbol per row (`buffer_view`), so styles and colours are NOT in a text snapshot; it
  also records cursor position and `assert_cursor_position`. V (ratatui-core/src/backend/test.rs at HEAD;
  ratatui.rs/recipes/testing/snapshots).
- Event handling: key events: check `KeyEventKind::Press` (Windows/kitty report release as well). V (init.rs docs examples).

### Textual (Python)

Pin: v8.2.8 (2026-06-30; GitHub releases). Licence: MIT (LICENSE at v8.2.8, "Copyright (c) 2021 Will McGugan"). Docs:
<https://textual.textualize.io> (read 2026-11-23).

- Default App bindings: `ctrl+q` quit with `priority=True` ("so there is always a way to exit the app") and `ctrl+c` ->
  `help_quit` (system binding, not quit). V (api/app BINDINGS, guide/input).
- Focus: one widget at a time gets key events; Tab / Shift+Tab move focus; `can_focus` per widget. Priority bindings are
  checked before the focused widget's. `Footer` widget shows bindings with `show=True`. V (guide/input).
- Input docs state "the Tab key is indistinguishable from Ctrl+I in the terminal" so key events carry `aliases`
  (["tab","ctrl+i"]); "Not all key combinations are supported in terminals and some keys may be intercepted by your OS";
  run `textual keys` to see what arrives. V.
- Animations: env `TEXTUAL_ANIMATIONS` (default FULL; valid values come from the `AnimationLevel` type, invalid value
  falls back to full), `TEXTUAL_SMOOTH_SCROLL=0`, `TEXTUAL_FPS` (default 60). V (src/textual/constants.py at v8.2.8,
  lines 95-105, 152-169). The values `none`/`basic`/`full`: I (type not read).
- Testing: `app.run_test(size=(w,h))` async context manager gives a `Pilot` (press keys, click, resize via `size`);
  snapshot testing through the official plugin pytest-textual-snapshot (`snap_compare` fixture, SVG screenshots; first
  run always fails). V (guide/testing).
- Command palette (ctrl+p by default in the guide) built in. Only the page title was read; I.

### Bubble Tea / Lip Gloss (Go)

Pin: bubbletea v2.1.2 (2026-11-18), lipgloss v2.1.1 (2026-11-15), bubbles v2.2.2. Module path is now
`charm.land/bubbletea/v2`, `charm.land/lipgloss/v2` (README, upgrade guide). Licence: MIT both (LICENSE at tags). v1
code in agent memory is outdated: v2 is declarative.

- v2: alt screen, mouse mode, focus reporting, bracketed paste and keyboard enhancements are fields on the `tea.View`
  returned from `View()` (`v.AltScreen = true`, `v.MouseMode = tea.MouseModeCellMotion`, `v.ReportFocus`,
  `v.DisableBracketedPasteMode`, `v.KeyboardEnhancements`); `tea.WithAltScreen`, `tea.WithMouseCellMotion` and
  `tea.EnterAltScreen` are removed. Space is now `"space"` in `msg.String()`. Paste arrives as `PasteMsg` /
  `PasteStartMsg` / `PasteEndMsg`, not as KeyMsg. `View` has a `Cursor *tea.Cursor` field (position, shape). V
  (UPGRADE_GUIDE_V2.md and tea.go at v2.1.2).
- Safety nets: default recover from panics and restore the terminal (`WithoutCatchPanics` turns it off: "the terminal
  will be in a fairly unusable state"); a signal handler for SIGINT/SIGTERM is installed (`WithoutSignalHandler`
  disables it); `ErrInterrupted` on SIGINT; `tea.Suspend()` / `SuspendMsg` supported where the OS allows. V (options.go,
  tea.go at v2.1.2).
- Lip Gloss v2: colour profile downsampling is automatic when output goes through `lipgloss.Println`/`Sprint` or Bubble
  Tea; standalone use of other printers skips it. V (README at v2.1.1).
- Testing: `teatest` is in `github.com/charmbracelet/x/exp/teatest` (the `exp` path marks it experimental, I):
  `NewTestModel` with `WithInitialTermSize`, `Send`, `Type`, `WaitFor`, `RequireEqualOutput` (golden files),
  `FinalModel`. V (pkg.go.dev index, read once; docs-mcp then failed so licence/version of x/exp not read).

### ncurses (C)

Pin: ncurses 6.6, patch 20261010 (man pages at invisible-island.net/ncurses/man/, page dates 2025-08-23 to 2026-09-19).
Licence: the ncurses licence, which its own page summarises as "a restatement of MIT-X11" (quoted via notcurses README;
ncurses-license.html shows "that MIT-X11 License" heading). Roughly MIT-style.

- Gives you: signal handlers for SIGINT/SIGTERM (cleanup), SIGTSTP (suspend and repaint), SIGWINCH (KEY_RESIZE plus
  `resizeterm`); terminfo-driven keys; `ESCDELAY`; colour pairs. Does NOT give you: layout, focus, widgets (separate
  panel/menu/form libs), or testing support. V (curs_initscr, curs_getch, curs_variables). Its own cleanup handler is
  documented as not async-signal-safe. V.
- `ESCDELAY` is an ncurses extension; default 1000 ms ("one second"), overridable by environment variable, upper limit
  30,000 when read from the environment, and the docs say to lower it for slow remote hosts only with care. V
  (ncurses(3x) ENVIRONMENT, ncurses 6.6). So a curses app has a one-second Esc lag unless the author sets it.
- ECMA-48: 5th edition, June 1991 (ISO/IEC 6429),
  <https://ecma-international.org/publications-and-standards/standards/ecma-48/> (PDF linked there, not read in full).
  Licence: Ecma copyright, free download; no licence text read. ctlseqs quotes it on 7-bit/8-bit equivalence only.

### notcurses (C/C++ library)

Pin: v3.0.17 (2025-10-28; last release, the repo is quiet since). Licence: Apache-2.0 (README "Apache2-licensed in its
entirety"; COPYRIGHT file header).

- `notcurses_init` options (man notcurses_init(3) at v3.0.17): installs handlers for SIGWINCH and SIGCONT (resize events
  `NCKEY_RESIZE`; opt out with `NCOPTION_NO_WINCH_SIGHANDLER`); installs handlers for SIGABRT, SIGBUS, SIGFPE, SIGILL,
  SIGINT, SIGQUIT, SIGSEGV, SIGTERM that clean up the terminal and re-raise to the previous handler (opt out with
  `NCOPTION_NO_QUIT_SIGHANDLERS`); alternate screen is the default and `NCOPTION_NO_ALTERNATE_SCREEN` is provided
  because "users tend to have strong opinions regarding the alternate screen", so expose it as a CLI option;
  `NCOPTION_CLI_MODE` alias for non-fullscreen use. V.
- Input: `ncinput` carries ctrl/alt/shift/modifier bitmask and an `NCTYPE_RELEASE` event type (kitty protocol use). V
  (man notcurses_input at v3.0.17, struct only).

### FTXUI (C++)

Pin: v7.0.3 (2026-08-06). Licence: MIT ("Copyright (c) 2019 Arthur Sonzogni").

- In v7 the interactive class is `App` (`src/ftxui/component/app.cpp`); `App::Fullscreen()` uses the alternate screen.
  On exit it writes `ESC[?1049l`, and turns off mouse modes 1000/1002/1003/1006. Records
  SIGINT/SIGTERM/SIGSEGV/SIGILL/SIGABRT/SIGFPE; Ctrl-C is turned into SIGINT handling unless a component handles it
  (`force_handle_ctrl_c_ = true`); SIGTSTP handler uninstalls the terminal state, re-raises SIGTSTP, then reinstalls on
  resume; SIGWINCH posts a resize event. V (app.cpp at v7.0.3 lines 121-122, 433-437, 470-518, 580, 900-906, 1270-1300).
  Screen reader or accessibility support: no hit in these greps (I).
- No official testing facility was read; FTXUI renders to a `Screen` object that can be printed without a terminal (I,
  not read this session).

## 3. Keybinding conventions (evidence from each tool's own docs)

All pins: tag's own documentation file, read 2026-11-23. Licences: lazygit MIT; k9s Apache-2.0; htop GPL-2.0 (COPYING;
the "or later" clause not checked); btop Apache-2.0; Midnight Commander GPL (doc/COPYING, version not read); vim "VIM
LICENSE" (charityware); less "Less License" (dual with GPL, not read in full).

| Tool (pin)                                | Help                       | Quit                                                     | Back/cancel                                                              | Search/filter                                                  | Other                                                                                               |
| ----------------------------------------- | -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| lazygit v0.66.3                           | `?` opens keybindings menu | `q` or `<ctrl+c>`                                        | `<esc>` cancel/close                                                     | `/` search or filter current view                              | `]` next tab; `<`/`>` scroll top/bottom; `J`/`K`, `<pgup>`/`<pgdown>`, `<ctrl+u>`/`<ctrl+d>` scroll |
| k9s v0.51.0                               | `?` shows mnemonics        | `:quit`, `:q`, `ctrl-c` (config can disable ctrl-c exit) | `esc` goes back; esc also leaves view/command/filter mode                | `/` filter, `:` command mode                                   | key hints in the header                                                                             |
| htop 3.5.3                                | `F1`, `h`, `?`             | `F10` or `q`                                             | -                                                                        | `F3` or `/` incremental search; `F4` or `\` incremental filter | function keys listed in a bottom bar (the bar is documented in the man page: I)                     |
| btop v1.4.8                               | `F1`, `?`, `h`             | `q` or `ctrl+c`                                          | `Esc` or `m` toggles main menu (Esc does not mean back at the top level) | none in help text                                              | `ctrl+z` sleep; option `vim_keys`: hjkl; mouse fully supported                                      |
| Midnight Commander 4.8.33                 | `F1`                       | `F10` (also S-F10)                                       | -                                                                        | -                                                              | where F-keys do not work, Esc then digit 1-9,0 = F1..F10; Esc is also the Meta prefix               |
| vim v9.2.1397                             | `<F1>` / `<Help>`          | `:q` (no single-key quit)                                | `<Esc>` leaves insert/visual; `CTRL-[` is the same                       | `/`                                                            | hjkl cursor keys; `CTRL-B` back one screen; `CTRL-A` add to number; `CTRL-Z` suspend                |
| less v714                                 | `h` or `H`                 | `q`, `:q`, `Q`, `ZZ`                                     | -                                                                        | `/pattern`, `n`, `N`                                           | `b`/`^B` back one window; `v` opens `$VISUAL`; `ESC-` prefixes                                      |
| V for all rows (docs/source of each tag). |                            |                                                          |                                                                          |                                                                |                                                                                                     |

What they agree on (I, from the table): `?` or F1 for help in most; `q` quits the four list-style tools (lazygit, htop,
btop, less) while vim, k9s and mc use their own forms; Esc cancels or goes back in lazygit/k9s but not in btop (menu) or
mc (prefix); `/` is search or filter everywhere it exists; vi motion keys appear in lazygit (`J`/`K`/`H`/`L`), btop
(opt-in `vim_keys`), less, vim. Disagreement: btop lets `ctrl+c` quit, k9s makes it configurable, lazygit quits on it,
and Textual's default does not quit on it (`ctrl+q` quits).

Multiplexer and emulator conflicts:

- tmux 3.8 prefix `C-b` by default; `C-b C-b` sends it through (tmux.1 DEFAULT KEY BINDINGS). Both `less` (`^B` back one
  window) and vim (`CTRL-B` scroll back one screen) use Ctrl+B. V (less.hlp v714; vim index.txt v9.2.1397; tmux.1 3.8).
  So a TUI that binds Ctrl+B is shadowed inside tmux until the user presses it twice.
- GNU screen: command character is `C-a` by default ("By default, each command begins with a control-a"), configurable.
  Ctrl+A is "add N to number" in vim and beginning-of-line in readline (the latter I). V (GNU screen manual at gnu.org,
  read 2026-11-23; version not captured).
- GNOME Terminal (stable help, read 2026-11-23; WebFetch paraphrase): Shift+Ctrl+T/N/W/Q (tab/window), Shift+Ctrl+C/V
  copy/paste, Shift+Ctrl+F find, Alt+1..Alt+9 switch tab, F11 full screen; the page lists no default F1 or F10 shortcut.
  So Alt+digit is taken by the emulator; Ctrl+Shift+letter is the emulator's namespace. V.
- tmux `escape-time` (milliseconds tmux waits after Esc to decide if it starts a sequence) is why Esc feels slow in tmux
  (I for the symptom, V for the option text).
- CUA (IBM Common User Access, 1987, via Wikipedia secondary source, read 2026-11-23): F1 help, F5 refresh, F10
  activates menus, Alt+underlined-letter opens menus, Tab / Shift+Tab move between dialog fields; the page says Esc was
  inconsistent across programs ("Some programs used Esc to cancel an action, while some used it to complete one"). V
  (Wikipedia), CUA documents themselves not read.
- Key hints: Textual `Footer` shows bindings from `BINDINGS`; lazygit shows a hint bar and `?` menu; htop bottom bar.
  The "visible key-hint bar" is therefore documented for Textual only (V) and for the others I did not read their UI
  docs (I).

## 4. Accessibility

Evidence is thin and mostly practitioner reports. No standards-body document is specific to full-screen TUIs.

- W3C WCAG2ICT, Group Note 11 December 2025 (<https://www.w3.org/TR/2025/NOTE-wcag2ict-22-20251211/>), informative, not
  endorsed by W3C itself (W3C licence: document licence not read). Appendix B "Text / Command-Line / Terminal
  Applications": the terminal acts like a user agent, AT must obtain all displayed text and infer structure and screen
  updates from the character matrix; plain text is "programmatically determinable" as lines of text; analysis techniques
  depend on finding the text cursor, so "soft cursors" and highlight bars "may bypass" them and cause failures; for
  contrast (1.4.3) it suggests relying on the terminal to render with sufficient contrast and notes many terminals let
  users force one foreground colour. 1.4.1 (colour) applies as written. V via WebFetch summaries (paraphrase, not
  verbatim; re-read the Note before quoting).
- GitHub CLI accessibility post (github.blog, 2 May 2025, updated 12 May 2025; GitHub CLI v2.72.0, `gh a11y`): "no
  equivalent, comprehensive standard for the terminal"; screen-reader users get prompts built with `charmbracelet/huh`
  because "constant screen redraws" are hard to read aloud; spinners that redraw braille characters were replaced by
  static text ("Working..."); colours aligned to the 4-bit ANSI palette so users can re-theme in their terminal, because
  a terminal's background is not set by the application and a legacy fixed palette gave low contrast. V (primary vendor
  post; they say their changes are a Public Preview).
- huh README (charm.land/huh/v2 at HEAD, MIT): first-class accessible mode, `form.WithAccessible(true)`; recommends
  setting it from an environment variable such as `ACCESSIBLE`, "drop TUIs in favor of standard prompts". V (README,
  HEAD, 2026-11-23).
- Claude Code docs (code.claude.com/docs/en/accessibility, read 2026-11-23, no version): screen reader mode replaces the
  visual interface with "plain, linear text" printed as labelled lines; opt-in via flag, env var or user settings;
  project settings cannot switch it on; separate `prefersReducedMotion` and colourblind-friendly themes. V. A vendor's
  own doc, not independent evidence that it works.
- Ink README (vadimdemedes/ink, HEAD): `useIsScreenReaderEnabled()` hook; reading of the INK_SCREEN_READER env var comes
  from a search snippet only. V for the hook (README), I for the env var.
- Casey Reeves, "The text mode lie" (xogium.me, 5 January 2026): single-author, blind-user account, anecdotal and not
  peer reviewed. Claims: grid-redraw frameworks (Ink, Bubble Tea, tcell) move the hardware cursor to update timers and
  spinners, so a cursor-tracking reader (Speakup, NVDA) announces the jumps; older tools stay usable because they let
  you hide the cursor, keep a single focus column (kernel menuconfig), or use VT100 scrolling regions (irssi). V that
  the article says this; the causal claims are the author's testimony (unverified; not corroborated by an independent
  test).
- BRLTTY Reference Manual (brltty.app/doc/Manual-BRLTTY/English/BRLTTY-4.html, read 2026-11-23, version not captured):
  braille window follows the cursor ("cursor tracking"); the screen cursor is shown as dots 7 and 8; `HOME`/`BACK`
  commands exist to recover from "an unexpected event (like cursor tracking)" moving the window. V. This is why cursor
  placement is the focus cue for braille users.
- NVDA 2026.3.1 user guide: in Windows Terminal text review works over the whole buffer; "In some cases, such as when
  connected over SSH, caret updates may be delayed", with a configurable caret move timeout. V.
- blindcomputing.org "State of Linux Command Line Accessibility" (2018, old): VTE terminals usable; "QT based terminals
  ... not accessible at all" (konsole, as of 2018, the author's check); tmux/screen splits make the reader read both
  panes on a line, a native split (terminator) avoids it. V that the post says it; dated.
- Maintainer positions: Textual issue #2425 "Accessibility" open since 2023-04-28; maintainer comment (2023-04-30) that
  the terminal has "historically poor accessibility", better later via web; issue #2348 (BRLTTY user asking whether
  Textual can keep the standard cursor) moved to a discussion, no answer read. Ratatui issue #2610 (2026-06-19):
  maintainer says focus, state and selection are not concepts in the library, "render characters at locations"; PR #2739
  (opened 2026-08-28, still open when read) adds an experimental Linux-only AT-SPI crate where the app declares an
  accessibility tree; verified only with Orca 46.1 by the author. V (issue and PR pages).
- opencode issue #43771 (2026-08-21): NVDA user cannot tell which list item is selected; asks for a textual `>` marker
  or a focus marker and cursor. Evidence of the user-visible symptom, one report. V.
- Orca/AT-SPI and VTE: no primary Orca or VTE document read (search found only Ghostty discussion #2351 and release
  notes). Orca/VoiceOver/fenrir behaviour with TUIs: no source found. Unsearched: fenrir docs, Speakup user guide text
  on cursor tracking (a search snippet says cursor tracking "experimental" in an old kernel doc: not read).
- Reduced motion: only Textual (`TEXTUAL_ANIMATIONS`), Claude Code (`prefersReducedMotion`) found; no terminal-level
  reduced-motion signal exists in the sources read (I). Contrast in themes: only the GitHub post and WCAG2ICT.

## 5. Testing TUIs

- Textual: `app.run_test(size=(w,h))` returns a `Pilot`; `pilot.press(...)`, `pilot.resize_terminal(width, height)` (API
  page), pause to let messages settle. Snapshot plugin pytest-textual-snapshot v1.1.0 (2025-01-23, MIT):
  `snap_compare(path_or_app, press=[...], terminal_size=(w,h), run_before=...)`, SVG screenshots, update with
  `--snapshot-update`, first run fails by design; its own sample disables cursor blink before capture. V (guide/testing;
  plugin README at v1.1.0).
- ratatui: `TestBackend::new(w,h)` plus `Terminal`; `TestBackend::resize(w,h)`; `assert_cursor_position`;
  `insta::assert_snapshot!(terminal.backend())` writes text only (symbols, no style). To catch a colour-only regression
  assert on the `Buffer` cells' style. V (test.rs at HEAD 2026-11-23; ratatui.rs snapshot recipe). The "assert on Buffer
  for style" is I.
- Bubble Tea: `teatest` (charmbracelet/x/exp/teatest, experimental path):
  `NewTestModel(tb, model, WithInitialTermSize(x,y))`, `Send(msg)` (so send `tea.WindowSizeMsg` to test resize: I),
  `Type`, `WaitFor`, `RequireEqualOutput` golden files, `FinalModel`. V (pkg.go.dev index; version and licence of x/exp
  not read beyond root MIT).
- Real pty: pexpect 4.9 (2023-11-25, ISC) `spawn(..., dimensions=(rows, cols))` sets the pty size; it matches byte
  streams, it is not a screen model (I: no terminal-emulator state in the module read). tmux 3.8: `send-keys`,
  `capture-pane -p` prints a pane to stdout, `-e` includes escape sequences for text and background attributes, `-a`
  captures the alternate screen (history not accessible), `-N`/`-J` trailing spaces; `resize-window -x -y` sets size. V
  (tmux.1 tag 3.8).
- VHS v0.12.1 (2026-09-24, MIT): tape scripts with `Type`, `Enter`, `Ctrl+...`, `Wait+Screen /regex/` (default `Wait`
  scope Line, timeout 15s), `Set Columns`/`Set Rows`, `Set CursorBlink false`; README: "VHS can also be used for
  integration testing. Use the `.txt` or `.ascii` output to generate golden files." Needs `ttyd` and `ffmpeg`. V (README
  at v0.12.1).
- FTXUI, ncurses, notcurses: no official testing guidance read.

## 6. Design guidance documents

- Monospace Design TUI (github.com/coreyt/monospace-design-tui, v0.3.0, commit 866322e8a4d799686b76f390cfb28ce80c6c3bef,
  2026-04-19): single-author "design language" for TUIs, rules meant to be auditable, builds on IBM CUA, OS/2, Norton
  Commander, Turbo Vision, lazygit, k9s, btop, bottom, Helix; ships a Textual appendix and an AI-agent directive.
  Licence CC BY-SA 4.0 (LICENSE; ShareAlike matters if a skill copies text). Young and unreviewed: I could not find
  independent adoption evidence. Treat as input, not a standard. V (README).
- IBM CUA via Wikipedia (secondary), see section 3.
- Textual docs (MIT code; docs licence not read) and Ratatui website docs, Bubble Tea/Lip Gloss READMEs (MIT): framework
  guides, not design systems. A "Charm design system" was not found. W3C WCAG2ICT (section 4) is the only standards-body
  text touching terminal apps.
- Third-party "skills" and blog posts about TUI design found by search (hyperskills tui-design, hyperbliss blog) were
  not read; marketing-grade.

## Gaps and contested points

- Bubble Tea v2 is current (v2.1.2) and differs from v1 in many APIs: any skill example must pin the major version.
- ctlseqs lacks mode 2026; xterm's own support unknown. Terminal-wg spec site unreachable (Anubis).
- ECMA-48 text and terminfo(5) capability details (smcup/rmcup, `RGB`) read only as man-page index entries.
- Accessibility: Reeves's claims (cursor teleporting, hide-the-cursor works) rest on one testimony; ratatui, Textual
  maintainers say they have no semantic model; BRLTTY, NVDA docs confirm cursor/caret is the AT's tracking point. The
  WCAG2ICT paraphrase came through WebFetch.
- Not read: ECMA-48 itself, terminfo(5), kitty/WezTerm/Ghostty docs, Windows Terminal, fenrir, Orca guide, Speakup
  guide, k9s/lazygit UI hint-bar docs, GNU screen version.
