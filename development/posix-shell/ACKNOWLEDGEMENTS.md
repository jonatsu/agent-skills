# Acknowledgements

This skill is original MIT-licensed work. No upstream prose, code, or examples were copied. The package
replaces the installed `posix-shell-pro` name with `posix-shell` to describe its scope directly.

The design was informed by review of the `posix-shell-pro` skill in
[`sickn33/antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills), commit
`d0cfdce27c34e56eb1d0976aca1a397716f0a739`.

Useful subjects retained at a general level include POSIX-only syntax, argument parsing, quoting, status
handling, temporary resources, migration from Bash, static analysis, and testing across shell implementations.

The implementation here was written independently after rejecting the reviewed skill's unsupported
frontmatter, missing resource, blanket shell-option rules, unsafe data examples, incorrect prohibition of the
POSIX `readonly` utility, unqualified extension advice, and claims of portability beyond its evidence.
