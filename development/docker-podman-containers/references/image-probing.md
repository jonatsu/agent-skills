# Probing Image Contents

Use these probes to find what a package would add to an image, which file a library name loads, which Python
requirements need a source build, how large an image is, and how to remove what test builds leave behind. The commands
are written for Debian-based images; `<image>`, `<pkg>`, and `libexample.so.2` stand for the real names.

## Contents

01. Run every probe in a throwaway container
02. See what a package would install
03. Check what recommended packages carry
04. Find which dependency pulls an unwanted package
05. Look inside a package without installing it
06. Check which file a library name resolves to
07. Find requirements without a prebuilt wheel
08. Resolve a base image's digest
09. Measure an image
10. Clean up after test builds

## Run Every Probe in a Throwaway Container

Probes install packages and change files, so run each in a container that `--rm` deletes when the command exits.
`--name` lets you stop the container by name, because an interrupted `run` started from a tool or script can keep
running:

```sh
podman run --rm --name probe --arch arm64 <image> sh -c 'apt-get update -qq && apt-cache depends <pkg>'
podman ps --filter name=probe   # after an interruption
podman stop probe
```

`--arch` runs a foreign-architecture image through QEMU emulation; Docker spells it `--platform linux/arm64`. For a
probe longer than one line, write a script and mount its directory read-only with `-v "$PWD/probes:/probe:ro,Z"`. The
`Z` suffix relabels the files so that SELinux lets the container read them.

## See What a Package Would Install

`apt-get install -s` simulates an install: it prints one `Inst` line per package and changes nothing. Count the lines,
and search them for the libraries the image should not carry:

```sh
apt-get install -s --no-install-recommends <pkg> > sim.txt
grep -c '^Inst' sim.txt
awk '/^Inst/{print $2}' sim.txt | grep -E 'libx11|libxcb|wayland|libgtk|libqt'
```

`apt-cache depends <pkg>` shows the split. `Depends:` lines are mandatory, and `Recommends:` lines are the ones
`--no-install-recommends` skips. The option cannot drop a hard dependency; only a different package or a source build
removes one.

## Check What Recommended Packages Carry

A recommended package can hold an essential runtime part, such as the plugins or modules a library loads by name.
Adding `--no-install-recommends`, for example to satisfy hadolint rule DL3015, then removes that part silently: the
image still builds, and the library still imports. Before dropping recommends from an install, list them with
`apt-cache depends <pkg> | grep Recommends:` and check each for files the workload loads at run time. After the change,
run `ldd` on each plugin and open it the way the program does, as the next sections show. An import alone often loads
no plugin.

## Find Which Dependency Pulls an Unwanted Package

Simulate each direct dependency separately. The dependency whose simulation contains the unwanted package is the one
that pulls it:

```sh
for dep in $(apt-cache depends <pkg> | awk '/Depends:/{print $2}'); do
  if apt-get install -s --no-install-recommends "$dep" 2>/dev/null | grep -q '^Inst <unwanted-pkg> '; then
    echo "pulled by: $dep"
  fi
done
```

Repeat the loop on the package it prints until you reach the one that depends on the unwanted package directly. Read
what the unwanted package costs from its installed size, in kilobytes:

```sh
apt-cache show <unwanted-pkg> | awk '/^Installed-Size/{print $2; exit}'
```

## Look Inside a Package Without Installing It

`apt-get download` fetches the release's current `.deb` into the current directory, and `dpkg-deb` reads it:

```sh
apt-get download <pkg>
dpkg-deb -f <pkg>_*.deb Depends       # the dependency list
dpkg-deb -c <pkg>_*.deb | grep '\.so' # the shared libraries it carries
dpkg-deb -x <pkg>_*.deb extracted/    # unpack its files
```

## Check Which File a Library Name Resolves To

A program asks for a library by its soname, the versioned name the library declares, such as `libexample.so.2`. The
dynamic linker picks the file by searching its directories in order. When the image holds two copies of one soname,
such as a distribution package and a build in `/usr/local/lib`, that order decides which one loads.

The order comes from `/etc/ld.so.conf`, which includes `/etc/ld.so.conf.d/*.conf` in name order. Debian lists
`/usr/local/lib` in `libc.conf`, which sorts after the multiarch file, such as `aarch64-linux-gnu.conf`, so the
distribution copy wins. To prefer the local build, add a file that sorts first, such as `00-local.conf`, and run
`ldconfig`. Make the build fail when the soname resolves anywhere else, so a later package change cannot swap the copy
unnoticed.

```sh
objdump -p /usr/local/lib/libexample.so.2 | grep SONAME   # the soname a file declares; objdump is in binutils
ldconfig -p | grep libexample                             # every cached file for the soname
cat /etc/ld.so.conf.d/*.conf                              # the search order
ldd <binary-or-plugin>                                     # the file each needed library resolves to
```

A `not found` line from `ldd` means that the image lacks a library. A plugin loaded with `dlopen` follows the same
search, but only when the program first opens it, which is often at first use rather than at import. Trigger that load,
and set `LD_DEBUG=libs` to watch it: the linker then reports each library it looks for and each file it initializes.

```sh
LD_DEBUG=libs <command that opens the plugin> 2>&1 | grep -E 'find library=libexample|calling init: .*libexample'
```

## Find Requirements Without a Prebuilt Wheel

A wheel is a prebuilt Python package. When none matches the platform and Python version, pip builds the package from
source, which needs a compiler and headers. Find those requirements before a build fails by asking pip for each one
with wheels only:

```sh
python3 -m venv /tmp/venv
for req in $(sed 's/ //g' requirements.txt); do
  /tmp/venv/bin/pip download -q --no-deps --only-binary=:all: -d /tmp/wheels "$req" > /dev/null 2>&1 \
    || echo "no wheel: $req"
done
```

Run it in a container with the target architecture and Python version, because a wheel covers one combination.

## Resolve a Base Image's Digest

`SKILL.md` says when to pin by digest. To pin one reference for every platform, take the digest of the
multi-architecture index from the registry's `Docker-Content-Digest` header. Docker Hub needs an anonymous token first:

```sh
AUTH_URL="https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/debian:pull"
TOKEN=$(curl -fsS "$AUTH_URL" | jq -r .token)
curl -fsSI -H "Authorization: Bearer $TOKEN" \
  -H 'Accept: application/vnd.oci.image.index.v1+json' \
  https://registry-1.docker.io/v2/library/debian/manifests/<tag> | grep -i docker-content-digest
```

Request the moving tag and the dated tag, such as `stable-slim` and a dated snapshot tag. When both digests match,
write the dated tag and the digest together, as `image:<dated-tag>@sha256:<digest>`, and update both together. List
the per-architecture digests with `podman manifest inspect <image> | jq -r '.manifests[] | "\(.platform.architecture) \(.digest)"'`.

## Measure an Image

Podman and Docker report different sizes for the same image, so compare sizes only within one method:

- **Podman:** `podman image inspect --format '{{.Size}}' <image>` gives the uncompressed bytes of all layers, the
  base image included.
- **Docker 29 with the containerd image store:** `docker image inspect` and the `CONTENT SIZE` column give the
  compressed size, and `DISK USAGE` adds the unpacked layers. Neither is the uncompressed size. Sum the layers instead,
  with `docker history --human=false --format '{{.Size}}' <image> | paste -sd+ | bc`. Docker's layer sizes have run
  about 7% above Podman's for identical content.
- **Engine-neutral:** count the file bytes in a throwaway container with `run --rm <image> du -sxb /`. Use
  `du -xh -d 3 / 2>/dev/null | sort -h | tail -20` to find the largest directories.

`history --format '{{.Size}}\t{{.CreatedBy}}'` shows what each instruction added, under either engine. `system df -v`
splits each image into the layers it shares and those only it holds, which shows what removing it would free. Convert
bytes to binary units with `numfmt --to=iec-i --suffix=B --format=%.1f`; add `--field=1` for the `du` output.

## Clean Up After Test Builds

Test builds leave images, intermediate layers, and stopped containers, and Podman hides its build containers from
`podman ps -a`. Record the IDs before testing, and remove only those that appear afterwards. `--external` includes the
build containers:

```sh
podman images -a -q --no-trunc | sort -u > images-before.txt
podman ps -a --external -q --no-trunc | sort -u > containers-before.txt
# ... test builds ...
comm -13 images-before.txt <(podman images -a -q --no-trunc | sort -u)
comm -13 containers-before.txt <(podman ps -a --external -q --no-trunc | sort -u)
```

A new ID may belong to other work on the host, so inspect its tags, architecture, and creation time before removing it.
Select images by snapshot rather than with `--filter since=<image>`, which also matches images created in the same
second. Docker keeps its own store: snapshot `docker images -q --no-trunc` and `docker ps -a -q --no-trunc` the same
way. `docker buildx du` lists the BuildKit cache; run `docker buildx prune` only when that cache was empty before the
tests, because it removes every unused entry. Removal is destruction under `SKILL.md`'s authority rules.
