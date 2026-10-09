# Checks for this repository's skill packages. `just` lists the recipes.

uv := 'uv run --frozen'

# Every check and test; run before calling work done.
check: secrets hooks test

# The whole history scanned for secrets. The betterleaks hook reads only staged changes, so the hooks do not.
secrets:
    betterleaks git . --redact --exit-code 1

# Every pre-commit hook over the whole tree.
hooks:
    pre-commit run --all-files

# The checks' own tests and the bundled-script tests.
test:
    {{ uv }} pytest -q
    {{ uv }} python -m unittest discover -s tests -t tests

# Both validators over one skill: the Agent Skills specification, then skill-forge's policy.
skill-check skill:
    {{ uv }} skill-checks validate {{ quote(skill) }}
