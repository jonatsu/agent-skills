# Patch Workflow

Preparing a patch series for review, from the commit history to the revised version after review. Every rule here
that changed between kernel releases is read from the target tree, never recalled.

## Contents

- Read the Tree's Rules
- Shape the Series
- Format With git format-patch
- Find Recipients
- Send
- Revise After Review
- Stable Releases

## Read the Tree's Rules

Open `Documentation/process/submitting-patches.rst` in the target tree before you format anything. Rules that moved
between releases come from that file. Examples are subject prefixes, commit-message conventions, tag handling, and
the tree's policy on tool-written patches.

- When the subsystem has a handbook, read it through `Documentation/process/maintainer-handbooks.rst`.
- Find the tree a subsystem wants patches against in the `T:` entry of `MAINTAINERS`.
- In a vendor tree, follow the vendor's `README` or contribution document first. It may route changes through a
  review system instead of a mailing list.
- When the tree lacks a section this file describes, say so and follow the nearest rule the tree states.

## Shape the Series

Base the series on a well-known release point of the maintainer's tree, not on an arbitrary commit. A release or
release-candidate tag is a safe base.

Split the work so that each patch is one logical change that a reviewer can verify alone:

- Put an API change and its first user in separate patches.
- Keep a mechanical change across many files in one patch.
- When a patch moves code, leave the moved lines unmodified in that patch.
- When one patch depends on another, say "this patch depends on patch X" in its description.
- When a series passes about 15 patches, post the first part and wait for review before the rest.

Every patch must leave a kernel that builds and runs, because bisection can stop at any commit. The skill body gives
the command that proves it.

Write each commit message so that it stands alone, in this order:

1. The problem, and who sees it. Include the user-visible impact, because stable and vendor trees pick patches by
   impact.
2. Numbers for any performance, memory, stack, or size claim, plus the cost the change adds.
3. What the change does, in imperative mood ("make xyzzy do frotz").

Add these details:

- Wrap the body at 75 columns.
- Write the subject as `subsystem: summary`, at most 70 to 75 characters. It states both the change and its reason.
- Inference: copy the `subsystem:` prefix from `git log --oneline` on the files you touch.
- Name another commit by at least 12 characters of its hash plus its one-line summary.
- Trim a backtrace to the frames that show the call chain. Drop timestamps, module lists, and register dumps.

A resubmitted patch repeats the full description, because a reviewer may never have received the earlier version.

## Format With git format-patch

Work on a topic branch that tracks the maintainer's branch, so that `--base=auto` can find the base commit:

```sh
git checkout -t -b my-topic <maintainer-branch>
# edit and commit
git format-patch --base=auto --cover-letter -o outgoing/ <maintainer-branch>
```

`--base` appends a `base-commit:` line to the cover letter, so reviewers and CI can apply the series without
guessing. It needs git 2.9.0 or later. The base commit must exist in an official maintainer or mainline tree. A commit
only you can reach is useless to others. Without git, add the same line by hand.

Edit `outgoing/0000-cover-letter.patch`. Git writes the placeholders `*** SUBJECT HERE ***` and `*** BLURB HERE ***`.
Replace both. Cover-letter text never reaches the kernel changelog, so each patch carries its own full description.

For a revised series, give the version to git instead of editing subjects:

```sh
git format-patch -v2 --base=auto --cover-letter --range-diff=<previous-tip> -o outgoing/ <maintainer-branch>
```

- `-v<n>` (`--reroll-count` in the git manual) prefixes file names with `v<n>-` and sets the subject prefix to
  `[PATCH v<n> M/N]`.
- `--range-diff=<previous-tip>` puts a comparison with the previous version into the cover letter when both versions
  share a base. When the base changed, give the previous version as a revision range. The git manual also documents
  `--interdiff`.
- `--rfc` marks a series as a request for comments.
- `--subject-prefix` replaces `PATCH`. Use it only when the tree or the maintainer asks for a different prefix.

Inference: tag each posted version before you rewrite the branch, because `--range-diff` needs the old tip.

Run the checks from the skill body on the generated files. Then run `git am` on the series in a clean checkout of the
base to prove that the mail form applies.

## Find Recipients

Pass the paths of the generated patches to `scripts/get_maintainer.pl`:

```sh
scripts/get_maintainer.pl outgoing/*.patch
```

Send to the maintainers it lists and to the subsystem list. Add developers who recently changed the same files,
found with `git log`, and anyone whose report prompted the patch.

- When no maintainer exists, the tree's `submitting-patches.rst` names the fallback maintainer and list.
- For a userspace interface change, add the manual-pages maintainer from `MAINTAINERS` and the API list the document
  names.
- Report an exploitable security bug privately, as `Documentation/process/security-bugs.rst` says. Keep that patch off
  every public list.
- Keep the mail off unrelated lists and people. Mail the top-level maintainer only when the tree says to.
- In a vendor tree, `MAINTAINERS` may be stale or absent. Ask the user who reviews changes (inference).

For a fix that goes through mainline, the stable tag in the commit message reaches the stable list (see Stable
Releases); `git send-email` copies the list from that tag, so send no separate mail (inference).

## Send

Sending posts mail to public lists, and nobody can recall it. Stop after formatting. Give the user the generated
files and the exact command, and send only on the user's instruction.

- Send patches inline as plain text. Attachments, compression, and links in place of the patch make review harder.
- Use `git send-email`, which the tree's document strongly recommends. Its tutorial is at `https://git-send-email.io`.
- When the tree documents another tool, use that one. Mainline names `b4` for tracking dependencies, running
  checkpatch, and formatting and sending mail.
- Send the series to yourself first and confirm that the patches arrive unwrapped. The tree's
  `Documentation/process/email-clients.rst` covers clients that corrupt patches.
- Let the tool thread the mails as replies to the first one. Avoid `--chain-reply-to`, which nests a long series
  deeply.
- Do not link a new version to the old one with `In-Reply-To`. Put a `lore.kernel.org` link to the earlier version in
  the cover letter.

Wait at least one week before a reminder, longer during a merge window. Comments typically arrive within two to three
weeks. When nothing arrives, check the recipients first. After a couple of weeks, resend an unchanged series with
`RESEND` in the subject prefix. Never use `RESEND` on a modified series.

## Revise After Review

Answer every review comment and thank the reviewer. A comment that leads to no code change still needs an answer. Add
a changelog entry or a code comment, so the next reviewer sees the reasoning.

- Reply inline, trim the quoted text to what you answer, and never top-post.
- Explain a technical disagreement with reasons. Reconsider when other reviewers side with the first one.
- Add every person who commented to the Cc list of the next version.
- Answer the earlier comments before you post the revision.
- Carry or drop reviewer-supplied tags as the tree's `submitting-patches.rst` says. Record each dropped one and the
  reason in the changelog.

Write a patch's changelog below its `---` line, where `git am` discards it. Never put it above the end of the commit
message. List the newest version first, and add `lore.kernel.org` links to earlier versions when you have them:

```text
vendor: example: fix probe error path

Release the clock when the reset line is missing, because the
probe function leaked it on that path.
---
Changes in v3:
- Release the clock in the error path, as asked in review.

Changes in v2:
- Drop the unused local variable.

v2: https://lore.kernel.org/example/v2-link
v1: https://lore.kernel.org/example/v1-link

 drivers/example/foo.c | 5 +++--
```

For a series, put the combined changelog in the cover letter. Per-patch notes go below that patch's `---`. The tree's
document allows either place.

## Stable Releases

A fix for a released kernel follows `Documentation/process/stable-kernel-rules.rst`. Read it from the tree, because
the rules and the tag syntax change.

The tree's `stable-kernel-rules.rst` lists requirements such as these:

- The fix, or an equivalent, already exists in mainline.
- It is obviously correct and tested, and at most 100 lines with context.
- It follows `submitting-patches.rst`.
- It fixes a real bug that bothers people, or only adds a device ID. Theoretical problems and cosmetic cleanups do
  not qualify.

It then offers three routes:

1. Mark the mainline patch with a stable tag in its sign-off area. This route is strongly preferred. The stable team
   applies the patch once it reaches mainline. The file defines the exact tag text, including how to name a version
   or a prerequisite commit.
2. After the fix reaches mainline, mail the stable list. Give the patch subject, the commit ID, the reason, and the
   wanted kernel versions.
3. When the fix needs changes to apply to an older series, mail the adjusted patch to the stable list. Name the
   upstream commit ID in the changelog as the file prescribes, and document every deviation from the upstream patch.

When route 2 or 3 names specific series, the fix must also be in every newer supported stable series. Otherwise
users regress when they upgrade. The stable team answers with an ACK or NAK and queues the patch. Reviewers then get
48 hours before a release candidate appears. Test that candidate and report the result on the list.

The release-candidate tree is rebased often and serves testing only. Security fixes bypass the normal stable review
and follow `Documentation/process/security-bugs.rst`.

A vendor tree on a long-term kernel takes stable updates in its own way. Ask the user which process applies
(inference).
