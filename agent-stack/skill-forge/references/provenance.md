# Provenance and Licensing

Every skill authored under this workflow records:

- the current author in `metadata.author`; and
- the applicable license in the Agent Skills top-level `license` field.

Use the target repository's license for original work. Use the upstream license for derived work unless its
terms permit and the author deliberately applies a compatible alternative. Verify licenses from the license
text at a pinned upstream revision; repository metadata alone is insufficient evidence.

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
written from scratch. Do not classify the result as uninfluenced merely because no expression was copied.

For idea influence, `ATTRIBUTIONS.md` names the original author, project and exact path, pinned commit or tag,
the ideas retained, and the fact that the expression is independent. Record the source's license status, but
do not claim that its license governs independently written expression.

For copied, adapted, translated, or vendored material, the package also ships:

- `LICENSE.upstream` containing the upstream license text verbatim; and
- `NOTICE.upstream` when the upstream project supplies one or its license requires preservation.

Start `ATTRIBUTIONS.md` from `assets/ATTRIBUTIONS.template.md` when available. Preserve existing provenance
artifacts and notices during updates. If the source or license cannot be verified, stop before making an
authoritative attribution claim and report what is missing.

Check the upstream license before adapting material. When its terms do not permit the intended use or
redistribution, write an independent replacement from domain knowledge and do not copy the restricted
expression.
