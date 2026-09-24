# Fuzzing with atheris

Fuzzing feeds generated input to code until something raises. It finds the crash on input nobody thought to
write: a truncated file, an unexpected encoding, a delimiter in the wrong place. Aim it at code that consumes
bytes or text from outside, such as parsers, decoders, and file or protocol readers.

Start with Hypothesis (see [parametrize-and-property.md](parametrize-and-property.md)). A `@given` test with a
"never raises" property runs in the ordinary suite and covers most needs. Reach for
[atheris](https://github.com/google/atheris) when a short random search is not enough: atheris is
coverage-guided, so it keeps and mutates the inputs that reach new branches, and it can run for minutes or
hours. It also fuzzes native extensions, and it is the engine OSS-Fuzz uses for Python.

## Requirements

atheris ships Linux wheels; `uv run --with atheris` installed one on Python 3.12 without a compiler. Its
current source supports Python 3.11 to 3.14, and older interpreters need an older release. Check the project's
interpreter before adopting it.

## Write a Harness

A harness is a script, not a pytest test. It takes one `bytes` argument, and any exception that escapes it is a
finding.

```python
import sys

import atheris

with atheris.instrument_imports():
    from mypkg.parser import parse


def test_one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    text = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())
    try:
        parse(text)
    except ParseError:
        pass  # the documented rejection; anything else is a bug


atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

Import the code under test inside `instrument_imports()`, or atheris sees no coverage and fuzzes blind. It also
instruments whatever those modules import, so expect lower throughput once real dependencies load.
`FuzzedDataProvider` turns the raw bytes into typed values: strings, integers, lists.

atheris has no way to declare an expected exception. Catch the exceptions the function documents inside the
harness, and let everything else escape.

## Run and Reproduce

```bash
python fuzz_parser.py -max_total_time=60 corpus/          # time-boxed run; corpus/ keeps useful inputs
python fuzz_parser.py -runs=100000 corpus/                # bounded by iterations instead
python fuzz_parser.py -artifact_prefix=crashes/ corpus/   # where crash files go; the default is the cwd
python fuzz_parser.py crashes/crash-<hash>                # replay one crashing input
```

Flags after the script name go to libFuzzer. A crash writes the input to a `crash-<hash>` file, and passing
that file back replays it deterministically. Once the cause is understood, turn the input into an ordinary
regression test, or an `@example` on a Hypothesis test, so the ordinary suite keeps it covered.

A 60-second run on a small pure-Python parser in this repository made about 200,000 executions per second and
found nothing, while a copy with a deliberate off-by-one crashed within the first few inputs. A clean run is
evidence only for the input shapes the harness can express.

## Reuse a Hypothesis Strategy

A `@given` test exposes `.hypothesis.fuzz_one_input`, which atheris can drive directly:

```python
@given(st.text())
def check_parse(text):
    parse(text)

atheris.Setup(sys.argv, check_parse.hypothesis.fuzz_one_input)
atheris.Fuzz()
```

This reuses strategies the suite already has, at a cost: on the same parser it ran about 30 times slower than
the plain harness and reached less coverage. Use it when the strategy encodes structure that random bytes would
rarely produce, and the plain harness otherwise.

## Further Reading

The OSS-Fuzz guide to [integrating a Python project](https://google.github.io/oss-fuzz/getting-started/new-project-guide/python-lang/)
covers continuous fuzzing, and points to the `ujson` project for harnesses in both styles.
