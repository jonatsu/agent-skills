# Attributions

## Current skill

- Skill: `writing-for-humans`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: assembled from the author's own writing rules plus two adapted
  upstream sources

## Original authors and sources

- Primary source (structure, provenance, and skimmability principles — the
  backbone of this skill):
  - The author's own global writing rules (`~/.config/claude/rules/WRITING.md`),
    ported into a portable, agent-agnostic skill.
- Secondary source (four distilled composition rules — positive form, parallel
  construction, emphatic word at sentence end, and omit-needless-words phrase
  reductions):
  - *The Elements of Style* by William Strunk Jr. (1918). Public domain.
- Tertiary source (the promotional-vocabulary blocklist under "Avoid AI tells"):
  - Upstream project:
    [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit),
    skill `writing-clearly-and-concisely`.
  - Upstream chain: adapted by softaworks from
    [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills),
    itself adapted from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style).
  - Upstream license: MIT.

## Adaptation note

This skill takes its structure and provenance discipline from the author's own
`WRITING.md`, adds four distilled rules from Strunk (stated as compact modern
directives, not the verbatim 1918 prose), and adopts only the
promotional-vocabulary blocklist from softaworks' `writing-clearly-and-concisely`
— the one category that `stop-slop` (this repo's AI-tell skill) does not already
cover. Strunk's dogmatic "avoid the passive voice" was deliberately softened to
an "active, third-person; passive when the actor is irrelevant" rule.

## Upstream license (MIT, softaworks chain)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
