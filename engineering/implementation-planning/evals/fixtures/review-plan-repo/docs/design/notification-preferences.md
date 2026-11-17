# Design: Notification Preferences

Status: Accepted

## Behavior

Each user can turn email and in-app notifications on or off. Both default to on. Security notifications (password
change, new sign-in) are always sent on every channel regardless of preferences. Only the user, or an administrator of
the user's account, may change a user's preferences.

## Design

- Storage: table `preferences(user_id PRIMARY KEY, email INTEGER, in_app INTEGER)`, added by migration `0003`. A
  missing row means both channels on.
- `notify.preferences` module: `get_preferences(user_id)` and `set_preferences(actor, user_id, email, in_app)`, which
  raises `PermissionError` unless the actor is the user or an account administrator.
- `dispatch` gains a `category` argument (`"security"` or `"general"`) and filters channels by preference for
  `"general"` only. Existing callers that do not pass `category` keep the current behavior.

## Rollout

Ships in one release. Rollback is the previous release; the new table is ignored by older code.
