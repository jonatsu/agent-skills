# ADR 0002: Identify members through the organization's OpenID Connect provider

Status: accepted, 2026-08-18.

## Context

Customers sign in with their own organization's identity provider. Maintaining passwords in the service would add a
credential store that the team does not want to secure.

## Decision

Members authenticate through the organization's OpenID Connect provider. The service identifies a member by the
provider's `sub` claim together with the issuer, stored as the member's external reference. Roles (member and
administrator) are held by the service, not taken from the provider. The service stores no passwords.

## Consequences

- A member who changes email address keeps the same identity.
- The service learns of a removed member only at the member's next sign-in attempt, so removal does not by itself
  revoke the member's items or roles.
