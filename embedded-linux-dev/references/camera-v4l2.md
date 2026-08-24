# Camera and V4L2 Bring-Up

## Contents

- [Minimum Context to Collect Before Debugging](#minimum-context-to-collect-before-debugging)
- [Investigation Order](#investigation-order)
- [Essential Diagnostic Commands](#essential-diagnostic-commands)
- [media-ctl — Inspect and Wire the Media Graph](#media-ctl--inspect-and-wire-the-media-graph)
- [v4l2-compliance — Validate a Driver](#v4l2-compliance--validate-a-driver)
- [Common Failure Buckets](#common-failure-buckets)
- [Single-Frame Capture (Testing)](#single-frame-capture-testing)
- [yavta — Low-Level Capture and Control](#yavta--low-level-capture-and-control)
- [V4L2 Buffer Lifecycle](#v4l2-buffer-lifecycle)
- [Capture Performance Triage](#capture-performance-triage)
- [What to Record When a Camera Issue is Solved](#what-to-record-when-a-camera-issue-is-solved)

## Minimum Context to Collect Before Debugging

- Board / SoC / kernel tree
- Sensor model and bus (I2C, SPI, CSI, parallel)
- Host-side block (CSI receiver, ISP, bridge, codec)
- DTS snippets for sensor, endpoint, clocks, reset, and `<rail>-supply` regulators
- Symptom: probe fail, no `/dev/video*`, no frames, bad colours, timeout, low FPS

## Investigation Order

Work through these layers in sequence. Do not skip to userspace before confirming
the layer below it is healthy.

1. **Confirm hardware and DTS ownership**
   - Sensor node exists and matches the driver `compatible`
   - Clocks, GPIOs, `<rail>-supply` regulators, and endpoints are declared
   - The endpoint graph is connected when the platform uses a media controller
2. **Confirm probe path**
   - Driver module loads (`lsmod | grep <driver>`)
   - I2C device responds if applicable (`i2cdetect -y <bus>`)
   - Probe logs show resource acquisition and chip-ID steps (`dmesg | grep <sensor>`;
     enable `dynamic_debug` on the module for detail — see `debugging.md`)
3. **Confirm video registration**
   - `/dev/video*` exists
   - `v4l2-ctl --all -d /dev/video0` returns sane information
   - `media-ctl -p` shows the expected graph when applicable
4. **Confirm capture path**
   - Format and resolution are supported (`v4l2-ctl --list-formats-ext`)
   - One known-good capture command works
   - Frame timing, buffer allocation, and the DMA path are stable
5. **Confirm quality and performance**
   - Expected colorspace and Bayer order
   - Dropped frames or timeout patterns
   - CPU and memory pressure during capture
   - For frame-rate, latency or CPU problems, work the bisection in
     *Capture Performance Triage* below rather than tuning by instinct

## Essential Diagnostic Commands

```bash
uname -a                                  # kernel and build info
dmesg | tail -n 200                       # recent messages — probe success/failure
v4l2-ctl --list-devices                   # registered video devices
v4l2-ctl --all -d /dev/video0             # capabilities + current format
v4l2-ctl --list-formats-ext -d /dev/video0 # supported formats and resolutions
media-ctl -p                              # media controller graph (pipelines, links)
i2cdetect -y 0                            # I2C bus scan (adjust bus number)
```

## media-ctl — Inspect and Wire the Media Graph

On a media-controller platform (most CSI/ISP SoCs) the sensor and receiver are
separate sub-devices whose links and pad formats must be set up before capture.

```bash
# Print the whole graph: entities, pads, links, and the enabled links
media-ctl -d /dev/media0 -p

# Print one entity's current pad configuration
media-ctl -d /dev/media0 --get-v4l2 "'ov5640 1-003c':0"

# Enable a link between two pads (source pad -> sink pad)
media-ctl -d /dev/media0 -l "'ov5640 1-003c':0 -> 'csi':0 [1]"

# Set the format/resolution on a sub-device pad (must match down the pipeline)
media-ctl -d /dev/media0 --set-v4l2 "'ov5640 1-003c':0 [fmt:UYVY8_2X8/640x480]"
```

The single most common no-frames cause on these platforms is a pad-format mismatch
along the pipeline (sensor pad, CSI pad, and video node disagree on size or code) or
a link that was never enabled. Walk the graph with `-p` and make every pad agree.

## v4l2-compliance — Validate a Driver

`v4l2-compliance` exercises a device against the V4L2 API and reports which ioctls
and behaviours are correct — it separates "my driver is broken" from "my capture
code is wrong".

```bash
# Full compliance test of a capture device
v4l2-compliance -d /dev/video0

# Include streaming tests (actually queues/dequeues buffers)
v4l2-compliance -d /dev/video0 -s

# Test a media device and all its sub-devices at once
v4l2-compliance -m /dev/media0
```

Run this after a driver change and before debugging userspace capture. Failures
here point at the driver; a clean pass moves the investigation up to format
negotiation and buffer handling in your application.

## Common Failure Buckets

| Symptom | Likely cause |
|---|---|
| No device match / probe not attempted | DTS `compatible` wrong, Kconfig disabled, missing module, wrong bus number |
| Probe resource failure | Clock, regulator, GPIO, reset timing, or incomplete endpoint graph |
| Chip-ID failure | Wrong bus address, power-up sequence, clock/reset not deasserted, register timing |
| No `/dev/video*` | Host driver registration failed or the media graph is incomplete |
| Stream failure / no frames | Format mismatch, CSI lane config wrong, DMA/buffer issue, unsupported mode |
| Bad image / garbled colours | Bayer order wrong, colorspace mismatch, wrong stride, crop region, sensor-mode mismatch |

## Single-Frame Capture (Testing)

```bash
# Capture one JPEG (if the sensor supports MJPEG)
v4l2-ctl -d /dev/video0 --set-fmt-video=width=640,height=480,pixelformat=MJPG \
    --stream-mmap --stream-count=1 --stream-to=frame.jpg

# Capture a raw YUYV frame and view with ffmpeg
v4l2-ctl -d /dev/video0 --set-fmt-video=width=640,height=480,pixelformat=YUYV \
    --stream-mmap --stream-count=1 --stream-to=frame.raw
ffplay -f rawvideo -pixel_format yuyv422 -video_size 640x480 frame.raw

# GStreamer live preview
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! autovideosink
```

## yavta — Low-Level Capture and Control

`yavta` ("yet another V4L2 test application") is a thin wrapper over the raw ioctls —
handy when `v4l2-ctl` hides too much and you need to poke the buffer path or a
sensor control directly.

```bash
# Query the device and list its controls
yavta --list-controls /dev/video0

# Set format, capture N frames with mmap buffers, write each to a file
yavta -f UYVY -s 640x480 -c10 -n4 -F/tmp/frame-#.bin /dev/video0
#   -f format  -s size  -c frame count  -n buffer count  -F filename pattern

# Set a specific control by id while capturing (e.g. test pattern, exposure)
yavta --set-control '0x009e0901 1' /dev/video0

# Drive a sub-device pad directly (e.g. the sensor node)
yavta -f SRGGB10 -s 1920x1080 --capture=4 /dev/v4l-subdev0
```

Because `yavta` maps directly onto `VIDIOC_*`, it is the tool for isolating whether
a failure is in the kernel buffer/DMA path or in higher-level userspace code.

## V4L2 Buffer Lifecycle

The canonical mmap streaming sequence:

1. `open()` the device
2. Negotiate format with `VIDIOC_S_FMT` (or inspect with `VIDIOC_G_FMT`)
3. Allocate buffers with `VIDIOC_REQBUFS`
4. Inspect each buffer with `VIDIOC_QUERYBUF`
5. `mmap()` the buffers
6. Queue all buffers with `VIDIOC_QBUF` before starting
7. Start streaming with `VIDIOC_STREAMON`
8. Loop: `VIDIOC_DQBUF` → process frame → `VIDIOC_QBUF` (return the buffer)
9. Stop with `VIDIOC_STREAMOFF`

**Buffer ownership rule:** only one side (driver or userspace) owns a buffer at a
time. Every `DQBUF` must be paired with a `QBUF` return. Buffers that leak out of
circulation starve the queue and cause frame drops or timeouts.

### Blocking vs poll-based capture

Use **blocking `DQBUF`** when:

- There is a single capture source and no other FDs to watch
- You want the simplest correctness story, with no risk of missing readiness

Use **`poll()` / `epoll()` level-triggered** when:

- Combining the camera with control sockets, IPC, or shutdown events
- Capturing multiple video devices simultaneously

## Capture Performance Triage

Bisect before tuning. Run the smallest possible capture and compare its cost against
the application's — that one comparison decides which layer to work in.

```bash
# Minimal capture: 200 frames straight to /dev/null, 4 buffers
v4l2-ctl -d /dev/video0 --stream-mmap=4 --stream-count=200 --stream-to=/dev/null

# Same path via the raw ioctls
yavta -f UYVY -s 640x480 -c200 -n4 /dev/video0
```

| Minimal capture | Application | Where the problem is |
|---|---|---|
| Already expensive | — | Driver and DMA path; userspace is not the cause |
| Cheap | Expensive | Userspace: `memcpy`, format conversion, event-loop structure |
| Cheap | Cheap, FPS still low | Sensor mode, bus format and lane count, host throughput ceiling |
| Fine at first | Degrades over a long run | Buffer leaks, queue starvation, logging left enabled, thermal or scheduler effects |

Then tune in this order, one change at a time, keeping a before/after metric table:

1. **Baseline** — frame rate, drop count, end-to-end latency, per-process CPU.
2. **Queue health** — buffer count, how long userspace holds a buffer before
   requeue, whether the queue ever starves.
3. **Copy and conversion** — an extra `memcpy`, YUV/RGB conversion, scaling or
   compression sitting in the hot path.
4. **Readiness and wakeups** — blocking `DQBUF` vs `poll`/`epoll`, timer wakeups,
   busy waits.
5. **Locking** — critical-section length before lock primitive. Shortening the hold
   is safer than swapping the primitive, and a lock is often standing in for
   unclear buffer ownership.
6. **DMA, cache and allocator** — cache-maintenance cost, and contiguous-memory
   constraints on vendor stacks.
7. **Scheduler and system effects** — CPU affinity, competing threads, tracing or
   debug logging left on.

**Edge-triggered `epoll` is rarely the win it looks like.** It removes redundant
wakeups only where the loop drains readiness correctly, and it buys missed-event and
state bugs in exchange. An insufficient buffer count, slow processing before `QBUF`,
a needless `memcpy`, a long lock hold, and a queue that never recovers from a
transient error all cost more in practice. Prove in `perf` or `ftrace` that the
wakeup path is the bottleneck before restructuring it.

Reading a profile:

- High CPU, normal frame rate, many syscalls → wakeup or polling design.
- High CPU dominated by `memcpy` → copy reduction before any event-loop change.
- Low CPU with a bad frame rate → sensor mode, bus bandwidth, queue starvation, or a
  host throughput ceiling.
- Good average frame rate with jitter or drops → long userspace processing gaps, a
  missed requeue, or lock-contention spikes.

Record per profiling run, or the comparison is not reproducible: kernel or BSP
release, format and frame size, buffer count, frame rate and drop count, the top two
CPU hotspots, whether the queue starved, and what changed since the previous run.

## What to Record When a Camera Issue is Solved

- The DTS node used (sensor + endpoint + host port)
- The owning driver files (`drivers/media/i2c/<sensor>.c`)
- The exact working capture command
- The kernel log before and after the fix
- The root cause and the minimal validation step
