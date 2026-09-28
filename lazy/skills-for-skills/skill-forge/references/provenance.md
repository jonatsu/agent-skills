# Provenance and Licensing

These are conservative authoring policies; determine legal obligations from the exact source license and the
relationship to it.

Use the target repository's license for original work. Use the upstream license for derived work unless its
terms permit and the author deliberately applies a compatible alternative. Verify licenses from the license
text at a pinned upstream revision. Repository metadata alone is insufficient evidence.

## Classify Every Source

Classify each source read during authoring by what changed after reading it:

| Relationship                                  | Required record                                     |
| --------------------------------------------- | --------------------------------------------------- |
| Fact or runtime verification only             | Cite the source near the affected claim when useful |
| Idea influenced independently written content | Add `ATTRIBUTIONS.md`                               |
| Copied, adapted, or translated material       | Add `ATTRIBUTIONS.md` and `LICENSE.upstream`        |
| Vendored code or assets                       | Add `ATTRIBUTIONS.md` and `LICENSE.upstream`        |

Reading a source creates an idea-influence obligation when it changes the skill's guidance, workflow,
structure, examples, terminology, or failure modes. This trigger applies when every sentence and example is
written from scratch. This is a conservative traceability policy. Do not present it as a universal legal rule.

For idea influence, `ATTRIBUTIONS.md` names the original author, project and exact path, pinned commit or tag,
the ideas retained, and the fact that the expression is independent. Record the source's license status, but
do not claim that its license governs independently written expression.

For copied, adapted, translated, or vendored material, determine the source license's actual obligations. This
workflow also requires the package to ship:

- `LICENSE.upstream` containing the upstream license text verbatim; and
- `NOTICE.upstream` when the upstream project supplies one or its license requires preservation.

When a package carries material from more than one upstream, give each further license its own file named for
its source, such as `LICENSE.upstream-<source>`, and name the file in that source's `ATTRIBUTIONS.md` entry, so
every copyright notice keeps traveling beside the material it covers.

Start `ATTRIBUTIONS.md` from `assets/ATTRIBUTIONS.template.md` when available. Preserve existing provenance
artifacts and notices during updates. If the source or license cannot be verified, stop before making an
authoritative attribution claim and report what is missing.

Check the upstream license before adapting material. When its terms do not permit the intended use or
redistribution, write an independent replacement from domain knowledge and do not copy the restricted
expression.
