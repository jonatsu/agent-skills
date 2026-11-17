# Restore a File

1. Plug in the offsite disk.
2. Run `restic -r /mnt/offsite snapshots` and pick a snapshot.
3. Run `restic -r /mnt/offsite restore <snapshot> --target /tmp/restore --include <path>`.
