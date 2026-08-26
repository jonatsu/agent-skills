#!/usr/bin/env python3
"""Tests for check_corpus.py.

Standard-library ``unittest`` rather than pytest, for the same reason the
script under test has no dependencies: this ships inside a skill and must run
wherever python3 does.

Run from anywhere:

    python3 skills/shared/design/design-forge/scripts/test_check_corpus.py

Or, from this directory:

    python3 -m unittest test_check_corpus -v
"""

from __future__ import annotations

import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# The module under test is this file's own sibling, so its directory is
# located by identity rather than by counting parents off a known layout.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_corpus as cc  # noqa: E402

VALID = """---
type: design
lifecycle: active
owns:
  - alpha
---

# Alpha
"""


def write(root: Path, name: str, text: str) -> Path:
    """Write one document into the corpus and return its path."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def run_checks(root: Path) -> cc.Report:
    """Load and check every document under root, as main() does."""
    report = cc.Report()
    docs = [
        doc
        for path in cc.collect(root, None)
        if (doc := cc.load(path, root, report)) is not None
    ]
    for doc in docs:
        cc.check_fields(doc, report)
        cc.check_length(doc, report)
        cc.check_amendments(doc, report)
    cc.check_ownership(docs, report)
    return report


def joined(messages: list[str]) -> str:
    """Collapse findings into one searchable string."""
    return "\n".join(messages)


class TempCorpus(unittest.TestCase):
    """Base class giving each test an empty corpus directory."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)


# --------------------------------------------------------------------------
# parser
# --------------------------------------------------------------------------


class StripCommentTests(unittest.TestCase):
    def test_removes_trailing_comment(self) -> None:
        self.assertEqual(cc.strip_comment(" true   # frozen"), "true")

    def test_keeps_hash_inside_quotes(self) -> None:
        self.assertEqual(cc.strip_comment(' "a # b"'), '"a # b"')

    def test_keeps_hash_not_preceded_by_space(self) -> None:
        self.assertEqual(cc.strip_comment(" issue#7"), "issue#7")

    def test_whole_value_commented_out(self) -> None:
        self.assertEqual(cc.strip_comment(" # nothing here"), "")


class CoerceScalarTests(unittest.TestCase):
    def test_booleans(self) -> None:
        self.assertIs(cc.coerce_scalar("true"), True)
        self.assertIs(cc.coerce_scalar("false"), False)

    def test_unwraps_matched_quotes(self) -> None:
        self.assertEqual(cc.coerce_scalar('"design"'), "design")
        self.assertEqual(cc.coerce_scalar("'design'"), "design")

    def test_bare_string_passes_through(self) -> None:
        self.assertEqual(cc.coerce_scalar("design"), "design")

    def test_number_stays_a_string(self) -> None:
        self.assertEqual(cc.coerce_scalar("30"), "30")


class ParseValueTests(unittest.TestCase):
    def test_inline_list(self) -> None:
        self.assertEqual(cc.parse_value(" [a, b]"), ["a", "b"])

    def test_empty_inline_list(self) -> None:
        self.assertEqual(cc.parse_value(" []"), [])

    def test_scalar(self) -> None:
        self.assertEqual(cc.parse_value(" design # note"), "design")


class SplitFrontmatterTests(unittest.TestCase):
    def test_ok(self) -> None:
        status, block, body = cc.split_frontmatter(["---", "a: 1", "---", "x"])
        self.assertEqual(status, "ok")
        self.assertEqual(block, ["a: 1"])
        self.assertEqual(body, 3)

    def test_absent(self) -> None:
        status, _, _ = cc.split_frontmatter(["# Title"])
        self.assertEqual(status, "absent")

    def test_absent_on_empty_file(self) -> None:
        status, _, _ = cc.split_frontmatter([])
        self.assertEqual(status, "absent")

    def test_unterminated(self) -> None:
        status, _, _ = cc.split_frontmatter(["---", "a: 1"])
        self.assertEqual(status, "unterminated")


class ParseFrontmatterTests(unittest.TestCase):
    def test_block_list(self) -> None:
        fields, errors = cc.parse_frontmatter(["owns:", "  - a", "  - b"])
        self.assertEqual(fields, {"owns": ["a", "b"]})
        self.assertEqual(errors, [])

    def test_comment_and_blank_lines_ignored(self) -> None:
        fields, errors = cc.parse_frontmatter(["# c", "", "type: design"])
        self.assertEqual(fields, {"type": "design"})
        self.assertEqual(errors, [])

    def test_nested_mapping_fails_closed(self) -> None:
        _, errors = cc.parse_frontmatter(["meta:", "  author: x"])
        self.assertEqual(len(errors), 1)
        self.assertIn("unsupported indented line", errors[0])

    def test_orphan_list_item(self) -> None:
        _, errors = cc.parse_frontmatter(["- a"])
        self.assertIn("list item with no key above it", errors[0])

    def test_line_without_colon(self) -> None:
        _, errors = cc.parse_frontmatter(["garbage"])
        self.assertIn("not a `key: value` pair", errors[0])

    def test_error_line_numbers_account_for_the_opening_marker(self) -> None:
        _, errors = cc.parse_frontmatter(["type: design", "garbage"])
        self.assertIn("line 3:", errors[0])


# --------------------------------------------------------------------------
# field checks
# --------------------------------------------------------------------------


class FieldCheckTests(TempCorpus):
    def test_valid_document_is_clean(self) -> None:
        write(self.root, "a.md", VALID)
        report = run_checks(self.root)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])
        self.assertFalse(report.failed)

    def test_missing_frontmatter(self) -> None:
        write(self.root, "a.md", "# No frontmatter\n")
        self.assertIn("no frontmatter block", joined(run_checks(self.root).errors))

    def test_unterminated_frontmatter(self) -> None:
        write(self.root, "a.md", "---\ntype: design\n")
        report = run_checks(self.root)
        self.assertIn("never closed", joined(report.errors))

    def test_missing_required_fields(self) -> None:
        write(self.root, "a.md", "---\nlocked: true\n---\n")
        found = joined(run_checks(self.root).errors)
        self.assertIn("`type` is required", found)
        self.assertIn("`lifecycle` is required", found)
        self.assertIn("`owns` is required", found)

    def test_unknown_lifecycle_value(self) -> None:
        doc = VALID.replace("lifecycle: active", "lifecycle: retired")
        write(self.root, "a.md", doc)
        self.assertIn("`lifecycle` is required", joined(run_checks(self.root).errors))

    def test_empty_owns_list(self) -> None:
        write(self.root, "a.md", "---\ntype: design\nlifecycle: active\nowns:\n---\n")
        self.assertIn("needs >=1 claim", joined(run_checks(self.root).errors))

    def test_locked_must_be_boolean(self) -> None:
        write(self.root, "a.md", VALID.replace("---\n\n# Alpha", "locked: yes\n---\n"))
        self.assertIn("must be true or false", joined(run_checks(self.root).errors))

    def test_unknown_key_is_only_a_warning(self) -> None:
        write(self.root, "a.md", VALID.replace("type: design", "type: design\nfoo: 1"))
        report = run_checks(self.root)
        self.assertEqual(report.errors, [])
        self.assertIn("unknown frontmatter key `foo`", joined(report.warnings))


class HandlingTests(TempCorpus):
    def with_handling(self, value: str) -> None:
        write(self.root, "a.md", VALID.replace("owns:", f"handling: {value}\nowns:"))

    def test_absent_is_the_normal_case(self) -> None:
        write(self.root, "a.md", VALID)
        self.assertEqual(run_checks(self.root).errors, [])

    def test_every_permitted_value_is_accepted(self) -> None:
        for value in cc.HANDLING_VALUES:
            with self.subTest(value=value):
                self.with_handling(value)
                self.assertEqual(run_checks(self.root).errors, [])

    def test_misspelled_value_is_an_error(self) -> None:
        self.with_handling("confidential")
        found = joined(run_checks(self.root).errors)
        self.assertIn("`handling` must be one of", found)

    def test_it_is_a_known_key_not_a_warning(self) -> None:
        self.with_handling("internal")
        self.assertEqual(run_checks(self.root).warnings, [])

    def test_index_omits_the_column_when_nothing_declares_one(self) -> None:
        write(self.root, "a.md", VALID)
        report = cc.Report()
        docs = [
            doc
            for path in cc.collect(self.root, None)
            if (doc := cc.load(path, self.root, report)) is not None
        ]
        self.assertNotIn("Handling", cc.render_index(docs))

    def test_index_adds_the_column_when_one_document_declares_one(self) -> None:
        self.with_handling("customer-confidential")
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        report = cc.Report()
        docs = [
            doc
            for path in cc.collect(self.root, None)
            if (doc := cc.load(path, self.root, report)) is not None
        ]
        rendered = cc.render_index(docs)
        self.assertIn(
            "| Owns | Document | Type | Lifecycle | Locked | Handling |", rendered
        )
        self.assertIn(
            "| alpha | a.md | design | active | no | customer-confidential |", rendered
        )
        self.assertIn("| beta | b.md | design | active | no | - |", rendered)


class SupersessionTests(TempCorpus):
    def test_superseded_requires_a_pointer(self) -> None:
        write(self.root, "a.md", VALID.replace("active", "superseded"))
        found = joined(run_checks(self.root).errors)
        self.assertIn("`superseded-by` is required", found)

    def test_pointer_target_must_exist(self) -> None:
        doc = VALID.replace("active", "superseded").replace(
            "owns:", "superseded-by: gone.md\nowns:"
        )
        write(self.root, "a.md", doc)
        self.assertIn("target gone.md not found", joined(run_checks(self.root).errors))

    def test_pointer_resolves_to_a_real_file(self) -> None:
        doc = VALID.replace("active", "superseded").replace(
            "owns:", "superseded-by: b.md\nowns:"
        )
        write(self.root, "a.md", doc)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        self.assertEqual(run_checks(self.root).errors, [])

    def test_pointer_forbidden_when_not_superseded(self) -> None:
        doc = VALID.replace("owns:", "superseded-by: b.md\nowns:")
        write(self.root, "a.md", doc)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        found = joined(run_checks(self.root).errors)
        self.assertIn("only allowed on a superseded document", found)

    def test_dangling_back_link_is_only_a_warning(self) -> None:
        doc = VALID.replace("owns:", "supersedes: [gone.md]\nowns:")
        write(self.root, "a.md", doc)
        report = run_checks(self.root)
        self.assertEqual(report.errors, [])
        self.assertIn("back-link gone.md not found", joined(report.warnings))


class OwnershipTests(TempCorpus):
    def test_collision_between_two_documents(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "b.md", VALID)
        found = joined(run_checks(self.root).errors)
        self.assertIn("ownership collision on 'alpha'", found)
        self.assertIn("a.md", found)
        self.assertIn("b.md", found)

    def test_distinct_claims_do_not_collide(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        self.assertEqual(run_checks(self.root).errors, [])


# --------------------------------------------------------------------------
# amendments and ceilings
# --------------------------------------------------------------------------


def with_amendments(entries: int, markers: int) -> str:
    """Build a document with N amendment entries and M inline markers."""
    body = [VALID.rstrip("\n"), ""]
    body += [f"text [amended A{n}]" for n in range(1, markers + 1)]
    body += ["", "## Amendments", ""]
    for n in range(1, entries + 1):
        body += [f"### A{n} - fix {n}", "reason.", ""]
    return "\n".join(body) + "\n"


class AmendmentTests(TempCorpus):
    def test_entry_and_marker_pair_cleanly(self) -> None:
        write(self.root, "a.md", with_amendments(entries=1, markers=1))
        self.assertEqual(run_checks(self.root).errors, [])

    def test_entry_without_marker(self) -> None:
        write(self.root, "a.md", with_amendments(entries=1, markers=0))
        found = joined(run_checks(self.root).errors)
        self.assertIn("amendment A1 has no inline marker", found)

    def test_marker_without_entry(self) -> None:
        write(self.root, "a.md", with_amendments(entries=0, markers=1))
        found = joined(run_checks(self.root).errors)
        self.assertIn("[amended A1] has no matching", found)

    def test_several_markers_for_one_entry_are_legal(self) -> None:
        # One correction routinely invalidates more than one point. Requiring
        # exactly one marker made that case unrepresentable, so an amendment
        # marked in three places had to be split into three near-duplicates.
        doc = with_amendments(entries=1, markers=1)
        doc = doc.replace(
            "# Alpha", "# Alpha\n\nagain [amended A1]\n\nthird [amended A1]"
        )
        write(self.root, "a.md", doc)
        self.assertEqual(run_checks(self.root).errors, [])

    def test_marker_inside_the_amendments_section_does_not_count(self) -> None:
        doc = with_amendments(entries=1, markers=1)
        doc = doc.replace("reason.", "reason. [amended A1]")
        write(self.root, "a.md", doc)
        self.assertEqual(run_checks(self.root).errors, [])

    def test_five_amendments_propose_supersession(self) -> None:
        write(self.root, "a.md", with_amendments(entries=5, markers=5))
        report = run_checks(self.root)
        self.assertEqual(report.errors, [])
        self.assertIn("propose superseding it", joined(report.warnings))

    def test_four_amendments_stay_quiet(self) -> None:
        write(self.root, "a.md", with_amendments(entries=4, markers=4))
        self.assertEqual(run_checks(self.root).warnings, [])


class CeilingTests(TempCorpus):
    def build(self, section_lines: int, tail_lines: int = 0) -> None:
        body = [VALID.rstrip("\n"), "", "## Long section", ""]
        body += [f"line {i}" for i in range(section_lines)]
        if tail_lines:
            body += ["", "## Tail", ""] + [f"t{i}" for i in range(tail_lines)]
        write(self.root, "a.md", "\n".join(body) + "\n")

    def test_long_section_names_itself(self) -> None:
        self.build(section_lines=cc.SECTION_WARN_LINES + 10, tail_lines=1)
        found = joined(run_checks(self.root).warnings)
        self.assertIn("section 'Long section'", found)
        self.assertIn("propose forking it", found)

    def test_one_section_document_is_exempt(self) -> None:
        # The expected shape of a freshly forked child. Warning here proposes
        # that the document fork itself, which is a remedy nobody can apply.
        self.build(section_lines=cc.SECTION_WARN_LINES + 10)
        self.assertNotIn("propose forking it", joined(run_checks(self.root).warnings))

    def test_document_ceiling_names_the_sections_it_computed(self) -> None:
        self.build(section_lines=10, tail_lines=cc.DOC_LIMIT_LINES)
        found = joined(run_checks(self.root).warnings)
        self.assertIn("extracting 'Tail'", found)

    def test_short_section_stays_quiet(self) -> None:
        self.build(section_lines=10)
        self.assertEqual(run_checks(self.root).warnings, [])

    def test_document_backstop(self) -> None:
        self.build(section_lines=10, tail_lines=cc.DOC_WARN_LINES)
        found = joined(run_checks(self.root).warnings)
        self.assertIn(f"past the {cc.DOC_WARN_LINES}-line backstop", found)

    def test_document_limit_replaces_the_backstop(self) -> None:
        self.build(section_lines=10, tail_lines=cc.DOC_LIMIT_LINES)
        found = joined(run_checks(self.root).warnings)
        self.assertIn(f"past the {cc.DOC_LIMIT_LINES}-line limit", found)
        self.assertNotIn("backstop", found)

    def test_ceilings_never_set_the_exit_status(self) -> None:
        self.build(section_lines=cc.SECTION_WARN_LINES + 10)
        self.assertFalse(run_checks(self.root).failed)


# --------------------------------------------------------------------------
# index
# --------------------------------------------------------------------------


class IndexTests(TempCorpus):
    def test_rows_are_generated_from_declarations(self) -> None:
        write(
            self.root,
            "a.md",
            VALID.replace("owns:\n  - alpha", "locked: true\nowns:\n  - alpha"),
        )
        report = cc.Report()
        docs = [
            doc
            for path in cc.collect(self.root, None)
            if (doc := cc.load(path, self.root, report)) is not None
        ]
        rendered = cc.render_index(docs)
        self.assertTrue(rendered.startswith(cc.INDEX_MARKER))
        self.assertIn("| alpha | a.md | design | active | yes |", rendered)

    def test_generated_index_is_skipped_when_rescanned(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "INDEX.md", cc.INDEX_MARKER + "\n\n# Document index\n")
        report = run_checks(self.root)
        self.assertEqual(report.errors, [])

    def test_refuses_to_overwrite_a_hand_written_index(self) -> None:
        target = write(self.root, "INDEX.md", "# Written by a person\n")
        report = cc.Report()
        cc.write_index(target, "replacement", report)
        self.assertIn("refusing to overwrite", joined(report.errors))
        self.assertEqual(target.read_text(encoding="utf-8"), "# Written by a person\n")

    def test_overwrites_its_own_output(self) -> None:
        target = write(self.root, "INDEX.md", cc.INDEX_MARKER + "\nold\n")
        report = cc.Report()
        cc.write_index(target, cc.INDEX_MARKER + "\nnew\n", report)
        self.assertEqual(report.errors, [])
        self.assertIn("new", target.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


class MainTests(TempCorpus):
    def run_main(self, *argv: str) -> tuple[int, str]:
        buffer = io.StringIO()
        errors = io.StringIO()
        with redirect_stdout(buffer), redirect_stderr(errors):
            code = cc.main(list(argv))
        return code, buffer.getvalue() + errors.getvalue()

    def test_clean_corpus_exits_zero(self) -> None:
        write(self.root, "a.md", VALID)
        code, out = self.run_main(str(self.root))
        self.assertEqual(code, cc.EXIT_OK)
        self.assertIn("0 error(s)", out)

    def test_contract_error_exits_one(self) -> None:
        write(self.root, "a.md", "# nope\n")
        code, _ = self.run_main(str(self.root))
        self.assertEqual(code, cc.EXIT_CONTRACT_ERRORS)

    def test_warnings_alone_still_exit_zero(self) -> None:
        write(self.root, "a.md", with_amendments(entries=5, markers=5))
        code, out = self.run_main(str(self.root))
        self.assertEqual(code, cc.EXIT_OK)
        self.assertIn("WARN", out)

    def test_quiet_suppresses_warnings_only(self) -> None:
        write(self.root, "a.md", with_amendments(entries=5, markers=5))
        _, out = self.run_main(str(self.root), "--quiet")
        self.assertNotIn("WARN", out)

    def test_missing_root_is_a_usage_error(self) -> None:
        code, _ = self.run_main(str(self.root / "nope"))
        self.assertEqual(code, cc.EXIT_BAD_USAGE)

    def test_missing_index_directory_is_a_usage_error(self) -> None:
        write(self.root, "a.md", VALID)
        code, _ = self.run_main(
            str(self.root), "--index", str(self.root / "x" / "i.md")
        )
        self.assertEqual(code, cc.EXIT_BAD_USAGE)

    def test_index_is_written_and_excluded_from_the_scan(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        target = self.root / "INDEX.md"
        code, out = self.run_main(str(self.root), "--index", str(target))
        self.assertEqual(code, cc.EXIT_OK)
        self.assertIn("2 document(s)", out)
        self.assertIn("| alpha | a.md |", target.read_text(encoding="utf-8"))

    def test_survey_accepts_a_corpus_with_no_frontmatter(self) -> None:
        write(self.root, "a.md", "# Old\n\n## Section\n\nbody\n")
        code, out = self.run_main(str(self.root), "--survey")
        self.assertEqual(code, cc.EXIT_OK)
        self.assertIn("1 document(s) surveyed", out)
        self.assertNotIn("no frontmatter block", out)

    def test_survey_reports_structure_and_flags_fork_candidates(self) -> None:
        long_section = "\n".join(f"line {i}" for i in range(cc.SECTION_WARN_LINES + 5))
        write(
            self.root,
            "a.md",
            f"# Old\n\n## Short\n\nbody\n\n## Long\n\n{long_section}\n",
        )
        _, out = self.run_main(str(self.root), "--survey")
        self.assertIn("no frontmatter", out)
        self.assertIn("Short", out)
        self.assertIn("FORK", out)
        self.assertIn("Long", out)

    def test_survey_does_not_flag_a_short_section(self) -> None:
        write(self.root, "a.md", "# Old\n\n## Short\n\nbody\n")
        _, out = self.run_main(str(self.root), "--survey")
        self.assertNotIn("FORK", out)

    def test_survey_still_sees_frontmatter_where_it_exists(self) -> None:
        write(self.root, "a.md", VALID)
        _, out = self.run_main(str(self.root), "--survey")
        self.assertIn("frontmatter present", out)

    def test_survey_refuses_to_write_an_index(self) -> None:
        write(self.root, "a.md", VALID)
        code, out = self.run_main(
            str(self.root), "--survey", "--index", str(self.root / "INDEX.md")
        )
        self.assertEqual(code, cc.EXIT_BAD_USAGE)
        self.assertIn("does not write an index", out)

    def test_survey_still_reports_an_unreadable_file(self) -> None:
        (self.root / "a.md").write_bytes(b"\xff\xfe not utf-8")
        code, out = self.run_main(str(self.root), "--survey")
        self.assertEqual(code, cc.EXIT_CONTRACT_ERRORS)
        self.assertIn("cannot read", out)

    def test_two_documents_without_an_index_warn(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))
        _, out = self.run_main(str(self.root))
        self.assertIn("no index was generated", out)


class IndexFlagTests(TempCorpus):
    """The two index flags, and the warning a read-only gate should not see."""

    def run_main(self, *argv: str) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            code = cc.main(list(argv))
        return code, buf.getvalue()

    def two_docs(self) -> None:
        write(self.root, "a.md", VALID)
        write(self.root, "b.md", VALID.replace("- alpha", "- beta"))

    def test_check_index_suppresses_the_missing_index_warning(self) -> None:
        self.two_docs()
        index = self.root / "INDEX.md"
        self.run_main(str(self.root), "--index", str(index))
        code, out = self.run_main(str(self.root), "--check-index", str(index))
        self.assertEqual(code, cc.EXIT_OK)
        self.assertNotIn("no index was generated", out)

    def test_check_index_fails_on_drift(self) -> None:
        self.two_docs()
        index = self.root / "INDEX.md"
        self.run_main(str(self.root), "--index", str(index))
        write(self.root, "c.md", VALID.replace("- alpha", "- gamma"))
        code, out = self.run_main(str(self.root), "--check-index", str(index))
        self.assertEqual(code, cc.EXIT_CONTRACT_ERRORS)
        self.assertIn("index is stale", out)
        self.assertIn("gamma", out)

    def test_index_and_check_index_are_mutually_exclusive(self) -> None:
        write(self.root, "a.md", VALID)
        code, out = self.run_main(
            str(self.root),
            "--index",
            str(self.root / "i.md"),
            "--check-index",
            str(self.root / "j.md"),
        )
        self.assertEqual(code, cc.EXIT_BAD_USAGE)
        self.assertIn("use one", out)

    def test_a_corpus_directory_is_required(self) -> None:
        code, out = self.run_main()
        self.assertEqual(code, cc.EXIT_BAD_USAGE)
        self.assertIn("corpus directory is required", out)


class CompareIndexTests(TempCorpus):
    """A read-only gate compares; it never writes what it is checking."""

    def generated(self) -> str:
        write(self.root, "a.md", VALID)
        report = cc.Report()
        docs = [
            doc
            for path in cc.collect(self.root, None)
            if (doc := cc.load(path, self.root, report)) is not None
        ]
        return cc.render_index(docs)

    def test_matching_index_is_silent(self) -> None:
        content = self.generated()
        path = write(self.root, "INDEX.md", content)
        report = cc.Report()
        cc.compare_index(path, content, report)
        self.assertEqual(report.errors, [])

    def test_drift_is_an_error_naming_the_row(self) -> None:
        content = self.generated()
        path = write(self.root, "INDEX.md", content.replace("alpha", "beta"))
        report = cc.Report()
        cc.compare_index(path, content, report)
        found = joined(report.errors)
        self.assertIn("index is stale", found)
        self.assertIn("alpha", found)

    def test_missing_index_is_an_error(self) -> None:
        content = self.generated()
        report = cc.Report()
        cc.compare_index(self.root / "nope.md", content, report)
        self.assertIn("index missing", joined(report.errors))

    def test_comparing_never_writes(self) -> None:
        content = self.generated()
        path = write(self.root, "INDEX.md", "stale\n")
        cc.compare_index(path, content, cc.Report())
        self.assertEqual(path.read_text(encoding="utf-8"), "stale\n")


# --------------------------------------------------------------------------
# fork verification
# --------------------------------------------------------------------------


class SectionExtractionTests(unittest.TestCase):
    def test_deeper_heading_does_not_end_the_section(self) -> None:
        lines = ["## A", "one", "### Inner", "two", "## B", "three"]
        self.assertEqual(
            cc.extract_section(lines, "## A"), ["## A", "one", "### Inner", "two"]
        )

    def test_last_section_runs_to_end_of_file(self) -> None:
        lines = ["## A", "one", "## B", "two", "three"]
        self.assertEqual(cc.extract_section(lines, "## B"), ["## B", "two", "three"])

    def test_absent_section_returns_none(self) -> None:
        self.assertIsNone(cc.extract_section(["## A"], "## Missing"))


class TrimBlanksTests(unittest.TestCase):
    def test_strips_both_ends_only(self) -> None:
        self.assertEqual(cc.trim_blanks(["", "a", "", "b", "", ""]), ["a", "", "b"])

    def test_all_blank_collapses_to_empty(self) -> None:
        self.assertEqual(cc.trim_blanks(["", "  "]), [])


class NameLongestTests(unittest.TestCase):
    def test_names_the_longest_first(self) -> None:
        sections = [("A", 0, 10), ("B", 0, 300), ("C", 0, 50)]
        self.assertEqual(cc.name_longest(sections, limit=2), "'B' (300), 'C' (50)")

    def test_no_sections_falls_back_to_prose(self) -> None:
        self.assertEqual(cc.name_longest([]), "its longest sections")


PARENT_BEFORE_FORK = """---
type: design
lifecycle: active
owns:
  - alpha
  - moving
---

# Alpha

## Keeps

kept line

## Moves

first moved line
second moved line
"""

FORKED_CHILD = """---
type: milestone
lifecycle: draft
owns:
  - moving
---

## Moves

first moved line
second moved line
"""

# The parent as it looks once the fork has been made and committed: the heading
# stays, its content is a pointer. Running the check at this revision compares
# the child against a pointer, which is the second wrong-baseline case.
PARENT_AFTER_FORK = """---
type: design
lifecycle: active
owns:
  - alpha
---

# Alpha

## Keeps

kept line

## Moves

> **Authority on this moved to [child.md](child.md)**, which owns it.
"""

# All-blockquote, but a quotation rather than a pointer -- it links nowhere near
# the child. The pointer test must not accuse it.
PARENT_WITH_QUOTED_SECTION = PARENT_AFTER_FORK.replace(
    "> **Authority on this moved to [child.md](child.md)**, which owns it.",
    "> Quoted from [the standard](https://example.invalid/spec.html), verbatim.",
)


def git(root: Path, *args: str) -> None:
    """Run one git command inside a temporary repository."""
    subprocess.run(  # noqa: S603
        ["git", *args], cwd=root, capture_output=True, check=True, text=True
    )


@unittest.skipIf(shutil.which("git") is None, "git is not installed")
class VerifyForkTests(TempCorpus):
    """The check that replaced reading a `git diff` by eye.

    The prescribed diff recipe reported a mismatch on a correct fork three
    different ways, so these cases pin the two things that actually matter: a
    formatter artifact must pass, and a changed word must not.
    """

    def setUp(self) -> None:
        super().setUp()
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "t@example.com")
        git(self.root, "config", "user.name", "T")
        write(self.root, "parent.md", PARENT_BEFORE_FORK)
        git(self.root, "add", "parent.md")
        git(self.root, "commit", "-qm", "before the fork")

    def verify(
        self, child_text: str, heading: str = "## Moves", rev: str = "HEAD"
    ) -> tuple[bool, cc.Report, str]:
        write(self.root, "child.md", child_text)
        report = cc.Report()
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = cc.verify_fork(
                f"{self.root / 'parent.md'}:{heading}",
                self.root / "child.md",
                rev,
                report,
            )
        return ok, report, buf.getvalue()

    def test_identical_relocation_verifies(self) -> None:
        ok, report, out = self.verify(FORKED_CHILD)
        self.assertTrue(ok)
        self.assertEqual(report.errors, [])
        self.assertIn("fork verified", out)

    def test_trailing_blank_trimmed_by_a_hook_still_verifies(self) -> None:
        # end-of-file-fixer rewrites relocated content after the move. That is
        # a formatter artifact, and reading it as a rewrite is what trained the
        # previous recipe's users to override it.
        ok, report, _ = self.verify(FORKED_CHILD.rstrip("\n"))
        self.assertTrue(ok)
        self.assertEqual(report.errors, [])

    def test_a_changed_word_fails(self) -> None:
        ok, report, _ = self.verify(FORKED_CHILD.replace("first moved", "1st moved"))
        self.assertFalse(ok)
        self.assertIn("fork mismatch at body line", joined(report.errors))

    def test_a_dropped_line_fails(self) -> None:
        ok, report, _ = self.verify(FORKED_CHILD.replace("second moved line\n", ""))
        self.assertFalse(ok)
        self.assertIn("fork mismatch", joined(report.errors))

    def test_an_added_line_fails(self) -> None:
        ok, report, _ = self.verify(FORKED_CHILD + "\nsmuggled in\n")
        self.assertFalse(ok)
        self.assertIn("fork mismatch", joined(report.errors))

    def test_missing_section_is_named(self) -> None:
        _, report, _ = self.verify(FORKED_CHILD, heading="## Absent")
        self.assertIn("no section '## Absent'", joined(report.errors))

    def test_unknown_revision_is_reported(self) -> None:
        _, report, _ = self.verify(FORKED_CHILD, rev="nosuchrev")
        self.assertIn("failed", joined(report.errors))

    def test_malformed_spec_is_rejected(self) -> None:
        report = cc.Report()
        cc.verify_fork("parent.md", self.root / "child.md", "HEAD", report)
        self.assertIn("--verify-fork needs", joined(report.errors))

    def test_a_dirty_parent_explains_the_mismatch_it_causes(self) -> None:
        # The normal case: you fork the document you were just editing, so the
        # parent is dirty and `--since HEAD` compares against a version that
        # predates the session. Without the hint this reads as a botched fork.
        write(
            self.root, "parent.md", PARENT_BEFORE_FORK.replace("first moved", "edited")
        )
        ok, report, _ = self.verify(FORKED_CHILD.replace("first moved", "edited"))
        self.assertFalse(ok)
        self.assertIn("fork mismatch at body line", joined(report.errors))
        self.assertIn("uncommitted changes", joined(report.warnings))
        self.assertIn("COMMITTED version", joined(report.warnings))

    def test_a_clean_parent_gets_no_baseline_hint(self) -> None:
        # The hint must not fire on a genuine relocation error, or it becomes
        # the excuse a real mismatch gets waved through with.
        ok, report, _ = self.verify(FORKED_CHILD.replace("first moved", "1st moved"))
        self.assertFalse(ok)
        self.assertNotIn("uncommitted changes", joined(report.warnings))

    def commit_parent(self, text: str) -> None:
        """Replace the parent and commit it, so HEAD carries that state."""
        write(self.root, "parent.md", text)
        git(self.root, "add", "parent.md")
        git(self.root, "commit", "-qm", "parent updated")

    def test_a_parent_already_carrying_the_pointer_says_so(self) -> None:
        # Running the check after committing the fork: HEAD holds the pointer,
        # not the section, and the tree is clean so the dirty hint stays quiet.
        self.commit_parent(PARENT_AFTER_FORK)
        ok, report, _ = self.verify(FORKED_CHILD)
        self.assertFalse(ok)
        self.assertIn("already carries the fork pointer", joined(report.warnings))
        self.assertIn("BEFORE the fork", joined(report.warnings))

    def test_the_pointer_hint_wins_over_the_dirty_hint(self) -> None:
        # Both causes can hold at once. The pointer is conclusive where
        # dirtiness is only likely, so only the conclusive one is reported.
        self.commit_parent(PARENT_AFTER_FORK)
        write(self.root, "parent.md", PARENT_AFTER_FORK + "\nan uncommitted edit\n")
        ok, report, _ = self.verify(FORKED_CHILD)
        self.assertFalse(ok)
        self.assertIn("already carries the fork pointer", joined(report.warnings))
        self.assertNotIn("uncommitted changes", joined(report.warnings))

    def test_the_cli_prints_the_hint_and_quiet_suppresses_it(self) -> None:
        # The hints were reachable from these tests and invisible from the
        # command line, because the --verify-fork branch printed errors only.
        # A hint nobody sees is the confusing report it exists to replace.
        self.commit_parent(PARENT_AFTER_FORK)
        write(self.root, "child.md", FORKED_CHILD)
        argv = [
            "--verify-fork",
            f"{self.root / 'parent.md'}:## Moves",
            str(self.root / "child.md"),
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cc.main(argv)
        self.assertEqual(code, cc.EXIT_CONTRACT_ERRORS)
        self.assertIn("already carries the fork pointer", buf.getvalue())

        quiet = io.StringIO()
        with redirect_stdout(quiet):
            cc.main([*argv, "--quiet"])
        self.assertIn("ERROR", quiet.getvalue())
        self.assertNotIn("already carries the fork pointer", quiet.getvalue())

    def test_an_all_blockquote_section_is_not_mistaken_for_a_pointer(self) -> None:
        # A section that quotes a specification is all-blockquote too. Accusing
        # it of being a pointer would send the reader after the wrong cause.
        self.commit_parent(PARENT_WITH_QUOTED_SECTION)
        ok, report, _ = self.verify(FORKED_CHILD)
        self.assertFalse(ok)
        self.assertNotIn("already carries the fork pointer", joined(report.warnings))

    def test_a_dirty_parent_that_still_matches_stays_silent(self) -> None:
        # Dirtiness alone is never a failure: an edit outside the moved section
        # leaves the comparison correct, and warning anyway would be noise on
        # every fork.
        write(
            self.root,
            "parent.md",
            PARENT_BEFORE_FORK + "\n## Added later\n\nunrelated\n",
        )
        ok, report, out = self.verify(FORKED_CHILD)
        self.assertTrue(ok)
        self.assertEqual(report.warnings, [])
        self.assertIn("fork verified", out)


if __name__ == "__main__":
    unittest.main()
