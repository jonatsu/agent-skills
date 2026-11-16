#!/usr/bin/env bash
#
# verify_skill.sh — reproducible local static safety checks for an agent skill
# before installation. Part of the find-skills skill (L1 of its Verification
# Pipeline). Vendor-independent: relies only on POSIX-ish tools plus optional
# scanners it degrades around when absent.
#
# Checks (each independent; all run):
#   1. Hidden / bidirectional Unicode (zero-width, RTL/LTR overrides, BOM)
#   2. Committed secrets            (betterleaks | gitleaks | trufflehog, else skipped)
#   3. Remote-exec / exfiltration patterns (curl|bash, base64|sh, cred paths)
#   4. Bundled scripts              (shellcheck on *.sh, semgrep if present)
#
# Findings are classed BLOCK (unsafe — do not install) or WARN (review first).
#
# Exit codes:
#   0  clean (no blockers, no warnings)
#   1  warnings only (review before installing)
#   2  one or more blockers (do NOT install)
#   64 usage error
#
# Usage:  verify_skill.sh <skill-dir>
#         verify_skill.sh --help | --version
#
set -Eeuo pipefail
shopt -s inherit_errexit 2> /dev/null || true

readonly SCRIPT_NAME="verify_skill"
readonly VERSION="1.0.0"
readonly EX_USAGE=64
readonly SCAN_TIMEOUT=60

declare -i findings_block=0
declare -i findings_warn=0

trap 'printf "%s: internal error at line %s (exit %s)\n" "$SCRIPT_NAME" "$LINENO" "$?" >&2' ERR

# --- output helpers ---------------------------------------------------------

section() { printf '\n== %s ==\n' "$1"; }
ok() { printf '  [ok]    %s\n' "$1"; }
skip() { printf '  [skip]  %s\n' "$1"; }
warn() {
  printf '  [WARN]  %s\n' "$1"
  findings_warn+=1
}
block() {
  printf '  [BLOCK] %s\n' "$1"
  findings_block+=1
}

usage() {
  cat << EOF
$SCRIPT_NAME $VERSION — local static safety checks for an agent skill.

Usage:
  $SCRIPT_NAME <skill-dir>       Verify the skill directory before install
  $SCRIPT_NAME --help            Show this help
  $SCRIPT_NAME --version         Show version

Exit codes: 0 clean, 1 warnings, 2 blockers, $EX_USAGE usage error.
Optional tools (used when present): betterleaks, gitleaks, trufflehog, shellcheck, semgrep.
EOF
}

# Run an external scanner under a timeout when `timeout` is available.
run_guarded() {
  if command -v timeout > /dev/null 2>&1; then
    timeout "${SCAN_TIMEOUT}s" "$@"
  else
    "$@"
  fi
}

# --- checks -----------------------------------------------------------------

# 1. Hidden / bidirectional Unicode. Prefer PCRE grep; fall back to python3.
check_hidden_unicode() {
  local dir="$1"
  local -a hits=()
  local range='[\x{200b}-\x{200f}\x{202a}-\x{202e}\x{2066}-\x{2069}\x{feff}]'

  if printf '' | grep -qP '' 2> /dev/null; then
    mapfile -t hits < <(grep -rlP "$range" -- "$dir" 2> /dev/null || true)
  elif command -v python3 > /dev/null 2>&1; then
    mapfile -t hits < <(
      python3 - "$dir" << 'PY' || true
import os, sys
bad = set(range(0x200b,0x2010)) | set(range(0x202a,0x202f)) | set(range(0x2066,0x206a)) | {0xfeff}
for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        p = os.path.join(root, f)
        try:
            if any(ord(c) in bad for c in open(p, encoding="utf-8", errors="ignore").read()):
                print(p)
        except OSError:
            pass
PY
    )
  else
    skip "hidden-Unicode scan (no PCRE grep or python3)"
    return 0
  fi

  if ((${#hits[@]})); then
    block "hidden or bidirectional Unicode found (possible instruction hiding):"
    printf '            %s\n' "${hits[@]}"
  else
    ok "no hidden or bidirectional Unicode"
  fi
}

# 2. Committed secrets. The list below is preference order, NOT a requirement:
# any one scanner satisfies the check, and none being present degrades to skip
# rather than failing. Add a scanner by adding a branch — this check MUST NOT
# hard-depend on one tool being installed, since which scanner a machine has
# changes over time.
check_secrets() {
  local dir="$1"
  if command -v betterleaks > /dev/null 2>&1; then
    if run_guarded betterleaks dir "$dir" > /dev/null 2>&1; then
      ok "no secrets (betterleaks)"
    else
      block "betterleaks flagged potential secrets — inspect with: betterleaks dir '$dir' -v"
    fi
  elif command -v gitleaks > /dev/null 2>&1; then
    if run_guarded gitleaks detect --no-git --no-banner --source "$dir" > /dev/null 2>&1; then
      ok "no secrets (gitleaks)"
    else
      block "gitleaks flagged potential secrets — inspect with: gitleaks detect --no-git --source '$dir' -v"
    fi
  elif command -v trufflehog > /dev/null 2>&1; then
    local out
    out="$(run_guarded trufflehog --no-update filesystem "$dir" 2> /dev/null || true)"
    if [[ -n "$out" ]]; then
      block "trufflehog flagged potential secrets — inspect with: trufflehog filesystem '$dir'"
    else
      ok "no secrets (trufflehog)"
    fi
  else
    skip "secret scan (install any of: betterleaks, gitleaks, trufflehog)"
  fi
}

# 3. Remote-exec and exfiltration patterns in text files.
check_dangerous_patterns() {
  local dir="$1"
  local -a exec_hits=() exfil_hits=()

  # curl|bash, wget|sh, base64 -d | sh — remote code execution
  mapfile -t exec_hits < <(
    grep -rInE '(curl|wget)[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(ba)?sh|base64[[:space:]]+(-d|--decode)[^|]*\|[^|]*sh' \
      -- "$dir" 2> /dev/null || true
  )
  if ((${#exec_hits[@]})); then
    block "remote fetch-and-execute pattern (curl|bash / base64|sh):"
    printf '            %s\n' "${exec_hits[@]}"
  else
    ok "no remote fetch-and-execute pattern"
  fi

  # credential/secret paths near network commands — needs human review
  mapfile -t exfil_hits < <(
    grep -rIlnE '\.ssh/|\.aws/credentials|\.env|id_rsa|GITHUB_TOKEN|SECRET|PASSWORD' \
      -- "$dir" 2> /dev/null \
      | xargs -r grep -lE 'curl|wget|nc |ncat|/dev/tcp' 2> /dev/null || true
  )
  if ((${#exfil_hits[@]})); then
    warn "credential paths referenced alongside network commands (review for exfiltration):"
    printf '            %s\n' "${exfil_hits[@]}"
  else
    ok "no obvious credential-exfiltration pattern"
  fi
}

# 4. Static analysis of bundled scripts.
check_bundled_scripts() {
  local dir="$1"
  local -a sh_files=()
  mapfile -d '' sh_files < <(find "$dir" -type f -name '*.sh' -print0 2> /dev/null || true)

  if ((${#sh_files[@]} == 0)); then
    ok "no bundled shell scripts"
  elif command -v shellcheck > /dev/null 2>&1; then
    if run_guarded shellcheck --severity=warning "${sh_files[@]}" > /dev/null 2>&1; then
      ok "bundled shell scripts pass shellcheck"
    else
      warn "shellcheck reported issues in bundled scripts — run: shellcheck ${sh_files[*]}"
    fi
  else
    skip "shellcheck on ${#sh_files[@]} bundled script(s) (install shellcheck)"
  fi

  if command -v semgrep > /dev/null 2>&1; then
    if run_guarded semgrep --error --quiet --config auto "$dir" > /dev/null 2>&1; then
      ok "no semgrep findings"
    else
      warn "semgrep reported findings — run: semgrep --config auto '$dir'"
    fi
  fi
}

# --- main -------------------------------------------------------------------

main() {
  case "${1:-}" in
    -h | --help)
      usage
      return 0
      ;;
    --version)
      printf '%s %s\n' "$SCRIPT_NAME" "$VERSION"
      return 0
      ;;
    "")
      printf '%s: missing <skill-dir>\n\n' "$SCRIPT_NAME" >&2
      usage >&2
      return "$EX_USAGE"
      ;;
  esac

  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    printf '%s: not a directory: %s\n' "$SCRIPT_NAME" "$dir" >&2
    return "$EX_USAGE"
  fi
  if [[ ! -e "$dir/SKILL.md" ]]; then
    warn "no SKILL.md at the directory root — is this a skill?"
  fi

  printf '%s %s — checking: %s\n' "$SCRIPT_NAME" "$VERSION" "$dir"

  section "hidden Unicode"
  check_hidden_unicode "$dir"
  section "secrets"
  check_secrets "$dir"
  section "dangerous patterns"
  check_dangerous_patterns "$dir"
  section "bundled scripts"
  check_bundled_scripts "$dir"

  printf '\n== summary ==\n  %d blocker(s), %d warning(s)\n' \
    "$findings_block" "$findings_warn"

  if ((findings_block > 0)); then
    printf '  VERDICT: UNSAFE — do not install.\n'
    return 2
  elif ((findings_warn > 0)); then
    printf '  VERDICT: REVIEW — resolve warnings before installing.\n'
    return 1
  fi
  printf '  VERDICT: clean.\n'
  return 0
}

# `|| exit` keeps the intentional non-zero verdict (1/2/64) from tripping the
# ERR trap, which is meant only for genuine internal faults.
main "$@" || exit $?
