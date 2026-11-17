# Repository Instructions

- Run `ansible-lint` before every commit.
- Keep secrets in Ansible Vault files; never commit a plain-text password or key.
- Apply a change to the `staging` inventory with `--check` before `prod`.
- Disable SSH password logins on every host.
- Runbooks live in `docs/`; keep one per recurring task.
