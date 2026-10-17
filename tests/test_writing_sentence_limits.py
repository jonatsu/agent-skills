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
    ("writing-readmes", "SKILL.md"),
    ("context-architecture", "references/writing-rules.md"),
    ("agents-context-docs", "SKILL.md"),
    ("writing-prompts", "SKILL.md"),
    ("session-handoff", "SKILL.md"),
    ("skill-forge", "references/authoring.md"),
)
# A word limit as the skills write it: "20 words", optionally bold.
WORD_LIMIT = re.compile(r"\*{0,2}(\d+) words\b")


def word_limits(skill: str, relative_path: str) -> list[int]:
    text = (skill_directory(skill) / relative_path).read_text(encoding="utf-8")
    return [int(match.group(1)) for match in WORD_LIMIT.finditer(text)]


class SentenceLimitsStayInStep(unittest.TestCase):
    def test_canonical_skill_states_procedural_then_descriptive_limit(self) -> None:
        limits = word_limits(*CANONICAL)
        self.assertEqual(
            len(limits), 2, f"{CANONICAL[0]} should state exactly two word limits: {limits}"
        )
        procedural, descriptive = limits
        self.assertLess(procedural, descriptive, f"{CANONICAL[0]} limits out of order: {limits}")

    def test_copies_match_the_canonical_limits(self) -> None:
        expected = word_limits(*CANONICAL)
        for skill, relative_path in COPIES:
            with self.subTest(skill=skill, file=relative_path):
                self.assertEqual(
                    word_limits(skill, relative_path),
                    expected,
                    f"{skill}/{relative_path} drifted from {CANONICAL[0]}; update every copy",
                )


if __name__ == "__main__":
    unittest.main()
