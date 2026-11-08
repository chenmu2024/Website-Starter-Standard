"""Static contract tests for the copied P1 browser/export/i18n templates."""
import json
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class P1TemplateTests(unittest.TestCase):
    def test_playwright_cross_browser_template_covers_three_engines_and_five_viewports(self):
        config = (ROOT / "templates/playwright/playwright.config.ts").read_text()
        spec = (ROOT / "templates/playwright/site-quality.spec.ts").read_text()
        workflow = (ROOT / "templates/github-actions/website-browser-quality.yml").read_text()
        for browser in ("chromium", "firefox", "webkit"):
            self.assertIn(browser, config)
        for width in ("360", "390", "768", "1024", "1440"):
            self.assertIn(width, spec)
        for contract in ("documentWidth", "visibleBrokenImages", "unnamedControls", "pageerror"):
            self.assertIn(contract, spec)
        for native_name in ("\.labels", "labelledBy", "valueName", "imageInputAlt"):
            self.assertIn(native_name, spec)
        self.assertIn("npx playwright install --with-deps chromium firefox webkit", workflow)
        self.assertIn("npx playwright test --config=playwright.config.ts", workflow)
        self.assertIn("if: always()", workflow)
        self.assertIn("tools/compile_release_report.py", workflow)
        self.assertIn("tools/validate_export_artifacts.py", workflow)
        self.assertIn("SEO_BASE_URL", workflow)
        self.assertIn("CALC_RUNTIME_COMMAND", workflow)
        self.assertIn("EXPORT_MANIFEST", workflow)

    def test_visual_baselines_are_separate_opt_in_and_reviewable(self):
        config = (ROOT / "templates/playwright/visual.config.ts").read_text()
        spec = (ROOT / "templates/playwright/visual-baseline.spec.ts").read_text()
        workflow = (ROOT / "templates/github-actions/website-browser-quality.yml").read_text()
        self.assertIn("maxDiffPixelRatio", config)
        self.assertIn("QA_VISUAL_ROUTES_JSON", spec)
        self.assertIn("data-visual-mask", spec)
        self.assertIn("QA_VISUAL_ROUTES_JSON != '[]'", workflow)

    def test_export_manifest_and_validator_support_csv_pdf_svg(self):
        manifest = json.loads((ROOT / "templates/exports/export-manifest.example.json").read_text())
        self.assertEqual({x["kind"] for x in manifest["exports"]}, {"csv", "pdf", "svg"})
        script = (ROOT / "tools/validate_export_artifacts.py").read_text()
        for token in ("validate_csv", "validate_pdf", "validate_svg", "expected_text_contains",
                      "expected_page_size_pt", "numeric_tolerance"):
            self.assertIn(token, script)

    def test_multilingual_policy_maps_language_codes_to_routes(self):
        policy = json.loads((ROOT / "templates/indexation-policy.multilingual.example.json").read_text())
        group = policy["hreflang_groups"][0]["routes"]
        self.assertEqual(group["es-ES"], "/es/")
        self.assertEqual(group["pt-BR"], "/pt-br/")
        self.assertEqual(group["x-default"], "/")
        audit = (ROOT / "tools/seo_audit.py").read_text()
        for token in ("HREFLANG_SELF_MISSING", "HREFLANG_RETURN_MISSING",
                      "HREFLANG_GROUP_INCOMPLETE", "HREFLANG_TARGET_CANONICAL",
                      "SITEMAP_HREFLANG", "HREFLANG_SOURCE_MISMATCH"):
            self.assertIn(token, audit)

    def test_release_manifest_requires_seo_and_browser_evidence(self):
        manifest = json.loads((ROOT / "templates/release-evidence/manifest.example.json").read_text())
        required = {x["id"] for x in manifest["checks"] if x["required"]}
        self.assertIn("seo", required)
        self.assertIn("browser", required)
        self.assertIn("visual", {x["id"] for x in manifest["checks"]})
        script = (ROOT / "tools/compile_release_report.py").read_text()
        self.assertIn("EVIDENCE_INCOMPLETE", script)
        self.assertIn("SCHEMA_VALID", script)
        self.assertIn("NOT_RUN", script)

    def test_github_workflow_templates_parse_as_yaml(self):
        paths = [
            ".github/workflows/seo-audit-tests.yml",
            "templates/github-actions/website-quality.yml",
            "templates/github-actions/website-post-deploy.yml",
            "templates/github-actions/website-browser-quality.yml",
        ]
        for relative in paths:
            with self.subTest(path=relative):
                document = yaml.safe_load((ROOT / relative).read_text())
                self.assertIsInstance(document, dict)
                self.assertIn("jobs", document)
                self.assertTrue("on" in document or True in document)

    def test_export_paths_are_relative_to_export_output_directory(self):
        manifest = json.loads((ROOT / "templates/exports/export-manifest.example.json").read_text())
        for item in manifest["exports"]:
            self.assertFalse(item["path"].startswith("exports/"))


if __name__ == "__main__":
    unittest.main()
