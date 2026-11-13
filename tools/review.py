"""Validate a local security decision package and report evidence readiness.

This checks declared traceability and artifact integrity, not security efficacy.
Python 3.10+; standard library only; no network access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


class PackageError(ValueError):
    """The input does not conform to the review package contract."""


def reject_duplicate_keys(pairs):
    """Reject ambiguous JSON at every object depth, before field validation."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise PackageError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise PackageError(f"{field}: expected a non-empty string")
    return value


def _table(value, name, fields):
    if not isinstance(value, list):
        raise PackageError(f"{name}: expected a list")
    result = {}
    for i, row in enumerate(value):
        if not isinstance(row, dict):
            raise PackageError(f"{name}[{i}]: expected an object")
        for field in fields:
            _text(row.get(field), f"{name}[{i}].{field}")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", row["id"]):
            raise PackageError(f"{name}[{i}].id: use letters, numbers, hyphens or underscores")
        if row["id"] in result:
            raise PackageError(f"{name}: duplicate ID {row['id']}")
        result[row["id"]] = row
    return result


def evaluate(package, base):
    """Return deterministic results. Raise PackageError for broken references/schema."""
    if not isinstance(package, dict) or package.get("schema_version") != "1.0":
        raise PackageError("schema_version must be '1.0'")
    title = _text(package.get("title"), "title")
    version = _text(package.get("system_version"), "system_version")
    reqs = _table(package.get("requirements"), "requirements", ("id", "statement"))
    decisions = _table(package.get("decisions"), "decisions", ("id", "summary", "owner", "status"))
    evidence = _table(package.get("evidence"), "evidence", ("id", "requirement_id", "decision_id", "status", "result", "system_version"))
    if not reqs:
        raise PackageError("requirements must contain at least one item")
    for row in reqs.values():
        if type(row.get("required")) is not bool:
            raise PackageError(f"{row['id']}.required: expected boolean")
    for row in decisions.values():
        if row["status"] not in {"proposed", "approved", "implemented"}:
            raise PackageError(f"{row['id']}: invalid decision status")
        links = row.get("requirement_ids")
        if not isinstance(links, list) or not links or not all(isinstance(x, str) for x in links):
            raise PackageError(f"{row['id']}.requirement_ids: expected a non-empty string list")
        if len(set(links)) != len(links) or any(x not in reqs for x in links):
            raise PackageError(f"{row['id']}: duplicate or unknown requirement reference")
    root = Path(base).resolve()
    evidence_results = []
    supported = set()
    for row in evidence.values():
        rid, did = row["requirement_id"], row["decision_id"]
        if rid not in reqs or did not in decisions or rid not in decisions[did]["requirement_ids"]:
            raise PackageError(f"{row['id']}: broken requirement/decision traceability")
        if row["status"] not in {"planned", "collected"} or row["result"] not in {"pass", "fail", "not_run"}:
            raise PackageError(f"{row['id']}: invalid evidence status or result")
        if row["status"] == "planned" and row["result"] != "not_run":
            raise PackageError(f"{row['id']}: planned evidence cannot have a test result")
        if row["status"] == "collected" and row["result"] == "not_run":
            raise PackageError(f"{row['id']}: collected evidence needs pass or fail")
        reasons = []
        if row["status"] == "planned":
            reasons.append("not collected")
        else:
            artifact = _text(row.get("artifact"), f"{row['id']}.artifact")
            digest = _text(row.get("sha256"), f"{row['id']}.sha256")
            if not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise PackageError(f"{row['id']}: sha256 must be 64 lowercase hexadecimal characters")
            target = (root / artifact).resolve()
            if Path(artifact).is_absolute() or not target.is_relative_to(root):
                raise PackageError(f"{row['id']}: artifact must stay inside the package directory")
            if not target.is_file():
                reasons.append("artifact missing")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                reasons.append("artifact digest mismatch")
        if row["result"] != "pass":
            reasons.append(f"result is {row['result']}")
        if row["system_version"] != version:
            reasons.append("system version mismatch")
        if decisions[did]["status"] != "implemented":
            reasons.append("decision not implemented")
        if not reasons:
            supported.add(rid)
        evidence_results.append({"id": row["id"], "requirement_id": rid, "supports_readiness": not reasons, "reasons": reasons})
    # A later failed observation for a requirement is not cancelled by another passing record.
    failed = {row["requirement_id"] for row in evidence.values() if row["result"] == "fail" and row["system_version"] == version}
    supported -= failed
    missing = sorted(rid for rid, row in reqs.items() if row["required"] and rid not in supported)
    return {"title": title, "system_version": version, "ready_for_review": not missing,
            "required_count": sum(row["required"] for row in reqs.values()),
            "supported_required_count": sum(row["required"] and rid in supported for rid, row in reqs.items()),
            "blocking_requirements": missing, "failed_requirements": sorted(failed),
            "evidence": evidence_results,
            "limitation": "Readiness checks declared records and local file digests; it does not authenticate evidence, assess sufficiency, approve release, or certify security."}


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").replace("\r", " ").replace("<", "&lt;").replace(">", "&gt;")


def markdown(result):
    lines = [f"# {_cell(result['title'])}", "", f"System version: {_cell(result['system_version'])}", "",
             "**Readiness: " + ("READY FOR HUMAN REVIEW" if result["ready_for_review"] else "INCOMPLETE") + "**", "",
             f"Supported required items: {result['supported_required_count']}/{result['required_count']}", "",
             "| Evidence | Requirement | Record check |", "| --- | --- | --- |"]
    for row in result["evidence"]:
        outcome = "; ".join(row["reasons"]) or "Matching passing record; human assessment still required"
        lines.append(f"| {row['id']} | {row['requirement_id']} | {_cell(outcome)} |")
    lines += ["", "Blocking requirements: " + (", ".join(result["blocking_requirements"]) or "None"), "",
              "Failed current-version requirements: " + (", ".join(result["failed_requirements"]) or "None"), "", result["limitation"], ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="exit 1 when required evidence is incomplete")
    args = parser.parse_args(argv)
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"),
                             object_pairs_hook=reject_duplicate_keys)
        result = evaluate(package, args.package.parent)
    except (OSError, ValueError, TypeError) as error:
        print(f"Invalid package: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2) if args.format == "json" else markdown(result), end="\n")
    return 1 if args.strict and not result["ready_for_review"] else 0


if __name__ == "__main__":
    sys.exit(main())
