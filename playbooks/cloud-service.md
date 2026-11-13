# Cloud service and tenant-isolation review

Use when a service handles records or operations for multiple organizations. This is a generic review guide, not a claim of compliance with a cloud standard.

## Bound the review

Identify tenants, identities, administrative roles, records, exports, queues, workers, caches, and backup/restore paths. Record every way bytes can leave storage, including previews and reports.

| Question | Decision to record | Evidence to request | Review trigger |
| --- | --- | --- | --- |
| Where is tenant context established? | Authoritative membership and object-ownership checks | Permitted same-tenant and denied cross-tenant access across release paths | New endpoint or sharing |
| When does revocation take effect? | Authorization point, cache invalidation, in-progress behavior | Concurrent revocation/read tests across instances | New cache or export |
| Can workers bypass tenant boundaries? | Scoped permissions and immutable tenant metadata | Worker configuration and negative tests | New service identity |
| Are approvals tied to exact content? | Version-bound publication | Stale-approval/replacement interleavings | New transformation |
| How is capacity shared? | Tenant quotas and bounded queues | Controlled load with rejection and legitimate availability | Workload change |
| Can restoration merge tenant data? | Tenant-aware restore process | Synthetic restore and ownership checks | Backup/schema change |

## Interpret the evidence

Passing an API test does not prove database, worker, export, and restore paths share the same protection. Enumerate them separately. Encryption does not itself establish tenant authorization. Private-network placement and identity boundaries are distinct.

Create requirements for access, revocation, publication, and restoration. Link exact model versions, decisions, and evidence plans. The [review tool](../docs/review-package.md) exposes missing records before human assessment.

See [authenticated document delivery](../examples/document-access-decision.md).
