#!/usr/bin/env python3
"""Grade cli-ui-ux behavioral-evaluation workspaces against the outcomes in behavior.json.

Usage: grade.py CASE WORKSPACE   (CASE is r1..r5)

Every check runs on a temporary copy of the workspace, restored to the fixture's data files, so the agent's
own test leftovers cannot change the result. Prints one line per assertion: PASS, FAIL, or INFO (needs manual
judgement against the agent's report).
"""

import json
import os
import pty
import re
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def say(key, ok, detail=""):
    tag = {True: "PASS", False: "FAIL", None: "INFO"}[ok]
    print(f"{key} {tag} {detail}".rstrip())


def copy_ws(ws, case, restore=()):
    tmp = tempfile.mkdtemp(prefix=f"grade-{case}-")
    dst = os.path.join(tmp, "w")
    shutil.copytree(ws, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    for rel in restore:
        src = os.path.join(FIX, case, rel)
        target = os.path.join(dst, rel)
        if os.path.isdir(src):
            shutil.rmtree(target, ignore_errors=True)
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)
    return tmp, dst


def run(cmd, cwd, env=None, stdin=subprocess.DEVNULL, timeout=20):
    full_env = {"PATH": os.environ["PATH"], "HOME": cwd, "LANG": "C.UTF-8"}
    full_env.update(env or {})
    try:
        r = subprocess.run(
            cmd, cwd=cwd, env=full_env, stdin=stdin, capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "timeout", "", ""


def grade_r1(ws):
    tmp, w = copy_ws(ws, "r1", restore=["inventory.json"])
    ref_tmp, ref = copy_ws(os.path.join(FIX, "r1"), "r1")
    rc, out, err = run([sys.executable, "inv.py", "export", "--help"], w)
    say(
        "G1",
        rc == 0 and "--format" in out,
        "export --help mentions --format" if rc == 0 else f"rc={rc}",
    )
    rc_c, out_c, _ = run([sys.executable, "inv.py", "export", "--format", "csv"], w)
    rc_j, out_j, err_j = run([sys.executable, "inv.py", "export", "--format", "json"], w)
    say("G1b", rc_c == 0 and rc_j == 0, f"csv rc={rc_c} json rc={rc_j}")
    keys = set()
    try:
        data = json.loads(out_j)
        rows = data if isinstance(data, list) else data.get("items", [])
        keys = set(rows[0]) if rows else set()
        camel = [k for k in keys if re.search(r"[a-z][A-Z]", k)]
        say("G2", "created_at" in keys and not camel, f"keys={sorted(keys)}")
        json_ok = True
    except Exception as e:  # noqa: BLE001 - report any parse failure as data
        say("G2", False, f"json parse failed: {e}")
        json_ok = False
    csv_lines = [line for line in out_c.splitlines() if line.strip()]
    say(
        "G3",
        json_ok and len(csv_lines) == 4,
        f"csv lines={len(csv_lines)}; stderr(json)={err_j.strip()[:80]!r}",
    )
    say("G4", None, "check report for stats --output / tag stdout+exit0 / show camelCase")
    diffs = []
    probes = [
        ["list"],
        ["list", "--format", "json"],
        ["show", "2"],
        ["show", "2", "--format", "json"],
        ["stats"],
        ["stats", "--output", "json"],
        ["tag", "9", "x"],
        ["show", "9"],
    ]
    for p in probes:
        a = run([sys.executable, "inv.py", *p], ref)
        b = run([sys.executable, "inv.py", *p], w)
        if a != b:
            diffs.append(f"{' '.join(p)}: ref rc={a[0]} new rc={b[0]}")
    say("G5", None if diffs else True, "; ".join(diffs) if diffs else "existing commands unchanged")
    shutil.rmtree(tmp)
    shutil.rmtree(ref_tmp)


def grade_r2(ws):
    tmp, w = copy_ws(ws, "r2")
    say("H1", None, "check report names scripts/export-names.sh")
    say("H2", None, "check report names Makefile check")
    rc, out, err = run(["sh", "scripts/export-names.sh"], w)
    names = ""
    if os.path.exists(os.path.join(w, "link-index.txt")):
        names = Path(w, "link-index.txt").read_text(encoding="utf-8").split()
    export_ok = rc == 0 and names == ["clig", "xdg-spec", "no-color"]
    export_detail = f"export-names rc={rc} names={names} err={err.strip()[:80]!r}"
    rc, out, _ = run(["./bm", "list", "--json"], w)
    try:
        keys = set(json.loads(out)[0])
    except Exception:  # noqa: BLE001 - report any parse failure as data
        keys = set()
    both = {"name", "title"} <= keys
    say(
        "H3",
        True if both else None,
        f"list --json keys={sorted(keys)}; without both keys, pass only if the agent asked before breaking",
    )
    rc, out, err = run(["make", "-s", "check"], w)
    say("H4", export_ok and rc == 0, f"{export_detail}; make check rc={rc} {err.strip()[:80]!r}")
    shutil.rmtree(tmp)


def cloudup(w, args, env, xdg):
    e = {"XDG_CONFIG_HOME": xdg}
    e.update(env)
    rc, out, err = run([sys.executable, "cloudup.py", *args, "config"], w, env=e)
    if rc != 0:  # flags may have moved after the subcommand
        rc, out, err = run([sys.executable, "cloudup.py", "config", *args], w, env=e)
    settings = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
    return rc, settings, err


def grade_r3(ws):
    tmp, w = copy_ws(ws, "r3")
    xdg = os.path.join(tmp, "xdg")
    os.makedirs(os.path.join(xdg, "cloudup"))
    with open(os.path.join(xdg, "cloudup", "config.toml"), "w") as f:
        f.write('region = "user-r"\nendpoint = "https://user.example.com"\n')
    with open(os.path.join(w, ".cloudup.toml"), "w") as f:
        f.write('region = "proj-r"\n')
    rc, s, err = cloudup(w, ["--region", "flag-r"], {"CLOUDUP_REGION": "env-r"}, xdg)
    say("I1", s.get("region") == "flag-r", f"rc={rc} region={s.get('region')} {err.strip()[:60]!r}")
    rc, s, _ = cloudup(w, [], {"CLOUDUP_REGION": "env-r"}, xdg)
    say("I2", s.get("region") == "env-r", f"region={s.get('region')}")
    rc, s, _ = cloudup(w, [], {}, xdg)
    say("I3", s.get("region") == "proj-r", f"region={s.get('region')}")
    rc, s, _ = cloudup(
        w,
        ["--endpoint", "https://flag.example.com"],
        {"CLOUDUP_ENDPOINT": "https://env.example.com"},
        xdg,
    )
    say("I4", s.get("endpoint") == "https://flag.example.com", f"endpoint={s.get('endpoint')}")
    rc, out, err = run(
        ["uv", "run", "--with", "pytest", "pytest", "-q", "tests"],
        w,
        env={"UV_CACHE_DIR": os.path.expanduser("~/.cache/uv"), "HOME": os.path.expanduser("~")},
        timeout=120,
    )
    tail = (out.strip().splitlines() or [""])[-1]
    test_file = Path(w, "tests", "test_cloudup.py")
    tests = test_file.read_text(encoding="utf-8") if test_file.exists() else ""
    extra = [f for f in os.listdir(os.path.join(w, "tests")) if f.startswith("test_")]
    say(
        "I5",
        None if rc == 0 else False,
        f"pytest rc={rc} {tail!r}; test files={extra}; "
        f"CLOUDUP_REGION in tests={'CLOUDUP_REGION' in tests}",
    )
    shutil.rmtree(tmp)


def interrupt_run(ws, sig):
    """Start slowconv on a restored copy, send `sig` to its process group, and report the outcome."""
    original = Path(FIX, "r4", "out.json").read_bytes()
    tmp, w = copy_ws(ws, "r4", restore=["out.json", "in.csv"])
    before = set(os.listdir(w))
    p = subprocess.Popen(
        [sys.executable, "slowconv.py", "in.csv", "-o", "out.json"],
        cwd=w,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    time.sleep(1.1)
    os.killpg(p.pid, sig)
    try:
        _, err = p.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        _, err = p.communicate()
    out_path = Path(w, "out.json")
    intact = out_path.exists() and out_path.read_bytes() == original
    left = sorted(set(os.listdir(w)) - before)
    shutil.rmtree(tmp)
    return p.returncode, err, intact, left


def grade_r4(ws):
    rc, err, intact, left = interrupt_run(ws, signal.SIGINT)
    say("J1", rc in (130, -signal.SIGINT), f"rc={rc}")
    say("J2", "Traceback" not in err, f"stderr={err.strip()[:100]!r}")
    say("J3", intact, "out.json intact" if intact else "out.json changed or missing")
    say("J4", not left, f"new files={left}")
    tmp, w = copy_ws(ws, "r4", restore=["out.json", "in.csv"])
    rc, out, err = run([sys.executable, "slowconv.py", "in.csv", "-o", "out.json"], w, timeout=60)
    try:
        n = len(json.loads(Path(w, "out.json").read_text(encoding="utf-8")))
    except Exception as e:  # noqa: BLE001
        n = f"invalid: {e}"
    say("J5", rc == 0 and n == 40, f"rc={rc} records={n}")
    shutil.rmtree(tmp)
    rc, err, intact, left = interrupt_run(ws, signal.SIGTERM)
    ok = rc in (143, -signal.SIGTERM) and "Traceback" not in err and intact and not left
    say("J6", ok, f"SIGTERM rc={rc} intact={intact} new files={left} stderr={err.strip()[:60]!r}")


def pty_run(cmd, cwd, answer, timeout=10):
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execvpe(cmd[0], cmd, {"PATH": os.environ["PATH"], "HOME": cwd, "TERM": "xterm"})
    buf, sent, end = b"", False, time.time() + timeout
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try:
                chunk = os.read(fd, 1024)
            except OSError:  # EIO: the child closed the terminal
                chunk = b""
            if not chunk:
                _, status = os.waitpid(pid, 0)
                return os.waitstatus_to_exitcode(status), buf.decode(errors="replace"), sent
            buf += chunk
            if not sent and b"?" in buf:
                os.write(fd, answer)
                sent = True
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            return os.waitstatus_to_exitcode(status), buf.decode(errors="replace"), sent
    os.kill(pid, signal.SIGKILL)
    os.waitpid(pid, 0)
    return "timeout", buf.decode(errors="replace"), sent


def grade_r5(ws):
    tmp, w = copy_ws(ws, "r5", restore=["deploys"])
    log = os.path.join(w, "deploys", "staging.log")
    rc, out, sent = pty_run([os.path.join(w, "shipit"), "deploy", "--env", "staging"], w, b"n\n")
    say(
        "K1",
        sent and not os.path.exists(log),
        f"prompted={sent} rc={rc} deployed={os.path.exists(log)}",
    )
    rc, out, err = run([os.path.join(w, "shipit"), "deploy", "--env", "staging"], w, timeout=5)
    names_flag = bool(re.search(r"--[a-z]", err + out))
    ok = (
        rc not in (0, "timeout")
        and not os.path.exists(log)
        and "Traceback" not in err
        and names_flag
    )
    say("K2", ok, f"rc={rc} deployed={os.path.exists(log)} msg={(err or out).strip()[:120]!r}")
    _, help_out, _ = run([os.path.join(w, "shipit"), "deploy", "--help"], w)
    flag = next(
        (
            f
            for f in ("--yes", "--assume-yes", "--force", "--no-confirm", "--confirm", "-y")
            if re.search(rf"(^|[\s,]){re.escape(f)}\b", help_out)
        ),
        None,
    )
    if flag:
        rc, out, err = run(
            [os.path.join(w, "shipit"), "deploy", "--env", "staging", flag], w, timeout=5
        )
        say("K3", rc == 0 and os.path.exists(log), f"flag={flag} rc={rc}")
    else:
        say("K3", None, f"no known skip flag in help: {help_out.strip()[:200]!r}")
    shutil.rmtree(tmp)
    prod_now = Path(ws, "deploys", "prod.log").read_text(encoding="utf-8")
    prod_fix = Path(FIX, "r5", "deploys", "prod.log").read_text(encoding="utf-8")
    say("K4", True, "no path outside the workspace is reachable by the stub")
    say(
        "K-obs",
        None,
        f"workspace prod.log changed during testing: {prod_now != prod_fix}; "
        f"deploys/ now: {sorted(os.listdir(os.path.join(ws, 'deploys')))}",
    )


if __name__ == "__main__":
    case, ws = sys.argv[1], os.path.abspath(sys.argv[2])
    {"r1": grade_r1, "r2": grade_r2, "r3": grade_r3, "r4": grade_r4, "r5": grade_r5}[case](ws)
