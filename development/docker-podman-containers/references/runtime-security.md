# Runtime and Supply-Chain Security

Apply controls from the target workload, runtime, kernel, and threat model. Linux isolation settings do not transfer
unchanged to Windows containers or every rootless runtime.

## Inspect Effective State

Inspect the image configuration and live container settings before recommending a change. Relevant evidence includes
the runtime user, capabilities, security options, namespaces, devices, mounts, writable paths, published ports, resource
limits, and restart behavior. Container environment output can contain secrets; select only the fields needed for the
diagnosis.

Membership in a rootful Docker daemon's control group commonly grants root-equivalent host power. Do not present a
service account with Docker socket access as a meaningful host privilege boundary.

Rootless Docker avoids that grant. Run `dockerd-rootless-setuptool.sh install` as the user: it starts a per-user
daemon and creates a CLI context named `rootless`. Rootless mode restricts some features, so check the workload
against Docker's rootless documentation.

## Replace Deployed Containers

Apply application, package, and image-configuration changes through version-controlled inputs, then build, qualify, and
deploy a new image. Use `exec` only for authorized diagnosis or one-off recovery; changes made inside a running
container, or captured with `docker commit`, are not a deployment source. Preserve the previous verified digest and
establish data compatibility before relying on rollback.

## Harden from a Compatible Baseline

For a typical Linux application workload, test these controls together:

- a non-root user with correct ownership for required files and mounts;
- all capabilities dropped, with individual capabilities restored only from demonstrated need;
- `no-new-privileges` enabled;
- a read-only root filesystem with explicit writable volumes or tmpfs mounts;
- the runtime's default seccomp profile and the host's normal AppArmor or SELinux policy;
- only required devices, namespaces, networks, ports, and host paths; and
- memory, CPU, process, file-descriptor, and log limits based on observed behavior.

Device plugins, low-level networking, debuggers, init systems, and infrastructure workloads may need exceptions. Keep
the exception local to that service and test it on the target host.

A non-root process reaches a host device, such as a USB node under `/dev/bus/usb`, through the device node's numeric
group ID on the host. Pass the device with `--device`, then grant the group. A group created in the image by name, such
as `plugdev`, grants access only when its ID matches the host's. Add the host's group ID at run time with
`--group-add <gid>`, Compose `group_add`, or create the image group with that ID. Rootless Podman can instead pass the
invoking user's own supplementary groups with `--group-add keep-groups`. That option works only with the crun runtime,
excludes other `--group-add` values, and is unavailable to remote clients.

## Bound Runtime Logs

Prefer application logs on standard output and standard error so the runtime's logging path captures them. Inspect the
effective logging driver, delivery mode, and storage destination. Set rotation or retention limits from the expected
rate and operational policy; an unbounded local log can exhaust host storage. Recreate affected containers after a
driver or option change, and verify that operators can still retrieve the required history.

## Keep the Runtime Seccomp Default

Docker recommends its current default seccomp profile for general workloads. Do not replace it with a generic bundled
allowlist: runtime defaults track kernel and engine security changes that a copied profile misses. Never use
`seccomp=unconfined` as a routine diagnostic step.

When a workload demonstrably needs a custom profile, start from the current profile shipped by the target runtime,
identify the blocked call and required arguments, and make the narrowest change. Test the full workload in an isolated
environment. Record the runtime version, kernel, profile source, reason, and regression check.

## Handle Images as Supply-Chain Objects

Read `image-scanning.md` for scanning, SBOM, and signing decisions. Pin deployment references to a verified digest where
the update workflow supports it. Avoid mounting the runtime socket or broad host paths into build and delivery tools;
those mounts extend compromise to the host or other workloads.
