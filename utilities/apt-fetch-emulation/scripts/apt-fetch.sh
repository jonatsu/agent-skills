#!/bin/sh
# shellcheck shell=sh
# apt-fetch.sh: list or download .deb packages from an APT repository without adding it to the host.
#
# Follows APT's fetch sequence over plain HTTP GET: the signed Release metadata, the Packages index it lists,
# then each selected package. Every index and package is checked against the SHA256 its parent lists, and the
# Release metadata against the given OpenPGP keyring.
#
# Usage: apt-fetch.sh [options] BASEURL SUITE ARCH [PACKAGE[=VERSION]...]
#   BASEURL  archive root, as in a sources.list line (https://deb.debian.org/debian)
#   SUITE    distribution under dists/ (bookworm); a value ending in / names a flat repository directory (./)
#   ARCH     Debian architecture (amd64, arm64, armhf, ...); x86_64 and aarch64 are accepted
# Options:
#   -k FILE  OpenPGP keyring the Release metadata must be signed with (binary format, as gpgv reads it)
#   -U       accept unsigned or unverified Release metadata; checksums then only detect corruption
#   -c COMP  component to read (default main; ignored for a flat repository)
#   -o DIR   download directory (default ./debs-SUITE-ARCH)
#   -l       list the packages the index offers instead of downloading
#   -a       download every package in the index
#
# Exit status: 0 on success, 1 when a fetch or verification fails, 2 on a usage error.

set -u

usage() {
  sed -n '9,21s/^# \{0,1\}//p' "$0" >&2
  exit 2
}

die() {
  printf 'apt-fetch: %s\n' "$*" >&2
  exit 1
}

# The request headers of APT 3.2.0, captured from a live `apt-get update`; override the agent if a repository
# expects another APT release.
APT_UA=${APT_FETCH_USER_AGENT:-"Debian APT-HTTP/1.3 (3.2.0) non-interactive"}

keyring=
unverified=0
component=main
outdir=
mode=select

while getopts k:Uc:o:la opt; do
  case ${opt} in
    k) keyring=${OPTARG} ;;
    U) unverified=1 ;;
    c) component=${OPTARG} ;;
    o) outdir=${OPTARG} ;;
    l) mode=list ;;
    a) mode=all ;;
    *) usage ;;
  esac
done
shift $((OPTIND - 1))
[ "$#" -ge 3 ] || usage

base=${1%/}
suite=$2
arch=$3
shift 3

case ${arch} in
  x86_64) arch=amd64 ;;
  aarch64) arch=arm64 ;;
  *) ;;
esac

if [ "${mode}" = select ] && [ "$#" -eq 0 ]; then
  printf 'apt-fetch: name packages to download, or pass -l to list or -a to download all\n' >&2
  usage
fi
if [ -z "${keyring}" ] && [ "${unverified}" -eq 0 ]; then
  printf 'apt-fetch: pass -k KEYRING to verify the repository, or -U to accept it unverified\n' >&2
  usage
fi
if [ -n "${keyring}" ]; then
  [ -r "${keyring}" ] || die "cannot read keyring: ${keyring}"
  # gpgv looks up a keyring name without a slash in its home directory.
  case ${keyring} in
    */*) ;;
    *) keyring=./${keyring} ;;
  esac
  command -v gpgv > /dev/null 2>&1 || die "gpgv is required to verify signatures"
fi
command -v curl > /dev/null 2>&1 || die "curl is required"

if command -v sha256sum > /dev/null 2>&1; then
  sha256_of() { sha256sum "$1" | awk '{ print $1 }'; }
elif command -v shasum > /dev/null 2>&1; then
  sha256_of() { shasum -a 256 "$1" | awk '{ print $1 }'; }
else
  die "sha256sum or shasum is required"
fi

# A flat repository keeps its Release and Packages files in SUITE itself, with no dists/ tree or components.
case ${suite} in
  */)
    flat=1
    rel_dir=${suite#./}
    rel_dir=${rel_dir%/}
    meta_url=${base}${rel_dir:+/${rel_dir}}
    ;;
  *)
    flat=0
    meta_url=${base}/dists/${suite}
    ;;
esac
if [ -z "${outdir}" ]; then
  suite_label=$(printf '%s' "${suite}" | tr '/' '_' | sed 's/^[._]*//;s/_*$//')
  outdir=./debs-${suite_label:-flat}-${arch}
fi

work=$(mktemp -d) || die "cannot create a temporary directory"
trap 'rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM

fetch() {
  curl -fsSL --proto '=http,https' -A "${APT_UA}" \
    -H "Cache-Control: max-age=0" -H "Accept: text/*" \
    -o "$2" "$1"
}

# Prints a clearsigned message's body, undoing dash-escaping; used only when the signature goes unchecked.
strip_clearsign() {
  awk '
        /^-----BEGIN PGP SIGNED MESSAGE-----/ { header = 1; next }
        header && /^$/ { header = 0; body = 1; next }
        header { next }
        /^-----BEGIN PGP SIGNATURE-----/ { exit }
        body { sub(/^- /, ""); print }
    ' "$1"
}

# Step 1: the Release metadata, verified against the keyring when one is given.
release=${work}/Release
if fetch "${meta_url}/InRelease" "${work}/InRelease" 2> /dev/null; then
  if [ -n "${keyring}" ]; then
    gpgv --keyring "${keyring}" --output "${release}" "${work}/InRelease" 2> "${work}/gpgv.log" \
      || die "InRelease signature does not verify against ${keyring} (an armored key needs gpg --dearmor): $(cat "${work}/gpgv.log")"
  else
    strip_clearsign "${work}/InRelease" > "${release}"
  fi
elif fetch "${meta_url}/Release" "${release}"; then
  if [ -n "${keyring}" ]; then
    fetch "${meta_url}/Release.gpg" "${work}/Release.gpg" || die "no InRelease or Release.gpg under ${meta_url}"
    gpgv --keyring "${keyring}" "${work}/Release.gpg" "${release}" 2> "${work}/gpgv.log" \
      || die "Release signature does not verify against ${keyring} (an armored key needs gpg --dearmor): $(cat "${work}/gpgv.log")"
  fi
else
  die "no InRelease or Release under ${meta_url}"
fi
[ "${unverified}" -eq 1 ] && [ -z "${keyring}" ] \
  && printf 'apt-fetch: WARNING: Release metadata is not authenticated\n' >&2

# Prints "sha256 size" for a path the Release file lists, relative to the Release file's directory.
release_entry() {
  awk -v want="$1" '
        /^[^ \t]/ { in_sha = (tolower($0) ~ /^sha256:/) }
        in_sha && /^[ \t]/ && $3 == want { print $1, $2; exit }
    ' "${release}"
}

# Step 2: a Packages index, in the first compression the Release file lists that fetches and decompresses.
fetch_index() { # index_path_without_extension output_file
  for ext in .xz .gz .bz2 ""; do
    entry=$(release_entry "$1${ext}")
    [ -n "${entry}" ] || continue
    case ${ext} in
      .xz) unpack=xz ;;
      .gz) unpack=gzip ;;
      .bz2) unpack=bzip2 ;;
      *) unpack= ;;
    esac
    [ -z "${unpack}" ] || command -v "${unpack}" > /dev/null 2>&1 || continue
    fetch "${meta_url}/$1${ext}" "${work}/index${ext}" 2> /dev/null || continue
    [ "$(sha256_of "${work}/index${ext}")" = "${entry%% *}" ] \
      || die "checksum mismatch for ${meta_url}/$1${ext}"
    if [ -n "${unpack}" ]; then
      "${unpack}" -dc "${work}/index${ext}" > "$2" || die "cannot decompress $1${ext}"
    else
      cp "${work}/index" "$2" || die "cannot copy $1"
    fi
    printf 'Index: %s\n' "${meta_url}/$1${ext}" >&2
    return 0
  done
  return 1
}

# Prints one tab-separated record per stanza: package, version, architecture, filename, sha256, with "-" for
# an absent field. `read` collapses adjacent tabs, so an empty field would shift the ones after it.
parse_packages() {
  awk '
        function show(v) { return v == "" ? "-" : v }
        function flush() {
            if (pkg != "") print pkg "\t" show(ver) "\t" show(arch) "\t" show(file) "\t" show(sha)
            pkg = ver = arch = file = sha = ""
        }
        /^$/ { flush(); next }
        /^[ \t]/ { next }
        {
            name = tolower(substr($0, 1, index($0, ":") - 1))
            value = substr($0, index($0, ":") + 1)
            sub(/^[ \t]+/, "", value); sub(/[ \t\r]+$/, "", value)
            if (name == "package") pkg = value
            else if (name == "version") ver = value
            else if (name == "architecture") arch = value
            else if (name == "filename") file = value
            else if (name == "sha256") sha = value
        }
        END { flush() }
    ' "$1"
}

records=${work}/records
: > "${records}"
if [ "${flat}" -eq 1 ]; then
  fetch_index Packages "${work}/Packages" || die "no usable Packages index listed in ${meta_url}"
  parse_packages "${work}/Packages" >> "${records}"
else
  fetch_index "${component}/binary-${arch}/Packages" "${work}/Packages" \
    || die "no usable index for ${component}/binary-${arch} in ${meta_url}; check the suite, component, and arch"
  parse_packages "${work}/Packages" >> "${records}"
  # A repository that lists "all" in Architectures publishes Architecture: all packages in a separate index.
  if [ "${arch}" != all ] && awk 'tolower($1) == "architectures:" { for (i = 2; i <= NF; i++) if ($i == "all") f = 1 } END { exit !f }' "${release}"; then
    fetch_index "${component}/binary-all/Packages" "${work}/Packages-all" \
      || die "Release lists architecture all but no usable binary-all index"
    parse_packages "${work}/Packages-all" >> "${records}"
  fi
fi
# Keep only packages this architecture can install; a flat index mixes every architecture.
awk -F '\t' -v a="${arch}" '$3 == a || $3 == "all"' "${records}" | sort -u > "${work}/usable"

if [ "${mode}" = list ]; then
  cut -f 1-3 "${work}/usable" | sort -u
  exit 0
fi

# Step 3: select records, then download and verify each package.
selected=${work}/selected
if [ "${mode}" = all ]; then
  cp "${work}/usable" "${selected}"
else
  : > "${selected}"
  for request in "$@"; do
    name=${request%%=*}
    version=
    case ${request} in
      *=*) version=${request#*=} ;;
      *) ;;
    esac
    awk -F '\t' -v n="${name}" -v v="${version}" '$1 == n && (v == "" || $2 == v)' "${work}/usable" > "${work}/match"
    versions=$(cut -f 2 "${work}/match" | sort -u | tr '\n' ' ')
    case ${versions} in
      "") die "no package ${request} for ${arch} in the index" ;;
      *" "?*) die "${name} has several versions; request one as ${name}=VERSION: ${versions}" ;;
      *) ;;
    esac
    cat "${work}/match" >> "${selected}"
  done
fi

mkdir -p "${outdir}" || die "cannot create ${outdir}"
ok=0
failed=0
tab=$(printf '\t')
while IFS=${tab} read -r pkg ver _ file sha; do
  deb=${file##*/}
  case /${file}/ in
    */../* | */./* | /-/) deb= ;;
    *) ;;
  esac
  case ${deb} in
    "" | . | ..)
      printf 'FAILED: %s %s has an unsafe or missing Filename: %s\n' "${pkg}" "${ver}" "${file}" >&2
      failed=$((failed + 1))
      continue
      ;;
    *) ;;
  esac
  if [ "${sha}" = - ]; then
    printf 'FAILED: %s %s has no SHA256 in the index\n' "${pkg}" "${ver}" >&2
    failed=$((failed + 1))
    continue
  fi
  if fetch "${base}/${file}" "${work}/download" 2> /dev/null \
    && [ "$(sha256_of "${work}/download")" = "${sha}" ] \
    && mv "${work}/download" "${outdir}/${deb}"; then
    ok=$((ok + 1))
    printf '%s\n' "${outdir}/${deb}"
  else
    printf 'FAILED: %s (download or checksum)\n' "${base}/${file}" >&2
    failed=$((failed + 1))
  fi
done < "${selected}"

printf 'Done: %d downloaded, %d failed, into %s\n' "${ok}" "${failed}" "${outdir}" >&2
[ "${failed}" -eq 0 ]
