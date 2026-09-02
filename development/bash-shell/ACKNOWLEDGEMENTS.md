# Acknowledgements

This skill is original MIT-licensed work. No upstream prose, code, identifiers, or examples were copied.

The design was informed by review of Yudhi Armyndharis'
[`antigravity-skills`](https://github.com/rmyndharis/antigravity-skills), commit
`3eff4af253b3a15e2ba6edf2c2b743b53fd81211`, especially:

- `skills/bash-pro/SKILL.md`
- `skills/bash-defensive-patterns/SKILL.md`
- `skills/bash-defensive-patterns/resources/implementation-playbook.md`

Useful ideas considered from those references included the Bash-versus-POSIX boundary, input and failure-mode discovery,
arrays, NUL-safe traversal, temporary-resource cleanup, idempotency, dependency checks, signal handling, replacement
writes, and ShellCheck/shfmt/test validation.

The implementation here was written independently after rejecting the reviewed skills' blanket strict-mode rules, unsafe
deletion guidance, broken version predicates, hidden producer failures, incomplete cleanup examples, portability claims,
and scope-expanding output catalogues.

The immediate reference repository states that its collection was ported from
[`wshobson/agents`](https://github.com/wshobson/agents), also MIT-licensed.
