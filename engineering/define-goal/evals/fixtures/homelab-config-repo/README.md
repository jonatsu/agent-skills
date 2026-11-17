# homelab

Ansible playbooks for the machines on my home network.

| Host     | Role                                |
| -------- | ----------------------------------- |
| `nas`    | File server for the family; backups |
| `pi-dns` | DNS for the house, with ad blocking |
| `media`  | Jellyfin media server for the TV    |

## Layout

- `site.yml` applies every role to its hosts.
- `inventory/` holds the `staging` and `prod` inventories.
- `roles/` holds one role per service.
- `docs/` holds runbooks.

## Commands

```sh
ansible-lint
ansible-playbook -i inventory/staging.yml site.yml --check
ansible-playbook -i inventory/prod.yml site.yml
```
