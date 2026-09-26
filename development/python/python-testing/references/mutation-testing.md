# Mutation Testing with mutmut

A passing suite proves the code runs, not that the tests would notice a bug. Mutation testing changes the code
in small ways, one mutant at a time, and reruns the tests. A mutant the tests kill is covered; a mutant that
survives is a change no test noticed.

Breaking the code by hand answers the question for one test. Use [mutmut](https://mutmut.readthedocs.io/) when
the question covers a module or a suite. What to do with a survivor, and whether a gap matters, is
`test-engineer`'s judgment; this reference covers running the tool and reading its output.

## Requirements

mutmut drives pytest and forks a process per test run, so it needs Linux or macOS; on Windows, run it under
WSL. It needs no project dependency to try it: `uv run --with mutmut mutmut run` runs it ephemerally. Add it as
a development dependency only when the project adopts it.

## Configure

mutmut reads `[tool.mutmut]` from `pyproject.toml` in the directory it runs from, and falls back to a
`[mutmut]` section in `setup.cfg`. Config loads before any subcommand, so without `source_paths` even
`mutmut --help` fails.

```toml
[tool.mutmut]
source_paths = ["src/mypkg"]                    # the whole package: this is what gets copied
only_mutate = ["src/mypkg/parser.py"]           # optional: mutate one file within it
pytest_add_cli_args_test_selection = ["tests/test_parser.py"]
```

`source_paths` decides what mutmut copies into its `mutants/` working directory. Point it at the package, not
at one file: naming a single file leaves its sibling modules out of the copy, and every test import fails. Use
`only_mutate` to narrow the mutation to one file.

Add `mutants/` to `.gitignore`.

## Run and Read

```bash
mutmut run                      # mutate, then run the selected tests against each mutant
mutmut results                  # list every mutant not killed
mutmut show <mutant-name>       # the diff of one mutant
mutmut tests-for-mutant <name>  # the tests mutmut ran against it
```

The progress line counts mutants per outcome: 🎉 killed, 🙁 survived, ⏰ timed out, 🤔 suspicious (slow), 🫥
covered by no test. A run over one 200-line module with a fast suite takes seconds; a whole project can take
hours, so scope a run to the module under change.

Read each survivor as one of three things:

- **A real gap.** On this repository's own description checker, `for line in lines[1:]` mutated to
  `lines[2:]` survived because every fixture put another key on the first frontmatter line. A second survivor
  forced a `"warn" if ... else "FAIL"` label to always say `warn`, because no test asserted the failure label.
  Write the test that kills it.
- **An equivalent mutant.** `"utf-8"` mutated to `"UTF-8"` survives because codec lookup ignores case. No test
  can kill it; ignore it.
- **An unpinned detail.** mutmut wraps string literals in `XX...XX`. A survivor there means no test asserts the
  exact text. Pin it only when the exact text is the contract, such as a user-facing message or a stable output
  format.

Do not chase a zero survivor count. The count is evidence for a review, not a gate.

## When Nothing Is Killed

**If mutmut reports that it could not find any test for any mutant, suspect the tests are importing the
original source rather than the mutated copy.** pytest searches upward from the `mutants/` directory for its
configuration. A `pyproject.toml` or `pytest.ini` further up, with its own `pythonpath` or `rootdir`, puts the
unmutated package first on the import path, and every mutant then looks untested. This was observed when the
project under test sat inside another repository. Put a `pytest.ini` next to the mutmut configuration to stop
the search, and list it in `also_copy` so the copy carries it too.

Set `debug = true` in the mutmut configuration to print the exact pytest command line for each mutant. That
is the fastest way to see what the tests actually imported.
