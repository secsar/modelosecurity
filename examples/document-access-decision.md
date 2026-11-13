# Example: Authenticated document delivery

**Decision ID:** EX-01 · **Revision:** 1  
**Status:** Proposed educational example  
**System:** fictional tenant document service  
**Owner and approval:** unassigned; no implementation approval claimed

## Context

Members of an organization read confidential documents through a service. Membership can be revoked while a user remains logged in. The design needs a clear definition of when that revocation affects access.

## Requirement

R-01: a new read decision after committed membership revocation must deny that user's access unless permission is granted again.

This requirement does not retract bytes already delivered or necessarily cancel a read authorized before revocation.

## Related analysis

- [Security model SM-01 revision 2](https://github.com/secsar/security-modeling/blob/ee792bbc07dbfb7beebb4e4830891e699c9210eb/case-studies/tenant-document-service.md): authorization and revocation semantics.
- [Threat model TM-01 revision 1](https://github.com/secsar/threat-modeling/blob/d0c35efd03594d8590aa07d0309a9bdfbbf7d599/case-studies/document-service.md): implementation failure scenarios and proposed validation.

The referenced documents remain the owners of their detailed specifications and scenarios.

## Options

| Option | Requirement fit | Operational tradeoff | Remaining exposure |
| --- | --- | --- | --- |
| Authenticated delivery with authoritative membership evaluation at each new read decision | Can satisfy R-01 if authorization observes committed state | Service handles delivery and must preserve consistent authorization semantics | Already delivered content remains available; implementation bypasses remain possible |
| Short-lived transferable download link without a revocation check | Does not satisfy R-01 while an issued link remains usable | Direct delivery can reduce application load | Link holder may initiate a new download after membership revocation |

A link mechanism with additional server-side revocation checks is a different option and would need its own analysis.

## Proposed decision

Use authenticated delivery and evaluate current authorization for each new read decision. Define the authorization point and concurrency behavior before implementation.

The reason is the revocation requirement, not a claim that one delivery pattern is universally preferable.

## Responsibilities

Application engineering owns authorization and content-release paths. Platform engineering owns authoritative state access and delivery capacity. The product owner confirms the behavior expected for in-progress downloads.

These are illustrative responsibilities, not assigned people.

## Validation plan

| ID | Setup and action | Expected outcome | Status |
| --- | --- | --- | --- |
| V-01 | Authorize a synthetic user, verify an allowed read, commit revocation, then start new reads across each service instance | Initial allowed read succeeds; subsequent decisions deny access | Not executed |
| V-02 | Coordinate a read and revocation concurrently | Result matches the documented authorization point and ordering | Not executed |
| V-03 | Attempt access through direct storage, preview, export, and other release paths | No path bypasses the required authorization | Not executed |
| V-04 | Exercise permitted reads under an agreed bounded load profile | Delivery meets the defined service target while enforcing authorization | Not executed |

## Evidence gaps and review triggers

No code, deployment, test result, or measured performance is included. Capacity targets and concurrency enforcement remain unspecified.

Revisit this decision when introducing offline access, sharing links, cross-tenant collaboration, authorization caches, or asynchronous exports.

