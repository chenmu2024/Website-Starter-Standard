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


def seo_evidence(errors=0, warnings=0):
    findings = []
    for index in range(errors):
        findings.append({"severity": "error", "code": f"ERR_{index}", "page": "/",
                         "message": "Fixture error"})
    for index in range(warnings):
        findings.append({"severity": "warning", "code": f"WARN_{index}", "page": "/",
                         "message": "Fixture warning"})
    return {"scope": "Built static HTML only", "base_url": "https://example.org",
            "pages_scanned": 1,
            "summary": {"error": errors, "warning": warnings, "info": 0},
            "pages": [{"route": "/", "title": "Example"}], "findings": findings}


def browser_evidence(expected=1, unexpected=0, flaky=0, skipped=0, errors=None, result_count=None):
    if result_count is None:
        result_count = expected + unexpected + flaky + skipped
    return {
        "errors": errors or [],
        "stats": {"expected": expected, "unexpected": unexpected, "flaky": flaky, "skipped": skipped},
        "suites": [{"title": "e2e", "specs": [{"title": "task",
                    "tests": [{"results": [{"status": "passed"} for _ in range(result_count)]}]}]}],
    }


def calculation_evidence(status="PASS"):
    return {"status": status, "cases_checked": 3, "errors": [],
            "scope": ("schema-only; NOT a calculation pass" if status == "SCHEMA_VALID"
                      else "actual runtime outputs compared to independent golden fixtures")}


def deployment_evidence():
    names = ("homepage", "home-canonical", "production-indexable", "home-title",
             "route:/robots.txt", "route:/sitemap.xml", "sitemap-xml", "sitemap-coverage",
             "real-404", "deployed-commit", "route:/tool/", "canonical:/tool/",
             "indexable:/tool/", "preview-noindex")
    return {"scope": "live HTTP only; not Cloudflare account/WAF/verified bot/GSC or AI citations",
            "production": "https://example.org", "preview": None, "status": "PASS", "errors": [],
            "checks": [{"name": name,
                        "status": "NOT_APPLICABLE" if name == "preview-noindex" else "PASS",
                        "detail": "Fixture check"} for name in names]}


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
        self.put("seo.json", seo_evidence(warnings=2))
        self.put("browser.json", browser_evidence(expected=45))
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
        self.put("seo.json", seo_evidence(errors=1))
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
        self.put("calc.json", calculation_evidence("SCHEMA_VALID"))
        self.put("browser.json", browser_evidence(expected=20, skipped=1))
        manifest = {"version": 1, "checks": [
            {"id": "calculation", "type": "calculation", "required": True, "file": "calc.json"},
            {"id": "browser", "type": "playwright", "required": True, "file": "browser.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual([x["status"] for x in report["checks"]], ["NOT_RUN", "PARTIAL"])

    def test_flaky_browser_and_unsubstantiated_manual_pass_fail(self):
        self.put("browser.json", browser_evidence(expected=10, flaky=1))
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

    def test_optional_failure_is_visible_but_does_not_fail_required_gate(self):
        self.put("seo.json", seo_evidence())
        self.put("browser.json", browser_evidence(expected=5))
        self.put("exports.json", {"status": "FAIL"})
        manifest = {"version": 1, "checks": [
            {"id": "seo", "type": "seo", "required": True, "file": "seo.json"},
            {"id": "browser", "type": "playwright", "required": True, "file": "browser.json"},
            {"id": "exports", "type": "exports", "required": False, "file": "exports.json"}
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["checks"][2]["status"], "FAIL")
        self.assertTrue(report["warnings"])
        self.assertFalse(report["errors"])


    def test_playwright_run_level_teardown_errors_block_green_test_stats(self):
        evidence = browser_evidence(expected=25, errors=[{"message": "globalTeardown failed"}])
        status, detail = compiler.classify("playwright", evidence)
        self.assertEqual(status, "FAIL")
        self.assertIn("setup/teardown", detail)


    def test_all_browser_tests_failed_is_fail_not_not_run(self):
        evidence = browser_evidence(expected=0, unexpected=15)
        status, detail = compiler.classify("playwright", evidence)
        self.assertEqual(status, "FAIL")
        self.assertIn("unexpected=15", detail)



    def test_malformed_minimal_pass_reports_are_rejected(self):
        cases = [
            ("seo", {"summary": {"error": False, "warning": 0, "info": 0},
                     "pages_scanned": 1, "pages": [{"route": "/"}], "findings": []}),
            ("calculation", {"status": "PASS"}),
            ("exports", {"status": "PASS"}),
            ("deployment", {"status": "PASS"}),
            ("playwright", {"stats": {"expected": 1, "unexpected": 0, "flaky": 0, "skipped": 0},
                            "errors": []}),
        ]
        for kind, evidence in cases:
            with self.subTest(kind=kind):
                status, detail = compiler.classify(kind, evidence)
                self.assertEqual(status, "FAIL", detail)

    def test_seo_summary_must_match_findings(self):
        evidence = seo_evidence()
        evidence["summary"]["error"] = 1
        status, detail = compiler.classify("seo", evidence)
        self.assertEqual(status, "FAIL")
        self.assertIn("disagree", detail)

    def test_playwright_stats_must_match_concrete_result_records(self):
        evidence = browser_evidence(expected=3, result_count=1)
        status, detail = compiler.classify("playwright", evidence)
        self.assertEqual(status, "FAIL")
        self.assertIn("only 1 result records", detail)

    def test_all_skipped_browser_tests_are_partial_not_not_run(self):
        evidence = browser_evidence(expected=0, skipped=2)
        status, detail = compiler.classify("playwright", evidence)
        self.assertEqual(status, "PARTIAL")
        self.assertIn("skipped=2", detail)

    def test_deployment_pass_requires_live_release_check_set_and_critical_route(self):
        evidence = {
            "scope": "live HTTP only; no Cloudflare account verification",
            "production": "https://example.org",
            "status": "PASS", "errors": [],
            "checks": [{"name": "homepage", "status": "PASS", "detail": "HTTP 200"}],
        }
        status, detail = compiler.classify("deployment", evidence)
        self.assertEqual(status, "FAIL")
        self.assertIn("missing required checks", detail)

    def test_invalid_optional_manifest_entry_invalidates_manifest(self):
        manifest = {"version": 1, "checks": [
            {"id": "seo", "type": "seo", "required": True, "file": "seo.json"},
            {"id": "optional", "type": "manual", "required": "", "file": "optional.json"},
        ]}
        report = compiler.compile_report(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["decision"], "INVALID_MANIFEST")
        self.assertIn("required must be boolean", report["errors"][0])



if __name__ == "__main__":
    unittest.main()
