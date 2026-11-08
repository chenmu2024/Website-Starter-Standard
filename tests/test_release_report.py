"""Tests for the required/optional release evidence compiler."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "compile_release_report.py"
spec = importlib.util.spec_from_file_location("release_report_compiler", SCRIPT)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class ReleaseReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def put(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf8")

    def test_required_pass_and_optional_missing_are_distinguished(self):
        self.put("seo.json", {"summary": {"error": 0, "warning": 2}})
        self.put("browser.json", {"stats": {"expected": 45, "unexpected": 0, "flaky": 0, "skipped": 0}})
        manifest = {"version": 1, "project": "Example", "checks": [
            {"id": "seo", "type": "seo", "required": True, "file": "seo.json"},
            {"id": "browser", "type": "playwright", "required": True, "file": "browser.json"},
            {"id": "physical-print", "type": "manual", "required": False, "file": "physical.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["decision"], "REQUIRED_GATES_PASS")
        self.assertEqual(report["checks"][2]["status"], "NOT_RUN")

    def test_missing_required_evidence_is_partial_not_pass(self):
        report = compiler.compile_report({"version": 1, "checks": [
            {"id": "browser", "type": "playwright", "required": True, "file": "missing.json"}
        ]}, self.root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["decision"], "EVIDENCE_INCOMPLETE")

    def test_required_failures_block_and_optional_failures_do_not_hide(self):
        self.put("seo.json", {"summary": {"error": 1, "warning": 0}})
        self.put("optional.json", {"status": "FAIL"})
        manifest = {"version": 1, "checks": [
            {"id": "seo", "type": "seo", "required": True, "file": "seo.json"},
            {"id": "exports", "type": "exports", "required": False, "file": "optional.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["checks"][1]["status"], "FAIL")
        self.assertTrue(any("exports" in item for item in report["warnings"]))

    def test_schema_only_calculation_and_skipped_browser_are_partial(self):
        self.put("calc.json", {"status": "SCHEMA_VALID"})
        self.put("browser.json", {"stats": {"expected": 20, "unexpected": 0, "flaky": 0, "skipped": 1}})
        manifest = {"version": 1, "checks": [
            {"id": "calculation", "type": "calculation", "required": True, "file": "calc.json"},
            {"id": "browser", "type": "playwright", "required": True, "file": "browser.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual([x["status"] for x in report["checks"]], ["NOT_RUN", "PARTIAL"])

    def test_flaky_browser_and_unsubstantiated_manual_pass_fail(self):
        self.put("browser.json", {"stats": {"expected": 10, "unexpected": 0, "flaky": 1, "skipped": 0}})
        self.put("manual.json", {"status": "PASS"})
        manifest = {"version": 1, "checks": [
            {"id": "browser", "type": "playwright", "required": True, "file": "browser.json"},
            {"id": "print", "type": "manual", "required": True, "file": "manual.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("reviewer, date and evidence" in x for x in report["errors"]))

    def test_manual_not_applicable_needs_reason_and_paths_are_confined(self):
        self.put("na.json", {"status": "NOT_APPLICABLE"})
        manifest = {"version": 1, "checks": [
            {"id": "physical", "type": "manual", "required": True, "file": "na.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        manifest["checks"][0]["file"] = "../outside.json"
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("escapes evidence directory", report["errors"][0])


if __name__ == "__main__":
    unittest.main()
