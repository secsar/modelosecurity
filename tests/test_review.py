import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.review import PackageError, evaluate, markdown, reject_duplicate_keys


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        data = b"Synthetic observation, not production evidence.\n"
        (self.root / "evidence.txt").write_bytes(data)
        self.package = {"schema_version": "1.0", "title": "Synthetic review", "system_version": "v1",
                        "requirements": [{"id": "R-1", "statement": "Tenant isolation", "required": True}],
                        "decisions": [{"id": "D-1", "summary": "Authorize each read", "owner": "Example owner", "status": "implemented", "requirement_ids": ["R-1"]}],
                        "evidence": [{"id": "E-1", "requirement_id": "R-1", "decision_id": "D-1", "status": "collected", "result": "pass", "system_version": "v1", "artifact": "evidence.txt", "sha256": hashlib.sha256(data).hexdigest()}]}

    def run_package(self):
        return evaluate(self.package, self.root)

    def test_matching_record_is_ready_for_review_not_certification(self):
        result = self.run_package()
        self.assertTrue(result["ready_for_review"])
        self.assertIn("does not authenticate evidence", result["limitation"])

    def test_modified_artifact_blocks_readiness(self):
        (self.root / "evidence.txt").write_text("changed")
        self.assertEqual(["R-1"], self.run_package()["blocking_requirements"])

    def test_missing_artifact(self):
        (self.root / "evidence.txt").unlink()
        self.assertIn("artifact missing", self.run_package()["evidence"][0]["reasons"])

    def test_stale_version(self):
        self.package["evidence"][0]["system_version"] = "v0"
        self.assertFalse(self.run_package()["ready_for_review"])

    def test_planned_evidence_does_not_count(self):
        self.package["evidence"][0].update(status="planned", result="not_run")
        self.assertFalse(self.run_package()["ready_for_review"])

    def test_planned_evidence_cannot_claim_pass(self):
        self.package["evidence"][0]["status"] = "planned"
        with self.assertRaises(PackageError):
            self.run_package()

    def test_pass_does_not_override_current_failure(self):
        failed = copy.deepcopy(self.package["evidence"][0])
        failed.update(id="E-2", result="fail")
        self.package["evidence"].append(failed)
        self.assertFalse(self.run_package()["ready_for_review"])

    def test_unknown_reference(self):
        self.package["evidence"][0]["requirement_id"] = "R-unknown"
        with self.assertRaises(PackageError):
            self.run_package()

    def test_duplicate_id(self):
        self.package["requirements"] *= 2
        with self.assertRaises(PackageError):
            self.run_package()

    def test_path_escape(self):
        self.package["evidence"][0]["artifact"] = "../private.txt"
        with self.assertRaises(PackageError):
            self.run_package()

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "outside.txt"
            target.write_text("outside")
            (self.root / "link.txt").symlink_to(target)
            self.package["evidence"][0]["artifact"] = "link.txt"
            with self.assertRaises(PackageError):
                self.run_package()

    def test_proposed_decision_does_not_count(self):
        self.package["decisions"][0]["status"] = "proposed"
        self.assertFalse(self.run_package()["ready_for_review"])

    def test_uncovered_requirement_blocks(self):
        self.package["requirements"].append({"id": "R-2", "statement": "Revocation", "required": True})
        self.assertEqual(["R-2"], self.run_package()["blocking_requirements"])

    def test_boolean_required_is_strict(self):
        self.package["requirements"][0]["required"] = "false"
        with self.assertRaises(PackageError):
            self.run_package()

    def test_report_escapes_html_and_table_delimiters(self):
        self.package["title"] = "<script>|test"
        self.assertIn("&lt;script&gt;\\|test", markdown(self.run_package()))

    def test_duplicate_json_keys_rejected_at_all_depths(self):
        samples = [
            '{"schema_version":"bad","schema_version":"1.0"}',
            '{"evidence":[{"result":"fail","result":"pass"}]}',
            '{"requirements":[{"required":true,"required":false}]}',
            '{"outer":{"inner":{"id":"a","id":"a"}}}',
        ]
        for sample in samples:
            with self.subTest(sample=sample), self.assertRaises(PackageError):
                json.loads(sample, object_pairs_hook=reject_duplicate_keys)

    def test_cli_rejects_contradictory_duplicate_keys(self):
        command = [sys.executable, "-m", "tools.review", str(self.root / "ambiguous.json"), "--strict", "--format", "json"]
        valid = json.dumps(self.package)
        samples = [
            valid.replace('"result": "pass"', '"result": "fail", "result": "pass"'),
            valid.replace('"required": true', '"required": true, "required": false'),
            valid.replace('"schema_version": "1.0"', '"schema_version": "0.0", "schema_version": "1.0"'),
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                (self.root / "ambiguous.json").write_text(sample)
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertIn("duplicate JSON key", result.stderr)

    def test_cli_exit_codes(self):
        path = self.root / "package.json"
        path.write_text(json.dumps(self.package))
        command = [sys.executable, "-m", "tools.review", str(path), "--strict", "--format", "json"]
        good = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(0, good.returncode)
        self.assertTrue(json.loads(good.stdout)["ready_for_review"])
        self.package["evidence"] = []
        path.write_text(json.dumps(self.package))
        self.assertEqual(1, subprocess.run(command, capture_output=True).returncode)
        path.write_text("not JSON")
        self.assertEqual(2, subprocess.run(command, capture_output=True).returncode)


if __name__ == "__main__":
    unittest.main()
