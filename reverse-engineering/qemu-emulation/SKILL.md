---
name: qemu-emulation
description: Run binaries or firmware under QEMU for dynamic analysis. Use to select user-mode versus system emulation, diagnose prerequisites and hardware-model limits, trace guest syscalls, attach a debugger, or reproduce a bounded code path.
license: MIT
compatibility: Requires the QEMU executable for the selected guest architecture. User mode needs a supported guest OS ABI and matching loader/libraries when dynamic; system mode needs a compatible machine, CPU, boot artifacts, and required device models. Debugging requires a compatible GDB.
metadata:
  author: Joonas Onatsu
---

# QEMU dynamic analysis

Choose the smallest emulation environment that can answer the question, then verify its assumptions against observable\
execution. Successful startup does not establish that the guest reaches the requested behavior.

## Diagnose the environment

Record host OS, distribution/version, host architecture, and guest binary hash. Inspect the guest format, architecture,\
bitness, endianness, ABI, interpreter, and linked libraries using available file/header tools. A file extension or\
firmware label does not establish bare-metal code versus an OS userspace program. Check each selected executable with\
`command -v`, its version, and installed help before constructing the run. Read\
[prerequisite diagnosis](references/prerequisites.md) for package recommendations and permission checks. Report missing\
prerequisites with their purpose and verified host-appropriate package/configuration options. Recommendations do not\
authorize installation, sudo, package changes, network setup, or host-wide configuration changes. Continue static\
preparation when execution is blocked.

## Select the execution route

Use user mode for a supported foreign-architecture userspace executable when host syscall translation can satisfy its\
requirements. A dynamically linked executable needs a matching guest loader and libraries; static linking removes that\
loader requirement, not dependencies on files, services, syscalls, or devices. Use explicit emulator invocation rather\
than requiring binfmt registration or a privileged chroot.

Select system mode when the question requires a guest kernel, drivers, boot behavior, or modeled devices. Establish\
machine, CPU, RAM layout, interrupt controller, storage, kernel, device tree, root filesystem, and boot arguments\
together. A vendor kernel/rootfs is not automatically compatible with QEMU's `virt` or another generic board. Consult\
the selected machine's documentation and `-machine help`, `-cpu help`, and `-device help` before promising support.\
Some hardware peripherals exist in selected models; device presence does not establish compatibility with the original\
device protocol.

KVM applies only when host/guest architecture, hardware, QEMU build, and access permit it. Cross-architecture analysis\
generally uses software translation (TCG). Lack of `/dev/kvm` does not block user mode or TCG. Do not recommend\
virtualization groups or modules unless the selected route needs them.

## Prepare a bounded experiment

Define a discriminating input, observation, success condition, stop condition, and time/resource budget. Preserve\
originals and write into a disposable working directory or disk overlay. User-mode emulation translates guest syscalls\
into host operations and is not a security sandbox. Choose isolation appropriate to the supplied executable before\
running it; a guest sysroot is not a general filesystem jail. Keep networking and passthrough disabled unless the\
accepted experiment requires them. Keep debugger endpoints local and close them when the experiment ends;\
unauthenticated GDB access permits execution control.

For a supplied ARM Linux executable, the following illustrates user mode after ABI and CPU compatibility checks:

```sh
qemu-arm -L "$guest_sysroot" -strace "$guest_program" --help
```

Resolve both variables to supplied absolute paths and replace `--help` with the justified test input. `-L` supplies the\
ELF interpreter prefix; it does not reproduce every pathname, service, or device from the original rootfs. Use explicit\
working-directory/environment setup and verify actual file access from traces. Record the complete command, tool\
version, input, output, exit status, and trace.

First run a harmless architecture-matched fixture with a known exit or output before the target experiment. A useful\
fixture makes one syscall and exits with a chosen code; this checks loader/CPU execution and trace capture. A fixture\
success establishes that path only, not firmware boot or peripheral compatibility.

## Observe and refine

Use guest `-strace` where supported to inspect translated syscalls. A statically linked binary can still produce\
syscall traces. Empty traces can mean no syscall was reached, early loader/CPU failure, wrong trace destination, or\
incorrect invocation. Inspect stderr, exit status, and instruction-level logging before inferring the cause.

For debugging, verify emulator stub syntax and debugger guest-architecture support from installed help. User mode\
commonly waits with `-g PORT`; endpoint binding support varies, so verify exposure before starting it. System mode can\
use `-S -gdb tcp:127.0.0.1:PORT` to halt before execution and bind locally. Use a supported local socket or appropriate\
existing isolation when a user-mode build cannot constrain listener exposure. Load the matching executable in GDB, then\
attach, confirm architecture/mappings, and set a justified breakpoint. Compare registers, memory, branch conditions,\
and outputs with static predictions. Account for load bias, ASLR, shared objects, and relocations before using file\
addresses as runtime breakpoints.

A missing peripheral can be replaced by a documented model, stub, or injected boundary input in a disposable\
experiment. Record its contract, returned data, errors, and timing assumptions. Reaching code after a stub does not\
validate physical behavior. Separate missing dependencies, unsupported instruction/device models, intentional anti-VM\
checks, and a wrong loading hypothesis.

## Complete or diagnose the run

| Symptom                             | Investigate before changing the setup                                                                      |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Present executable reported missing | PT_INTERP path, sysroot contents, library ABI, then actual guest file accesses                             |
| Illegal instruction                 | Decoding mode, CPU extensions, guest ABI, selected emulator, and fault location                            |
| System boot stalls                  | Serial output, kernel/board/DTB compatibility, root device and drivers, then device accesses               |
| Device syscall fails                | Required guest driver and QEMU device model, or an explicit stub boundary                                  |
| Debugger cannot attach              | Stub enabled, listener transport/address, port availability, firewall/isolation, and debugger architecture |

Change one supported hypothesis at a time and rerun the discriminating input. Preserve failed-run diagnostics; use\
fresh state when replay could otherwise conceal a setup change. Finish with the reached code path and observable\
result, or an exact blocker with the next executable step. Report assumptions, stubs, unmodeled hardware, and the\
boundary between demonstrated logic and untested physical behavior.
