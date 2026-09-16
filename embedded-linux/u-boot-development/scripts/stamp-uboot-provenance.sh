#!/usr/bin/env bash
# Record a quiescent build using caller-supplied build-time identity evidence.
set -euo pipefail

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

if (($# < 5)); then
  printf 'Usage: %s SOURCE_ROOT BUILD_DIR NEW_RECORD BUILD_IDENTITY ARTIFACT [ARTIFACT ...]\n' "${0##*/}" >&2
  exit 2
fi

for tool in cat git sha256sum realpath dirname basename mktemp ln rm date; do
  command -v "$tool" > /dev/null || fail "missing required tool: $tool"
done
for operand in "$@"; do
  [[ $operand == /* ]] || fail "all paths must be absolute: $operand"
done

source_root=$(realpath -e -- "$1") || fail "cannot resolve source root: $1"
build_dir=$(realpath -e -- "$2") || fail "cannot resolve build directory: $2"
record=$3
identity=$4
shift 4
[[ -d $source_root && -d $build_dir ]] || fail 'source and build paths must be directories'
source_top=$(git -C "$source_root" rev-parse --show-toplevel) || fail "not a Git source tree: $source_root"
[[ $source_top == "$source_root" ]] || fail "source must be the Git root: $source_top"
[[ ! -e $record && ! -L $record ]] || fail "output already exists: $record"
record_parent=$(dirname -- "$record") || fail "cannot resolve output parent: $record"
record_parent=$(realpath -e -- "$record_parent") || fail "output parent does not exist: $record"
[[ -d $record_parent ]] || fail "output parent is not a directory: $record_parent"
record_name=$(basename -- "$record") || fail "cannot resolve output name: $record"
record="$record_parent/$record_name"
[[ -s $identity && -f $identity && -r $identity ]] || fail "build identity must be a nonempty readable file: $identity"
config="$build_dir/.config"
[[ -s $config && -f $config && -r $config ]] || fail "effective config must be a nonempty readable file: $config"

files=("$identity" "$config" "$@")
hashes=()
for file in "${files[@]}"; do
  [[ -f $file && -r $file ]] || fail "required input is not a readable regular file: $file"
  sum=$(sha256sum < "$file") || fail "cannot hash required input: $file"
  hash=${sum%% *}
  [[ $hash =~ ^[0-9a-f]{64}$ ]] || fail "invalid SHA-256 result for: $file"
  hashes+=("$hash")
done
revision=$(git -C "$source_root" rev-parse --verify HEAD) || fail 'cannot resolve source HEAD'
status=$(git -C "$source_root" status --porcelain=v1 --untracked-files=all) || fail 'cannot inspect source state'
identity_text=$(cat -- "$identity") || fail "cannot read build identity: $identity"
timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ) || fail 'cannot obtain timestamp'

umask 077
record_tmp=$(mktemp -- "$record_parent/.uboot-provenance.XXXXXXXX") || fail 'cannot create temporary record'
cleanup() {
  local result=$?
  trap - EXIT
  if ! rm -f -- "$record_tmp"; then
    printf 'error: cannot remove temporary record: %s\n' "$record_tmp" >&2
    ((result != 0)) || result=1
  fi
  exit "$result"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

{
  printf 'u-boot build evidence v1\n' || fail 'cannot write record header'
  printf 'captured_at: %s\nsource_root: %q\nbuild_dir: %q\n' "$timestamp" "$source_root" "$build_dir" || fail 'cannot write paths'
  printf 'source_head_at_capture: %s\nsource_status_at_capture: %q\n' "$revision" "$status" || fail 'cannot write source state'
  printf 'caller_build_identity: %q\n' "$identity_text" || fail 'cannot write identity'
  printf 'sha256 (identity, effective config, then required artifacts):\n' || fail 'cannot write digest header'
  for index in "${!files[@]}"; do
    printf '%s  %q\n' "${hashes[$index]}" "${files[$index]}" || fail 'cannot write digest'
  done
} > "$record_tmp" || fail 'cannot write complete record'

# A hard link publishes complete content without replacing a concurrent writer.
ln -T -- "$record_tmp" "$record" || fail "cannot publish new record without replacement: $record"
printf 'wrote %s\n' "$record"
