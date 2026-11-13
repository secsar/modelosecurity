# Evidence readiness tool

`python -m tools.review PACKAGE` validates local JSON and emits Markdown or JSON. Python 3.10+, standard library, no network calls.

## Contract version 1.0

| Object | Required fields | Rules |
| --- | --- | --- |
| Root | schema_version, title, system_version, requirements, decisions, evidence | schema_version is string 1.0; at least one requirement |
| Requirement | id, statement, required | required is a JSON boolean |
| Decision | id, summary, owner, status, requirement_ids | proposed, approved, or implemented; referenced requirements exist |
| Evidence | id, requirement_id, decision_id, status, result, system_version | Links agree with the decision's requirements |
| Collected evidence | artifact, sha256 | Relative path inside package directory; lowercase SHA-256 digest |

IDs contain letters, numbers, underscores, or hyphens and are unique within each type. Planned evidence has result not_run. Collected evidence has result pass or fail. Contradictory states, broken references, and duplicate JSON keys at any nesting depth are invalid.

See the [sample package](../examples/review-package/package.json).

## Readiness semantics

A requirement is supported for this tool when at least one record is collected, declares pass, references an implemented decision, matches the current system version, and has a local artifact with matching digest.

A current-version failure on that requirement blocks readiness even if another record passes. Missing evidence blocks required items; optional items do not block the package.

ready_for_review means no required item is blocked. It does **not** mean ready for production. Files can be fabricated, incomplete, irrelevant, or scientifically weak. The tool does not authenticate evidence or assess its sufficiency.

## Commands and exit codes

```bash
python -m tools.review examples/review-package/package.json
python -m tools.review examples/review-package/package.json --format json
python -m tools.review examples/review-package/package.json --strict
python -m unittest discover -s tests -v
```

| Code | Meaning |
| --- | --- |
| 0 | Valid package; in strict mode, no required evidence gap |
| 1 | Strict mode found incomplete required evidence |
| 2 | Invalid input, inaccessible package, or malformed references |

Without --strict, an incomplete but valid package exits 0. Inspect ready_for_review or enable strict mode for an automation gate.

## File handling and limits

Artifact paths resolve relative to the package file. Traversal and symlink escape are rejected. Artifacts are read for hashing, never executed. Use trusted local packages and bounded file sizes; this tool is not a sandbox for hostile filesystem workloads.

Version matching is exact string comparison. No expiry policy or external identity verification is implemented.

Tests cover modified/missing artifacts, stale versions, planned evidence, status contradictions, reference integrity, path escape, conflicting outcomes, CLI codes, and report escaping. They test the tool, not a deployed document service.
