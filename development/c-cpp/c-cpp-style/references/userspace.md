# Linux Userspace Patterns

Use this file for C and C++ that runs as a Linux process on the device. Each pattern is one that code gets wrong
without a prompt, with the page that states it. Man pages are from Linux man-pages 6.17. A note marked "inference" is
a synthesis, not a statement in the cited page.

## Contents

- Default Written Style
- Atomic File Replacement
- Descriptor Hygiene
- Spawning Processes
- Signals
- Parsing Untrusted Input
- Integer Overflow Checks
- Wiping Secrets
- Dropping Privileges
- Single-Run Command-Line Tools
- Device Conditions

## Default Written Style

Follow the project's own style first. A GNU-style project follows the GNU Coding Standards. With no style in the
tree, apply the systemd rules below. They come from `docs/CODING_STYLE.md` (commit `e691c3d7c145`), the best
maintained written style for modern Linux APIs.

Take layout from the `SKILL.md` section "Layout", not from systemd: match the surrounding indentation and brace every
body. Systemd's own layout (8-space indents, about 109 columns, no braces on single statements) is not part of this
default.

- Return a negative `-Exxx` value from every function that can fail for more than one reason.
- Check every allocation.
- Set close-on-exec at every call that creates a descriptor (see Descriptor Hygiene).
- Parse numbers with `strtol` and its siblings, never `atoi` (see Parsing Untrusted Input).
- Avoid `dup`, `fgets`, `basename`, `dirname`, `FILENAME_MAX`, and `exit` inside library-style code.
- Replace a fixed `char buf[256]` with a sized allocation or a length-checked helper.
- Use fixed-width `<stdint.h>` types, never kernel types such as `u32`.
- Use `unsigned` for values that cannot be negative.
- Prefer worker processes over threads, and `posix_spawn` where `fork` plus `exec` would do.

Write the underlying rule, not systemd's project-specific wrappers (`safe_atoi`, `xopenat`), which a foreign tree
lacks.

## Atomic File Replacement

A reader must see either the old file or the new one, and the new one must survive power loss. The man pages and LWN
say:

- `rename` atomically replaces the target. No moment exists when another process finds the new path missing, and a
  failed call keeps the old target (rename(2)).
- `fsync` flushes the file's data and metadata, but the directory entry may not reach disk. Call `fsync` on a
  descriptor for the directory too (fsync(2)).
- POSIX never promised that data survives without `fsync`. Ext3 ordering hid this, and ext4 delayed allocation
  exposed it. LWN (2009) says to fix the applications.
- A newly created file needs `fsync` on both the file and its directory (LWN, 2011).

Write the replacement in this order (inference, assembled from those pages):

1. Create a temporary file in the target's directory, so the `rename` stays on one filesystem.
2. Give it the final mode when you create it, or call `fchmod` before the rename.
3. Write all the data. Check every write for an error and a short count.
4. Call `fsync` on the temporary file's descriptor.
5. Call `close` and check its return value.
6. Call `rename` to the final name.
7. Open the directory and call `fsync` on it.

`renameat2` with `RENAME_NOREPLACE` refuses to overwrite an existing target, so it suits creation, not replacement.
`O_TMPFILE` creates a file with no name until the program links it in. Unverified: its `linkat(2)` step and limits;
read open(2) and linkat(2) before use.

## Descriptor Hygiene

A descriptor that leaks across `exec` gives the child access it should not have. Set close-on-exec when the call
creates the descriptor, never with a later `fcntl`. Another thread can `fork` and `exec` between the two calls, and
open(2) calls the flag "essential in some multithreaded programs" for that reason.

| Call that creates a descriptor | Set close-on-exec with |
| ------------------------------ | ---------------------- |
| `open`                         | `O_CLOEXEC`            |
| `socket`                       | `SOCK_CLOEXEC`         |
| `recvmsg` (received fds)       | `MSG_CMSG_CLOEXEC`     |
| `fcntl` duplication            | `F_DUPFD_CLOEXEC`      |
| `signalfd`                     | `SFD_CLOEXEC`          |
| `fopen`                        | mode letter `e`        |

`close_range(first, last, CLOSE_RANGE_CLOEXEC)` marks a whole range close-on-exec (since Linux 5.11).
`CLOSE_RANGE_UNSHARE` avoids races with threads that share the descriptor table (close_range(2)).

Open an untrusted path with `O_NONBLOCK`, so a FIFO or device cannot hang the open (systemd style). Then call `fstat`
on the descriptor, never `stat` on the path (inference). CERT names the path races FIO45-C (TOCTOU) and POS35-C
(symlinks).

## Spawning Processes

Use `posix_spawn` for a child that only runs another program. Its man page says it was specified for machines without
`fork(2)`, generally small embedded systems without an MMU, so it works on a nommu target. It lets the caller set the
child's signal mask and default signals (`POSIX_SPAWN_SETSIGMASK`, `POSIX_SPAWN_SETSIGDEF`) and run file actions
before `exec`. Descriptors marked close-on-exec close in the child.

```c
#include <spawn.h>
#include <sys/wait.h>

extern char **environ;

/* Run the program at an absolute path; return its exit status, or -1 on any failure. */
int run(const char *path, char *const argv[])
{
    pid_t pid;
    int status;

    if (posix_spawn(&pid, path, NULL, NULL, argv, environ) != 0) {
        return -1;
    }
    if (waitpid(pid, &status, 0) < 0) {
        return -1;
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}
```

- Avoid `system(3)`. Its man page forbids it in set-user-ID, set-group-ID, and capability-holding programs, because
  environment variables can subvert it. It also says input that reaches the command line must be carefully sanitized.
  Pass an `argv` array so no shell parses the arguments.
- Name the program by absolute path (inference). The same page advises against `execlp` and `execvp` in privileged
  code.
- After `fork` in a multithreaded program, the child may call only async-signal-safe functions (fork(2)). Systemd adds
  that threads plus `fork` can deadlock on the malloc lock.
- The HotOS 2019 paper "A fork() in the road" argues that `fork` should not be a first-class primitive in new
  designs. Treat that as opinion, not Linux policy. Systemd uses both `posix_spawn` and `fork` plus `exec`, as the
  case needs.

## Signals

Choose the first option that fits (inference, built from the man pages):

1. Block the signals and read them from a `signalfd` in the event loop, or call `sigwaitinfo`.
2. Write one byte to a self-pipe from the handler and read it in the loop.
3. Set a `volatile sig_atomic_t` flag in the handler and nothing else.

Facts behind that order:

- A handler may call only async-signal-safe functions, a fixed table in signal-safety(7). `printf` and `malloc` are
  not in it. The page calls the alternative, blocking signals around every unsafe call, difficult in any program of
  size.
- `signalfd` turns signals into a descriptor you `read`. Block those signals first with `sigprocmask(2)`. `SIGKILL`
  and `SIGSTOP` cannot arrive this way (signalfd(2)).
- Install handlers with `sigaction`, not `signal`, which is less portable (sigaction(2); GNU Coding Standards 4.2).
  Set `SA_RESTART` (systemd).

```c
#include <signal.h>
#include <stddef.h>

static volatile sig_atomic_t stop_requested;

static void on_term(int signo)
{
    (void)signo;
    stop_requested = 1;
}

int install_term_handler(void)
{
    struct sigaction sa = { .sa_handler = on_term, .sa_flags = SA_RESTART };

    sigemptyset(&sa.sa_mask);
    return sigaction(SIGTERM, &sa, NULL);
}
```

## Parsing Untrusted Input

Treat every byte from a file, socket, or device as hostile until a parser has accepted it.

- Parse once, at the boundary, into a validated typed structure. Carry a length with each pointer. Reject malformed
  input instead of repairing it (inference).
- The LangSec paper "The Halting Problems of Network Stack Insecurity" (;login:, December 2011) treats input handling
  as a recogniser for a language. It advises keeping the accepted language small and using grammar-generated parsers.
- Convert numbers as strtol(3) describes: set `errno = 0`, call, test `ERANGE`, and compare `endptr` with the start.
  That catches input with no digits. The function does not modify `errno` on success, so the reset matters. Also test
  that `*endptr` ends the field.
- Never use `atoi`; it reports no error.

Binary input needs three more rules:

- Read each integer by copying its bytes with `memcpy` into an integer variable, then converting the byte order with
  `be32toh`, `le64toh`, and the related functions in `<endian.h>` (endian(3)). Never cast a byte buffer to a struct
  or integer pointer: the cast ignores alignment and byte order, and breaks the aliasing rules (inference).
  Device-tree properties are big-endian, so a property read into a `uint32_t` needs `be32toh` too.
- Check lengths in an order in which no sum can overflow: compare a field's length with the bytes remaining, never
  `offset + length` with the total (inference).
- Validate the whole input before acting on any part of it, so malformed input changes nothing (inference).

```c
#include <endian.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

/* Read a big-endian u32 at off; false when fewer than 4 bytes remain. */
static bool read_be32(const unsigned char *buf, size_t len, size_t off, uint32_t *out)
{
    uint32_t raw;

    if (off > len || len - off < sizeof(raw)) {
        return false;
    }
    memcpy(&raw, buf + off, sizeof(raw));
    *out = be32toh(raw);
    return true;
}
```

Give every such parser a fuzz target; `c-cpp-testing` describes the setup.

```c
#include <errno.h>
#include <limits.h>
#include <stdbool.h>
#include <stdlib.h>

/* Parse a whole-string decimal int; false on any error. */
bool parse_int(const char *s, int *out)
{
    char *end;
    long v;

    errno = 0;
    v = strtol(s, &end, 10);
    if (errno != 0 || end == s || *end != '\0' || v < INT_MIN || v > INT_MAX) {
        return false;
    }
    *out = (int)v; /* range checked against INT_MIN and INT_MAX above */
    return true;
}
```

## Integer Overflow Checks

Check every addition, subtraction, and multiplication that feeds an allocation size, `memcpy` length, or index
(inference).

- Use `__builtin_add_overflow(a, b, &res)` and the `sub` and `mul` forms. GCC computes in infinite precision, returns
  true when the stored result differs, and defines the behaviour for every argument value (GCC manual).
- C23 adds `ckd_add`, `ckd_sub`, and `ckd_mul` in `<stdckdint.h>`, supported since GCC 14. Gate their use on
  `__STDC_VERSION__` and the compiler version, with the builtins as the fallback.

## Wiping Secrets

A plain `memset` before `free` can be removed by the optimiser, because the program never reads the buffer again.

- Call `explicit_bzero` on key material, passwords, and tokens when done. Its man page guarantees that compiler
  optimisations do not remove the erase. It is a nonstandard extension, available since glibc 2.25 and on the BSDs.
- `memset_explicit` is the C23 equivalent, and glibc 2.43 declares it in `string.h`. Check the installed C library
  first, because older glibc and other C libraries may lack it.
- Wipe on every exit path, failures included, not only after success (inference). A cleanup ladder or the `die()`
  helper below is the place.
- When the program links OpenSSL, `OPENSSL_cleanse` does the same job.
- Zeroing a buffer does not clear registers, spilled copies, swap, or core dumps (inference). Where secrets matter,
  add `mlock`, `madvise` with `MADV_DONTDUMP`, and short lifetimes.
- Turn core dumps off with `setrlimit(RLIMIT_CORE, ...)` at zero and `prctl(PR_SET_DUMPABLE, 0)`. A process that is
  not dumpable also cannot be attached with `ptrace(PTRACE_ATTACH)`, and root owns its `/proc/<pid>` files
  (PR_SET_DUMPABLE(2const)). A change of user or group ID resets the attribute, so call it after dropping privileges.
- Never pass a secret in `argv`, where `ps` and `/proc/<pid>/cmdline` show it to other users, and never write one to
  a message or a log (inference). Read it from a file, a descriptor, or standard input.

## Dropping Privileges

Split the work so the part that needs privilege is small and the rest has none. OpenSSH privilege separation is the
model. An unprivileged slave asks a privileged monitor for each privileged operation, and the monitor validates each
request (Provos, Friedl, Honeyman, USENIX Security 2003).

1. Under systemd, prefer the unit file's settings to code (inference; load the `systemd-units` skill). The directives
   are `NoNewPrivileges=`, `ProtectSystem=`, `ProtectHome=`, `PrivateTmp=`, `PrivateDevices=`,
   `CapabilityBoundingSet=`, `RestrictAddressFamilies=`, `SystemCallFilter=`, `MemoryDenyWriteExecute=`,
   `RestrictNamespaces=`, `DynamicUser=`, `LockPersonality=`, and `RestrictSUIDSGID=` (systemd.exec(5)).
2. In code, drop supplementary groups first, then the group ID, then the user ID. Verify that each drop worked (CERT
   POS36-C and POS37-C).
3. Drop capabilities you do not need from the bounding set with `prctl(PR_CAPBSET_DROP, ...)` (capabilities(7)).
4. Enable `no_new_privs` with `prctl` before running less trusted code. Children inherit it across `fork`, `clone`,
   and `execve`, and it cannot be unset. It stops set-user-ID bits and file capabilities from adding privilege. An
   unprivileged seccomp filter requires it (no_new_privs.rst; seccomp(2)).
5. Prefer a unit file or init script to a sandbox library on an embedded target (inference).

## Single-Run Command-Line Tools

A tool that runs once and exits may end through a `die()` helper instead of a cleanup ladder, when that helper first
wipes secrets and removes partial output (inference). Library code still returns errors to its caller.

- List every exit status in the file's header comment, and keep each value stable, because scripts branch on it.
  Callers test the status, never the message text.
- Write each message to standard error as `<program>: <what failed>; <what to do next>`.

For the wider design of options, messages, and exit statuses, use the `cli-ui-ux` skill.

## Device Conditions

An embedded device breaks three assumptions that desktop code makes (inference):

- The wall clock may be wrong until a time server sets it, or for ever on a device without one. Measure intervals,
  timeouts, and retries with `clock_gettime(CLOCK_MONOTONIC, ...)`, and use the wall clock only for timestamps shown
  to people.
- Flash wears with every write. Keep state that lasts one boot, such as PID files, sockets, and caches, on tmpfs under
  `/run`, and write persistent state only when it changes.
- Power can fail during a write. When rewriting a block device or a raw partition, order the writes so that an
  interrupted run leaves nothing a reader accepts: invalidate the header, write the payload, then write the header
  last. Call `fsync` on the device descriptor after each step, so the device does not reorder them.
