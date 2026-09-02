# Initialize Repository Context

Initialization succeeds when every target client has a verified path to the smallest useful repository context, existing
knowledge is preserved, and unsupported behavior is reported accurately.

## 1. Establish Requirements

Identify the repository root, target agents, relevant package boundaries, and target filesystem constraints. Inspect
existing context files before creating anything. Read [loading-model.md](loading-model.md) for the relevant known adapters
or capability discovery.

Derive the minimum topology from those facts:

- one vendor-neutral canonical root file;
- filename adapters required by target clients;
- nested files only where rules differ by directory and the client path is verified;
- vendor-specific files only for behavior that cannot be represented portably; and
- `llms.txt` only when requested as a documentation index.

If two real candidate canonical files diverge, stop before changing them. Show unique sections, shared-section differences,
and client exposure, then ask whether to retain one or merge them.

## 2. Gather Repository Knowledge

Inspect authoritative local sources: manifests, task runners, continuous-integration workflows, toolchain pins,
contributor documentation, repository history, enforcement mechanisms, and the real directory structure.

Write only verified facts that pass the cache and behavior tests in `SKILL.md`. Prioritize non-obvious constraints,
reasons, ordering, silent failures, source-of-truth boundaries, and how existing enforcement affects agent work. Do not
copy a command catalog, directory listing, README, generated output, or third-party guidance into context.

When ecosystems disagree or none has been chosen, ask only if the answer changes the context. Otherwise omit unsupported
sections.

## 3. Create Safely

Use [templates.md](templates.md) and `../assets/AGENTS.template.md` only when their shapes save work. Remove every unused
section and placeholder.

Create the canonical file without replacing existing content. Create symlinks without force. Keep hand-maintained text
outside marked generated regions. For scoped files, add a root pointer that tells the agent when and what to read.

Do not create `.claude/rules`, `.github/instructions`, `.github/copilot-instructions.md`, or any comparable client-specific
surface unless a target-client requirement and repository need justify it.

## 4. Verify the Outcome

Verify that:

- every intended client reaches the appropriate context through a documented or observed path;
- every symlink resolves and remains inside the intended repository boundary;
- all referenced commands and paths exist;
- nested rules have a root pointer where a target client does not descend;
- no conflicting instructions or placeholders remain; and
- `llms.txt`, when requested, contains only resolving documentation links.

Use a live loaded-context command or controlled session when available. Name untested clients, unsupported filesystem
features, and unknown reload behavior in the delivery.
