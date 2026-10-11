# Diagnosing Repository Access Failures

Probe before concluding that a repository is broken or empty. Send the same headers APT sends, because some
servers and CDNs answer differently for another client string:

```sh
ua="Debian APT-HTTP/1.3 (3.2.0) non-interactive"
curl -s -o /dev/null -w '%{http_code}  InRelease\n' -A "$ua" "$BASE/dists/$SUITE/InRelease"
for ext in .xz .gz .bz2 ""; do
  curl -s -o /dev/null -w "%{http_code} %{size_download}  Packages${ext:-  (plain)}\n" -A "$ua" \
    "$BASE/dists/$SUITE/main/binary-$ARCH/Packages$ext"
done
```

For a flat repository, probe `$BASE/$DIR/InRelease` and `$BASE/$DIR/Packages$ext` instead. Use a GET rather
than `curl -I`, because some object stores answer HEAD and GET under different rules.

| Result                               | Meaning                                                                    |
| ------------------------------------ | -------------------------------------------------------------------------- |
| 404 on InRelease and Release         | Wrong base URL or suite; compare with the publisher's `sources.list` line  |
| 200 on InRelease, 404 on every index | Architecture or component not published; read `Architectures:` in Release  |
| 200 on InRelease, 403 on every index | The repository exists, but its indexes are access-controlled               |
| 403 on `.xz`, 200 on `.gz`           | Per-object permissions; the script falls through to the format that serves |
| 200 with zero bytes                  | An empty placeholder index; no packages for that architecture              |
| 403 on every path                    | Server-wide policy, such as an IP allowlist or required credentials        |

## Object-Store Hosting

Repositories served straight from an object store, such as Amazon S3, report missing and forbidden objects
alike as 403 when listing is denied. Separate the cases with these probes:

1. Request the same key in virtual-hosted form (`bucket.s3.amazonaws.com/key`) and in path form
   (`s3.amazonaws.com/bucket/key`). A CDN in front can cache a policy for one form only.
2. Request a sibling the publisher links publicly, such as the signing key or the install script. A 200 there
   with 403 on the indexes means the repository prefix is restricted on purpose.
3. Read the publisher's install script for the step that grants access: a device registration, a token, an
   authenticated `sources.list` entry, or presigned URLs.

A restricted prefix is an access decision by the publisher. Stop and report it, with the probe results, and ask
the user for the credentials or access route the publisher provides. Do not search for a way around the
restriction.
