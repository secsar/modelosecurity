# Security review workflow

A review package brings decisions and evidence together while leaving detailed models in their owning repositories.

## 1. Establish the protection need

Record the business function, system boundary, identities, data sensitivity, and operating environment. Produce named requirements with observable expected behavior, an accountable owner, and explicit exclusions.

“Secure access” is too vague. “A new read decision after committed membership revocation must deny access” can be examined.

## 2. Describe intended behavior and failure scenarios

Develop a security model for policy rules and properties. Develop a threat model for how enforcement or assumptions could fail. Reference specific immutable versions. Do not copy the detailed documents into every package.

## 3. Make an architecture decision

Compare choices against requirements, costs, usability, assumptions, and remaining exposure. Assign responsibility for implementing and maintaining the decision. Use the [decision record](../templates/security-decision.md).

## 4. Examine evidence

Describe the setup, expected permitted and denied behavior, system version, and limitations. Store evidence in an authorized location. Public demonstrations must use synthetic records.

Create a [review package](review-package.md) linking requirements to decisions and evidence. Ask whether the evidence is relevant, trustworthy, current, and sufficient. The local tool checks only structure, declared status, version equality, and file digest consistency.

## 5. Decide and revisit

Record conclusions, gaps, and any acceptance with scope and an accountable owner. Readiness is input to the decision, not approval itself. State what changes would invalidate the conclusion.

## Example trace

| Layer | Identifier | Example |
| --- | --- | --- |
| Requirement | R-02 | Committed revocation affects new read decisions |
| Security model | SM-01 / P-02 | Revocation semantics |
| Threat model | TM-01 / T-02 | Stale membership decision |
| Decision | D-01 | Authoritative authorization at content release |
| Evidence | E-02 | Planned revocation observation |
| Outcome | Incomplete | A plan is not an executed observation |

See the [fictional decision](../examples/document-access-decision.md).
