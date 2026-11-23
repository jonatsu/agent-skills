"""Several skills carry their own copy of the sentence limits; this keeps the copies in step.

`writing-for-humans` holds the canonical procedural and descriptive limits. The other prose skills and the
agent-facing writing skills restate them, so none depends on an agent also loading `writing-for-humans`.
"""

from __future__ import annotations

import re
import unittest

from skill_locator import skill_directory

CANONICAL = ("writing-for-humans", "SKILL.md")
COPIES = (
    ("writing-documentation", "SKILL.md"),
    ("repo-landing-docs", "SKILL.md"),
    ("context-architecture", "references/writing-rules.md"),
    ("agents-context-docs", "SKILL.md"),
    ("writing-prompts", "SKILL.md"),
    ("session-handoff", "SKILL.md"),
    ("skill-forge", "references/authoring.md"),
)
# A sentence limit as the skills state it: the canonical table's "**20 words per sentence**", and the copies'
# "within 20 words", optionally bold. Other counts, such as "a 2,000-word budget" or "300 words", are not limits.
CANONICAL_LIMIT = re.compile(r"\*{0,2}(\d+) words per sentence\b")
COPY_LIMIT = re.compile(r"\bwithin\s+\*{0,2}(\d+) words\b")


def limits_in(text: str, pattern: re.Pattern[str]) -> list[int]:
    return [int(match.group(1)) for match in pattern.finditer(text)]


def word_limits(skill: str, relative_path: str, pattern: re.Pattern[str]) -> list[int]:
    text = (skill_directory(skill) / relative_path).read_text(encoding="utf-8")
    return limits_in(text, pattern)


class SentenceLimitsStayInStep(unittest.TestCase):
    def test_patterns_ignore_counts_that_are_not_limits(self) -> None:
        text = "The default budget of 2,000 words; a report of at most 300 words; keep it within 20 words."
        self.assertEqual(limits_in(text, COPY_LIMIT), [20])
        self.assertEqual(limits_in(text, CANONICAL_LIMIT), [])

    def test_canonical_skill_states_procedural_then_descriptive_limit(self) -> None:
        limits = word_limits(*CANONICAL, CANONICAL_LIMIT)
        self.assertEqual(len(limits), 2, f"{CANONICAL[0]} should state exactly two word limits: {limits}")
        procedural, descriptive = limits
        self.assertLess(procedural, descriptive, f"{CANONICAL[0]} limits out of order: {limits}")

    def test_copies_match_the_canonical_limits(self) -> None:
        expected = word_limits(*CANONICAL, CANONICAL_LIMIT)
        for skill, relative_path in COPIES:
            with self.subTest(skill=skill, file=relative_path):
                self.assertEqual(
                    word_limits(skill, relative_path, COPY_LIMIT),
                    expected,
                    f"{skill}/{relative_path} drifted from {CANONICAL[0]}; update every copy",
                )


if __name__ == "__main__":
    unittest.main()
