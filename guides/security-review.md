# Security review guide

Use this guide to turn a design discussion into a decision that can be reviewed and supported by evidence. Adapt the depth to the system and consequences.

## 1. Establish the decision

Describe the business function, affected users, sensitive data, and the decision being made. Name the owner and identify exclusions. Avoid starting with a product recommendation before stating the requirement.

Deliverable: a short scope statement and a concrete question.

## 2. Describe the system

Record components, data flows, external dependencies, administrative access, and changes in trust. Identify the source of identities, permissions, and authoritative records.

Deliverable: a diagram and an explanation of the relevant boundaries.

## 3. Define intended security behavior

Describe who may perform which actions and under what conditions. State lifecycle, revocation, and integrity requirements precisely.

Use the [security-modeling repository](https://github.com/secsar/security-modeling) for detailed policy and property specifications. Reference the exact model revision used.

## 4. Examine failure scenarios

Identify plausible ways the intended behavior could fail and the consequences. Distinguish assumptions from observed weaknesses.

Use the [threat-modeling repository](https://github.com/secsar/threat-modeling) for detailed scenarios, prioritization, and mitigation analysis.

## 5. Compare options

For each option, record:
- How it addresses the requirement.
- Which assumptions it needs.
- Operational and usability costs.
- Failure and recovery behavior.
- Remaining exposure.
- Evidence needed before adoption.

Use the [decision template](../templates/security-decision.md). Explain rejected alternatives so reviewers can understand the choice.

## 6. Plan validation

Specify the version under review, test setup, expected permitted and denied behavior, and evidence to retain. Include concurrency and failure behavior where relevant.

Record missing evidence as missing. A configured control, a passing test, and a proven property support different claims.

## 7. Record the outcome

Choose a clear status: Proposed, Approved for implementation, Implemented, or Validated with scope. Approval requires an actual accountable decision; a template or example cannot supply it.

Record unresolved conditions and changes that would trigger another review. Keep evidence and decisions versioned.

## Review completion

A review is ready for decision when scope, requirements, alternatives, responsible owners, validation criteria, and unresolved limitations are visible. Completion of the review does not by itself establish that a system is secure.
