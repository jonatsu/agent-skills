# QEMU prerequisite diagnosis

Check requirements for the selected operation only. Reading disassembly needs none of the optional guest boot\
infrastructure. Use installed help and the [QEMU manual](https://www.qemu.org/docs/master/) for the installed release.

## Host and packages

On Linux, read `/etc/os-release` and `uname -m`. Determine the package manager and query its local catalogue. Confirm a\
package exists for the host release and supplies the required executable before recommending it. On Debian-family\
systems, `apt-cache policy PACKAGE` and `apt-cache show PACKAGE` inspect catalogue availability;\
`dpkg -S /absolute/executable` identifies the installed provider. Other distributions require their native equivalents.

| Selected operation           | Candidate dependency to verify                                                               |
| ---------------------------- | -------------------------------------------------------------------------------------------- |
| Linux user-mode emulation    | Target-specific `qemu-*` executable; often `qemu-user` on Debian/Ubuntu                      |
| ARM system emulation         | `qemu-system-arm`; often package `qemu-system-arm` on Debian/Ubuntu                          |
| Cross-architecture debugging | GDB with the guest target; often `gdb-multiarch` on Debian/Ubuntu                            |
| Inspect guest ELF metadata   | `readelf` and an architecture-capable disassembler; package varies by target                 |
| Dynamic guest program        | Guest runtime loader plus matching ABI libraries from the supplied rootfs/sysroot            |
| System boot                  | Compatible kernel/firmware, DTB where required, root filesystem, and supported machine model |

These names are candidates, not portable installation commands. Verify installed versions and repository metadata\
locally. A cross-compiler is needed to build guest code, not necessarily to execute an already supplied guest binary. A\
container runtime is an optional isolation route and brings its own permissions and filesystem boundary requirements.\
Do not pull images or enable services as part of prerequisite discovery.

## Guest compatibility

Inspect the ELF machine, flags, interpreter, dependencies, and attributes. For ARM, distinguish ARM/Thumb instruction\
state, CPU features, endianness, and soft/hard-float ABI as applicable. Confirm the loader file exists inside the\
supplied sysroot and that the libraries match its ABI. A host libc of the same name cannot substitute for the guest\
architecture's libc.

For system mode, inspect whether the kernel supports the selected board, interrupt controller, timer, console, and\
storage bus. A matching CPU instruction set alone is insufficient to boot vendor firmware on a generic machine. The\
[ARM virt documentation](https://www.qemu.org/docs/master/system/arm/virt.html) describes a virtual platform, not a\
model of arbitrary ARM hardware. Record needed peripherals and compare their actual model/register/protocol coverage\
with the guest's accesses.

## Permissions and configuration

Explicit user-mode invocation does not require system binfmt registration. TCG system emulation ordinarily needs no KVM\
permission. Check `/dev/kvm` and effective access only when selecting KVM. TAP networking, bridge setup, device\
passthrough, privileged mounts, or low ports can require separate permissions. Prefer already available unprivileged\
mechanisms when they meet the experiment, and obtain missing authorization before host changes. Check debugger listener\
address/transport and port availability before enabling the stub.

Report each missing item as: required operation, observed absence, recommended provider/configuration, verification\
source, privilege or setup dependency, and what can proceed in the meantime.
