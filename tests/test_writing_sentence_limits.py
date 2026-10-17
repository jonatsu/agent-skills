"""The prose skills each carry their own copy of the sentence limits; this keeps the copies in step.

`writing-for-humans` holds the canonical procedural and descriptive limits. `writing-documentation` and
`writing-readmes` restate them so neither depends on an agent also loading `writing-for-humans`.
"""

from __future__ import annotations

import re
import unittest

from skill_locator import skill_directory

CANONICAL_SKILL = "writing-for-humans"
COPYING_SKILLS = ("writing-documentation", "writing-readmes")
# A word limit as the skills write it: "20 words", optionally bold.
WORD_LIMIT = re.compile(r"\*{0,2}(\d+) words\b")


def word_limits(skill: str) -> list[int]:
    text = (skill_directory(skill) / "SKILL.md").read_text(encoding="utf-8")
    return [int(match.group(1)) for match in WORD_LIMIT.finditer(text)]


class SentenceLimitsStayInStep(unittest.TestCase):
    def test_canonical_skill_states_procedural_then_descriptive_limit(self) -> None:
        limits = word_limits(CANONICAL_SKILL)
        self.assertEqual(
            len(limits), 2, f"{CANONICAL_SKILL} should state exactly two word limits: {limits}"
        )
        procedural, descriptive = limits
        self.assertLess(procedural, descriptive, f"{CANONICAL_SKILL} limits out of order: {limits}")

    def test_copying_skills_match_the_canonical_limits(self) -> None:
        expected = word_limits(CANONICAL_SKILL)
        for skill in COPYING_SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(
                    word_limits(skill),
                    expected,
                    f"{skill} sentence limits drifted from {CANONICAL_SKILL}; update every copy together",
                )


if __name__ == "__main__":
    unittest.main()
