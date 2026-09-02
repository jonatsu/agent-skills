# Provenance and Licensing

Every skill authored under this workflow records:

- the current author in `metadata.author`; and
- the applicable license in the Agent Skills top-level `license` field.

Use the target repository's license for original work. Use the upstream license for derived work unless its
terms permit and the author deliberately applies a compatible alternative. Verify licenses from the license
text at a pinned upstream revision; repository metadata alone is insufficient evidence.

## Adapted Skills

An adapted or vendored skill also ships:

- `ATTRIBUTIONS.md` naming original authors, source project and path, pinned commit or tag, current adapter,
  and material adaptation;
- `LICENSE.upstream` containing the upstream license text verbatim; and
- `NOTICE.upstream` when the upstream project supplies one or its license requires preservation.

Start `ATTRIBUTIONS.md` from `assets/ATTRIBUTIONS.template.md` when available. Preserve existing provenance
artifacts and notices during updates. If the source or license cannot be verified, stop before making an
authoritative attribution claim and report what is missing.

Check the upstream license before adapting material. When its terms do not permit the intended use or
redistribution, write an independent replacement from domain knowledge and do not copy the restricted
expression.
