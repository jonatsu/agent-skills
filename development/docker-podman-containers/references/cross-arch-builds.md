# Cross-Architecture Builds

An amd64 host builds and runs arm64 images through QEMU user-mode emulation: the kernel's `binfmt_misc` hands each
foreign executable to `qemu-<arch>`. Containers need the interpreter registered with the `F` (fix binary) flag. It makes
the kernel open the interpreter at registration, so the interpreter works inside a container that does not contain it.

## Host Packages on Ubuntu

| Purpose                | Ubuntu 24.04 LTS                 | Ubuntu 26.04 LTS             |
| ---------------------- | -------------------------------- | ---------------------------- |
| Emulation              | `qemu-user-static`               | `qemu-user-binfmt`           |
| Podman engine          | `podman` (4.x) and `buildah`     | `podman` (5.x) and `buildah` |
| Docker engine          | `docker.io`                      | `docker.io`                  |
| Docker BuildKit client | `docker-buildx`, from `-updates` | `docker-buildx`              |

On 24.04, install `qemu-user-static`. Its sibling `qemu-user-binfmt` registers the dynamically linked interpreter
without the `F` flag, so foreign binaries fail inside containers. On 26.04, `qemu-user` is statically linked,
`qemu-user-binfmt` registers it with `F`, and `qemu-user-static` no longer exists. Podman 4.x lacks the 5.x defaults
that `podman-differences.md` describes.

Without `docker-buildx`, Docker falls back to its legacy builder, which rejects `RUN --mount`. The Dev Containers CLI
then skips BuildKit too.

## Docker Next to Podman

- `docker.io` conflicts with `podman-docker`, so apt removes that shim. Check that the install removes nothing else.
- Write `{ "ip-forward-no-drop": true }` to `/etc/docker/daemon.json` before installing Docker. Without it, Docker
  sets the firewall's forward policy to drop, which cuts off forwarded traffic such as libvirt guests'.
- Install with `--no-install-recommends` to skip `ubuntu-fan`, which adds its own network service.
- Membership in the `docker` group is equivalent to root and takes effect at the next login. A socket ACL,
  `setfacl -m "u:$USER:rw" /run/docker.sock`, grants the same power and lasts until `dockerd` restarts.
- A session whose `DOCKER_HOST` points at Podman's socket needs `DOCKER_HOST=unix:///run/docker.sock` for Docker
  commands.

## Check the Emulation

```sh
cat /proc/sys/fs/binfmt_misc/qemu-aarch64                 # the flags line contains F, as in "flags: POF"
podman run --rm --arch arm64 <image> uname -m              # aarch64
docker run --rm --platform linux/arm64 <image> uname -m    # aarch64
```

Every package install and source build runs emulated and several times slower. A Python requirement without a
prebuilt wheel for the target costs the most; `image-probing.md` shows how to find those before the build.
