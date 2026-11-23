# Testing MCU Firmware

How to test firmware that runs on a microcontroller. It covers what runs on the host, in an emulator, and on the
board. It also covers making hardware-facing code testable and starting with no tests. It adds the trade-offs and the
order of work to the skill body's "Make Hardware-Facing Code Testable".

Each claim carries one evidence label. "Doc" means a project's or vendor's own documentation. "Expert" means one named
practitioner's published opinion or worked example. "Inference" means a conclusion that no primary source states.
Where a source gives no numbers, this file says so.

## Contents

- Sources Cited
- What to Test Where
- One Source Tree, Two Builds
- Seams and Their Trade-Offs
- Adding Tests to an Untested Codebase
- Timing and Interrupts
- Limits of Host Tests
- Emulation
- Hardware in the Loop on a Small Budget
- Coverage on an MCU
- Zephyr: ztest and twister
- ESP-IDF: Unity and pytest-embedded
- Practices for an Untested MCU Project

## Sources Cited

- Grenning: James Grenning, "Test-Driven Development for Embedded C", conference paper, 2014, 23 pages,
  `wingman-sw.com/papers/EmbeddedTdd-Grenning-v1r1.pages.pdf`. Page numbers are PDF pages.
- Memfault: Tyler Hoffman's posts on the Memfault Interrupt blog. They cover unit-test basics (2019-10-08, CppUTest
  3.8), mocking (2020-05-12), and Renode (2020-07-07), plus an undated introduction to Renode.
- VanderVoord: Mark VanderVoord, the "Unit Test How?" series, 2015, `vandervoord.net`.
- Embedded Artistry: Phillip Johnston's "Virtual Devices" post, and a post dated 2021-10-25 on testing old code.
- Zephyr (v4.5.0) and ESP-IDF (v6.1.1): the documentation named in each section below.

Unverified: find the exact title and URL of each Memfault post, the VanderVoord articles, and the 2021 Embedded
Artistry post before relying on a citation. Search by author, topic, and date.

## What to Test Where

Grenning describes five stages that run less often as they get closer to the product (expert, Grenning pp. 19-20):

| Stage | Where it runs                    | What it is likely to find                                                         |
| ----- | -------------------------------- | --------------------------------------------------------------------------------- |
| 1     | The TDD microcycle on the host   | Logic, design, modularity, interface, and boundary conditions                     |
| 2     | Compile for the target processor | Compiler and library compatibility: language features, headers, prototypes        |
| 3     | Run tests on evaluation hardware | Processor execution problems, and portability: word size, alignment, endianness   |
| 4     | Run tests on the target hardware | Stage 3 problems, hardware integration, and misunderstood hardware specifications |
| 5     | Acceptance tests                 | Stage 4 problems, and misunderstood feature specifications                        |

Grenning says the cycle works when a build and test takes "only a handful of seconds", so the microcycle stays off the
target. Stage 3 sometimes makes up for very constrained target memory and is not always needed. He wants stages 2 to 4
to run on check-in, or at least nightly.

No source gives a ratio of tests per level, so this proportion is an inference from his frequency axis. Put most tests
on the host. Add a smaller layer in an emulator for paths that need the real startup and peripherals. Keep a thin layer
on hardware for what only silicon shows, such as timing, analog behaviour, DMA, clock trees, and errata.

## One Source Tree, Two Builds

Grenning calls building the same code for host and target "dual-targeting", and says the differences between the
environments should not discourage it. Practices 1 and 7 below say how to set it up.

Zephyr and ESP-IDF document the same split (doc). Zephyr's `unit_testing` board builds only the module under test plus
ztest into a native executable, and `native_sim` builds the whole operating system for the host. ESP-IDF runs Unity on
the chip and host tests on Linux. Its pytest-embedded runs on the target, on the Linux host, and in QEMU.

A first host build of firmware meets these hazards (inference; no primary source lists them):

- Fixed-address register pointers fault on a host, because the address is not mapped. Redirect them to RAM.
- Vendor and CMSIS headers, and intrinsics such as `__disable_irq` and critical-section macros, need stubs.
- Interrupt service routine attributes need a host macro that expands to nothing.

## Seams and Their Trade-Offs

The trade-offs below are inference unless a source is marked.

| Seam                       | Cost and strength                                                                                                 | Weakness                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Hardware abstraction layer | Needs a production change and a design choice per interface; the best long-term shape (expert: Embedded Artistry) | Adds one indirection; a badly shaped layer leaks hardware details                                              |
| Link-time substitution     | No production change; the cheapest start on legacy C (expert: Memfault; doc: CMock)                               | One fake per link set, so each test binary needs its own file list; weak for static and inlined code           |
| Preprocessor substitution  | Register headers rebuilt under a `TEST` macro, so registers become RAM variables (expert: VanderVoord)            | Complicates the production header, and the test header can drift from the real one                             |
| Function-pointer interface | The code calls through a table that a test fills                                                                  | Needs a production change; costs a little RAM and a call                                                       |
| Register-level fake        | Runs the real driver, including bit manipulation (expert: VanderVoord)                                            | Does not model read-to-clear, write-one-to-clear, or timing, so the test encodes your reading of the datasheet |
| Test-only alternate root   | A compile-time macro redirects hard-coded paths to a test directory (Linux userspace, not an MCU seam)            | Replaces inputs only; a check that the macro bypasses is no longer tested                                      |

Choose between a fake and a mock by the question the test asks (expert: Memfault).

- A fake is a working, simplified implementation. It survives refactors but costs effort to write correctly.
- A stub returns canned values.
- A mock records calls and returns scripted values. Use one when a stub is not enough and a perfect fake is not worth
  the effort. Memfault found that full branch coverage usually needs mocks, because each `buffer == NULL` branch must be
  forced. A mock pins down call sequences, so it can break on a refactor (inference).

A register-level fake needs no real address, because VanderVoord says it "isn't important". Most microcontrollers have
large register sets, so the work is tedious. Practice 5 covers the registers that change on read.

Mock tooling in the sources: CppUMock, the Fake Function Framework (`fff`, header-only C, bundled by Zephyr as
`zephyr/fff.h`), and CMock, a Ruby generator.

## Adding Tests to an Untested Codebase

Do not write tests for all the existing code at once. Embedded Artistry (expert, 2021-10-25 post) says that "doesn't
make economic sense". It recommends bringing old code under test whenever you are about to change it. The ordered
steps are in "Practices for an Untested MCU Project"; this section keeps the evidence behind them.

- Grenning calls his circular buffer "one of the easier things to test because there are no external dependencies".
  His Zune example is a pure date loop that hangs on the 366th day of a leap year, and one test finds it.
- Grenning (p. 21): "Write tests for the current behavior. Test drive the new behavior. Changing legacy code is
  dangerous." Embedded Artistry accepts "big fat tests" that run the existing code end to end, and refactoring for
  testability later.
- Memfault breaks dependencies by reading the linker's undefined symbols. Each added double can be
  replaced with a better one later.

## Timing and Interrupts

Primary sources on this topic are thin.

Fake clock and direct callback, backed by Grenning's paper (expert, p. 17). He puts time behind a `TimeService`
interface and replaces it in tests with a `FakeTimeService`. The test sets the fake time with `FakeTimeService_SetDay`
and `FakeTimeService_SetMinute`. It then calls the scheduler's wake-up callback directly, "as the RTOS will do in the
product", and checks a spy for the result.

Calling an interrupt service routine directly from a test is an inference from that pattern. The paper does not
discuss interrupt service routines, and no primary source covers it. Apply the inference like this:

- Set the fake register state, then call the handler as an ordinary function. VanderVoord's register fakes make that
  state settable.
- Keep the handler thin. Move its logic into a plain function that takes its inputs as arguments, and test that
  function with controlled inputs.

The same inference gives a clock interface that a test advances by hand (this code is illustrative, not from a source):

```c
typedef struct {
    unsigned long (*now_ms)(void);
} clock_if;

static unsigned long fake_now;
static unsigned long fake_now_ms(void) { return fake_now; }
static const clock_if fake_clock = { fake_now_ms };
```

Other timing tools in the sources:

- Zephyr's ztest has a stress tool, `ZTRESS_EXECUTE`, that runs several contexts with random sleeps and adjusts the CPU
  load to raise the chance of preemption. It runs inside the Zephyr kernel, so it needs `native_sim`, QEMU, or
  hardware (inference). Zephyr advises a much higher tick rate under QEMU.
- Valgrind's Helgrind and DRD, and ThreadSanitizer, check host code that uses pthreads. They cannot see interrupt
  handlers or RTOS tasks on a target (inference).

## Limits of Host Tests

A host test run cannot show these problems (inference; Grenning's stage 3 row lists the last as found on the target):

- Preemption and interrupt latency, because the test runs one thread of control.
- The memory ordering of the real core.
- Peripheral timing.
- Differences in word size, alignment, and endianness, unless the host build matches the target.

A `-m32` build matches pointer and `long` size only (inference). Alignment differs too: x86 tolerates unaligned access
that Cortex-M0 class cores fault on, so UBSan's alignment check (`-fsanitize=undefined`) is the host-side catch.

A register fake or a mock adds a further limit. The test passes against your model of the hardware, so it cannot find
a wrong model.

## Emulation

| Tool                            | What it gives                                                                                                                                                                    | Where it falls short                                                                                                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Renode (MIT licence, 1.17.1)    | Whole-machine emulation with Robot Framework: `renode-test my_test.robot` writes `robot_output.xml`, `log.html`, and `report.html`. Runs under GitHub Actions (expert: Memfault) | Peripheral models are per chip. In Memfault's introduction to Renode the firmware wrote to an unmapped RAM that the model lacked, and the author extended the machine description |
| QEMU system mode, Arm M-profile | Cortex-M0, M4, and M33 machines. The STM32 machines list their supported and missing devices                                                                                     | The documentation says QEMU covers only a small fraction of the Arm ecosystem; machines are generic boards, so vendor peripherals are usually absent                              |
| Zephyr's simulators             | Twister supports `qemu`, `simics`, `xt-sim`, `renode`, `nsim`, `mdb-nsim`, `tsim`, `armfvp`, `native`, and `custom`; `--timeout-multiplier` covers slow simulation               | Not every board has a simulator, and a `build_only` test is never run                                                                                                             |

For Renode under Twister, the platform takes `uart` and `resc` keys. Choose QEMU only when the board has a machine
model, and otherwise Renode (inference).

Emulation validates startup, scheduling, protocol logic, and driver logic against a model. It cannot find errata,
analog behaviour, power problems, electrical bus faults, or DMA and cache subtleties. A test passes or fails against
the model author's reading of the datasheet. Timing-accuracy tests are doubtful in an emulator (inference).

## Hardware in the Loop on a Small Budget

Automated testing on real hardware is hard. Memfault (expert, 2020) says it needs flashers, power
supplies, and software to orchestrate tests and capture results, and offers Renode as the cheaper path. Start with the
smallest runner that works.

- On-device test runner with a serial reporter. Unity routes its output through `UNITY_OUTPUT_CHAR(a)` on a target
  without stdout (doc). A host script that reads Unity's `file:line:test:PASS|FAIL` lines from the serial port is the
  cheapest runner for C (inference). Define `UNITY_EXCLUDE_SETJMP` on a target without setjmp, at the cost of custom
  helper functions and CMock (doc).
- Probe-driven flow. The Rust `embedded-test` harness with `probe-rs run` (doc, docs.rs) reads the test list from the
  ELF and flashes all tests once. It resets the device before each test, selects the test through semihosting
  `SYS_GET_CMDLINE`, and reads the verdict from semihosting `SYS_EXIT`. The tool targets Rust. Semihosting for selection
  and verdict, with a debug probe for flashing, does not depend on the language (inference).
- A board on a desk in CI (inference; no primary source prescribes it). Attach the board, a serial port, and a debug
  probe to a self-hosted runner. The job flashes, resets, reads the verdict, and fails on a non-zero result. Run it
  nightly at first.
- On Linux-class boards, Yocto's `testimage` runs on real hardware through `TEST_TARGET` (see the embedded Linux
  reference).

## Coverage on an MCU

Host coverage with gcov and gcovr is the practical route (inference). Zephyr documents two other routes (doc, coverage
page). The first is gcov on QEMU or a real target, with `CONFIG_COVERAGE=y` and `CONFIG_COVERAGE_DUMP=y`. The second is
gcov on the host through the POSIX architecture. The emulator prints a dump to the console. Save the log, and rebuild
the `.gcda` and `.gcno` files with `scripts/gen_gcov_files.py -i log.log`. Zephyr states that gcov is limited by
available RAM and is enabled only for QEMU emulation of embedded targets.

For a target with no file system, GCC's freestanding-environment page documents `-fprofile-info-section` (default
section `.gcov_info`), so a program can dump the data itself.

## Zephyr: ztest and twister

Zephyr tests run through ztest, with mocks from the Fake Function Framework (`DEFINE_FAKE_VOID_FUN`, and `RESET_FAKE`
in a `ZTEST_RULE`). Twister builds and runs them on the targets from the earlier sections.

- Module logic: the `unit_testing` board. Whole-system logic on the host: `native_sim`. Then QEMU or another simulator,
  then a board.
- Unit tests are Linux-only. On Windows or macOS, Zephyr says to use containers or virtual machines.
- One board: `west twister --device-testing --device-serial /dev/ttyACM0 -p <board> -T tests/...`.
- Several boards: `west twister --generate-hardware-map`, then run with `--hardware-map map.yml`. The map supports the
  flash runners pyocd, nrfjprog, jlink, openocd, and dediprog.
- A device with no serial port: `--device-serial-pty` takes a script that relays messages.
- Special wiring: describe it with a fixture, and reserve a board with `run_with_fixture_only`. A quarantine list skips
  tests that can wedge a board. Reports include JUnit XML.

## ESP-IDF: Unity and pytest-embedded

ESP-IDF uses the Unity framework for tests on the chip, and pytest-embedded runs them.

- Target tests use Unity, and pytest-embedded drives the board.
- Host tests use CMock for mocks on the Linux host, with `target: linux`, and need Ruby on the host. ESP-IDF says only
  a small fraction of its components support host tests, and that they are "still under development".
- QEMU runs use `@pytest.mark.qemu`.

## Practices for an Untested MCU Project

Take these in order. Each step cites its source.

01. Build a host test target next to the firmware build, with its own flags and source list. Run it in CI before you
    write tests. Keep every test double in a test directory, not in the firmware sources. Pick one framework: CppUTest
    or Unity with Ceedling for plain C, Zephyr's `unit_testing` board inside Zephyr, or Unity with pytest-embedded
    inside ESP-IDF (doc: Zephyr, ESP-IDF; expert: Memfault, Grenning stage 1).
02. Test pure logic first: parsers, state machines, protocol code, ring buffers, and fixed-point, conversion, and math
    code. These need no doubles (expert: Grenning, Memfault; Grenning's Zune example).
03. Test code when you change it, not all at once. Write a "big fat" characterization test of today's behaviour before
    the change, then drive the new behaviour (expert: Grenning p. 21, Embedded Artistry 2021-10-25).
04. Cut hardware dependencies one at a time. Compile the module with its test, read the undefined symbols, and add one
    stub, fake, or mock per symbol. Prefer link-time substitution first, because it needs no production change (expert:
    Memfault; doc: CMock).
05. For drivers that must stay register-based, remap the registers to RAM variables under a `TEST` build. Use a
    queue-of-values macro, which returns the next value from a queue the test fills, only for the few registers that
    change on read (expert: VanderVoord). He calls that macro too complex for regular use.
06. When you next change a driver, add a narrow interface, a function-pointer table or an abstract class, between the
    hardware-independent and hardware-dependent code (expert: Embedded Artistry, "Virtual Devices").
07. Keep a CI job that compiles the same sources for the target on every change, so the host and target builds do not
    drift. It catches code that builds on the host but not with the cross compiler (expert: Grenning stage 2). Run the
    host tests under AddressSanitizer and UBSan, and collect gcov coverage on the host (inference for MCU use).
08. Add one emulator smoke test. Boot the real image in Renode or QEMU, and assert on the UART output with Robot
    Framework or a script. Expect to add missing peripheral models (doc: Renode testing page; expert: Memfault).
09. Add one hardware smoke job on a bench board. Flash, reset, and read the serial verdict, nightly at first (doc: Zephyr
    Twister hardware map, or probe-rs; expert: Grenning, "at least nightly").
10. Grow by defect. Give every field bug a regression test at the lowest level that can reproduce it (inference,
    consistent with Grenning's Zune example).
