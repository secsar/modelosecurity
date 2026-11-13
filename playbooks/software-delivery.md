# Software delivery review

Use when source changes produce artifacts that can reach production.

## Map the chain

Describe source ownership, branch rules, build identities, dependency inputs, artifact storage, approval, deployment identity, and rollback. Identify where content or authority can be substituted.

| Decision | Questions | Evidence |
| --- | --- | --- |
| Source acceptance | Who can approve and merge? How are exceptions controlled? | Policy configuration and authorized/denied changes |
| Build trust | Can untrusted contributions access credentials or modify trusted outputs? | Workflow review and safe fixture execution |
| Dependencies | Are inputs fixed and updates reviewed? | Inventory, version strategy, and update record |
| Artifact identity | Can deployment identify exactly what was built? | Digests connecting built, stored, approved, and deployed artifacts |
| Release authority | Is approval bound to an artifact and environment? | Substitution invalidates approval |
| Recovery | Can a known artifact be restored under controlled authority? | Synthetic rollback and audit trail |

## Interpretation

An artifact hash supports content identity relative to a trusted reference. It does not prove that source, dependencies, or the build were trustworthy.

A successful build is not a security assessment. State which tests ran, their scope, and unresolved failures. Record release requirements, decisions, and evidence in the [review package](../docs/review-package.md). Keep credentials and production deployment configuration out of public examples.
