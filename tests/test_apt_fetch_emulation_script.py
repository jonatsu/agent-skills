"""Behavioral tests for apt-fetch-emulation's apt-fetch.sh against a local, signed APT repository fixture."""

from __future__ import annotations

import functools
import gzip
import hashlib
import http.server
import lzma
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import override

from skill_locator import skill_directory

SCRIPT = skill_directory("apt-fetch-emulation") / "scripts" / "apt-fetch.sh"

EXIT_FAILED = 1
EXIT_USAGE = 2


@dataclass(frozen=True)
class Deb:
    name: str
    version: str
    arch: str
    corrupt: bool = False

    @property
    def filename(self) -> str:
        return f"pool/main/{self.name[0]}/{self.name}/{self.name}_{self.version}_{self.arch}.deb"

    @property
    def content(self) -> bytes:
        return f"fake deb {self.name} {self.version} {self.arch}\n".encode()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _packages_index(debs: list[Deb], prefix: str = "") -> bytes:
    stanzas: list[str] = []
    for deb in debs:
        listed_sha = _sha256(b"something else" if deb.corrupt else deb.content)
        fields = [
            f"Package: {deb.name}",
            f"Version: {deb.version}",
            f"Architecture: {deb.arch}",
            f"Filename: {prefix}{deb.filename}",
            f"Size: {len(deb.content)}",
            f"SHA256: {listed_sha}",
            "Description: fixture",
            " continuation line",
        ]
        stanzas.append("\n".join(fields) + "\n")
    return "\n".join(stanzas).encode()


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_bytes(data)


def _release(indices: dict[str, bytes], architectures: str) -> str:
    lines = [f"Suite: fixture\nArchitectures: {architectures}\nComponents: main\nSHA256:"]
    lines += [f" {_sha256(data)} {len(data)} {path}" for path, data in sorted(indices.items())]
    return "\n".join(lines) + "\n"


def _gpg(home: Path, *args: str) -> None:
    _ = subprocess.run(
        ["gpg", "--homedir", str(home), "--batch", "--quiet", *args],
        check=True,
        capture_output=True,
    )


def _make_key(home: Path, uid: str, keyring: Path) -> None:
    home.mkdir(mode=0o700)
    _gpg(home, "--passphrase", "", "--quick-gen-key", uid, "ed25519", "sign", "never")
    _gpg(home, "--output", str(keyring), "--export", uid)


def _build_suite(
    root: Path, suite: str, by_arch: dict[str, list[Deb]], home: Path, *, tamper: bool = False
) -> None:
    """Write a dists/ suite whose InRelease is clearsigned with the key in `home`."""
    indices: dict[str, bytes] = {}
    for arch, debs in by_arch.items():
        index = _packages_index(debs)
        indices[f"main/binary-{arch}/Packages"] = index
        indices[f"main/binary-{arch}/Packages.xz"] = lzma.compress(index)
        indices[f"main/binary-{arch}/Packages.gz"] = gzip.compress(index)
        for deb in debs:
            _write(root / deb.filename, deb.content)
    suite_dir = root / "dists" / suite
    for path, data in indices.items():
        _write(suite_dir / path, data)
    release = _release(indices, " ".join(by_arch))
    if tamper:
        _write(suite_dir / "main/binary-amd64/Packages.xz", lzma.compress(b"Package: swapped\n"))
    _write(suite_dir / "Release", release.encode())
    _gpg(home, "--output", str(suite_dir / "InRelease"), "--clearsign", str(suite_dir / "Release"))
    (suite_dir / "Release").unlink()


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    @override
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - signature fixed by the base class
        pass


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("gpg", "gpgv", "curl", "xz")),
    "needs gpg, gpgv, curl and xz",
)
class AptFetchTests(unittest.TestCase):
    """The script lists and downloads only what verifies, and refuses everything else."""

    HELLO_1 = Deb("hello", "1.0", "amd64")
    HELLO_2 = Deb("hello", "2.0", "amd64")
    DOCS = Deb("docs", "1.0", "all")
    ARM_ONLY = Deb("armonly", "1.0", "arm64")
    CORRUPT = Deb("broken", "1.0", "amd64", corrupt=True)

    out: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls._tmp.name)
        root = tmp / "www"
        cls.keyring = tmp / "repo.gpg"
        cls.other_keyring = tmp / "other.gpg"
        home = tmp / "gnupg"
        _make_key(home, "Fixture Repo <repo@example.com>", cls.keyring)
        _make_key(tmp / "other-gnupg", "Other <other@example.com>", cls.other_keyring)

        standard = {"amd64": [cls.HELLO_1, cls.HELLO_2], "arm64": [cls.ARM_ONLY], "all": [cls.DOCS]}
        _build_suite(root, "stable", standard, home)
        _build_suite(root, "corrupt", {"amd64": [cls.CORRUPT]}, home)
        _build_suite(root, "tampered", {"amd64": [cls.HELLO_1]}, home, tamper=True)

        # A flat repository: indices under flat/, Filename relative to the archive root, no signature.
        flat_index = _packages_index([cls.HELLO_1, cls.ARM_ONLY], prefix="flat/")
        _write(root / "flat" / "Packages", flat_index)
        _write(
            root / "flat" / "Release", _release({"Packages": flat_index}, "amd64 arm64").encode()
        )
        for deb in (cls.HELLO_1, cls.ARM_ONLY):
            _write(root / "flat" / deb.filename, deb.content)

        handler = functools.partial(_QuietHandler, directory=str(root))
        cls._server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls._server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls._server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls._server.shutdown()
        cls._server.server_close()
        cls._tmp.cleanup()

    def setUp(self) -> None:
        self.out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.out)

    def _run(
        self, *args: str, keyring: Path | None = None, signed: bool = True
    ) -> subprocess.CompletedProcess[str]:
        options = ["-k", str(keyring or self.keyring)] if signed else []
        env = {
            key: value for key, value in os.environ.items() if not key.lower().endswith("_proxy")
        }
        return subprocess.run(
            ["sh", str(SCRIPT), *options, "-o", str(self.out / "debs"), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def _downloaded(self) -> list[str]:
        return (
            sorted(path.name for path in (self.out / "debs").glob("*"))
            if (self.out / "debs").exists()
            else []
        )

    def test_list_includes_the_all_index_and_excludes_other_architectures(self) -> None:
        result = self._run("-l", self.base, "stable", "x86_64")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(), ["docs\t1.0\tall", "hello\t1.0\tamd64", "hello\t2.0\tamd64"]
        )

    def test_download_of_a_pinned_version_verifies_and_lands(self) -> None:
        result = self._run(self.base, "stable", "amd64", "hello=2.0", "docs")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self._downloaded(), ["docs_1.0_all.deb", "hello_2.0_amd64.deb"])
        self.assertEqual(
            (self.out / "debs" / "hello_2.0_amd64.deb").read_bytes(), self.HELLO_2.content
        )

    def test_ambiguous_version_fails_and_names_the_versions(self) -> None:
        result = self._run(self.base, "stable", "amd64", "hello")
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertIn("1.0 2.0", result.stderr)
        self.assertEqual(self._downloaded(), [])

    def test_unknown_package_fails(self) -> None:
        result = self._run(self.base, "stable", "amd64", "armonly")
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertIn("no package armonly", result.stderr)

    def test_package_checksum_mismatch_leaves_no_file(self) -> None:
        result = self._run("-a", self.base, "corrupt", "amd64")
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertIn("FAILED", result.stderr)
        self.assertEqual(self._downloaded(), [])

    def test_index_checksum_mismatch_fails(self) -> None:
        result = self._run("-l", self.base, "tampered", "amd64")
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertIn("checksum mismatch", result.stderr)

    def test_signature_from_another_key_fails(self) -> None:
        result = self._run("-l", self.base, "stable", "amd64", keyring=self.other_keyring)
        self.assertEqual(result.returncode, EXIT_FAILED)
        self.assertIn("does not verify", result.stderr)

    def test_missing_trust_decision_is_a_usage_error(self) -> None:
        result = self._run("-l", self.base, "stable", "amd64", signed=False)
        self.assertEqual(result.returncode, EXIT_USAGE)
        self.assertIn("-k KEYRING", result.stderr)

    def test_missing_selection_is_a_usage_error(self) -> None:
        result = self._run(self.base, "stable", "amd64")
        self.assertEqual(result.returncode, EXIT_USAGE)

    def test_flat_repository_unverified_downloads_with_a_warning(self) -> None:
        result = self._run("-U", self.base, "flat/", "amd64", "hello", signed=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not authenticated", result.stderr)
        self.assertEqual(self._downloaded(), ["hello_1.0_amd64.deb"])


if __name__ == "__main__":
    unittest.main()
