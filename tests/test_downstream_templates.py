"""Guard against accidentally turning downstream quality templates into no-op jobs."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DownstreamTemplateTests(unittest.TestCase):
    def test_ci_has_explicit_required_commands_and_real_outputs(self):
        template = (ROOT / "templates" / "github-actions" / "website-quality.yml").read_text()
        for marker in ("BUILD_COMMAND: REPLACE_ME", "CORE_TEST_COMMAND: REPLACE_ME",
                       "BROWSER_TEST_COMMAND: REPLACE_ME", "CALC_RUNTIME_COMMAND: REPLACE_ME",
                       "tools/seo_audit.py", "--policy-json",
                       "tools/validate_calculation_cases.py", "--observed",
                       "release-evidence/", "if: always()", "test -d"):
            self.assertIn(marker, template)
        self.assertIn("SITE_DIR: dist", template)
        self.assertIn("test -f release-evidence/calculation-observed.json", template)

    def test_post_deploy_workflow_requires_actual_commit_and_url(self):
        template = (ROOT / "templates" / "github-actions" /
                    "website-post-deploy.yml").read_text()
        self.assertIn("workflow_dispatch:", template)
        self.assertIn("expected_sha:", template)
        self.assertIn("--expected-sha", template)
        self.assertIn("tools/verify_deployment.py", template)
        self.assertNotIn("wrangler pages deploy", template)

    def test_indexation_examples_are_explicit_not_all_pages_by_default(self):
        preview = json.loads((ROOT / "templates/indexation-policy.preview.json").read_text())
        production = json.loads((ROOT / "templates/indexation-policy.production.json").read_text())
        self.assertEqual(preview["mode"], "preview")
        self.assertEqual(preview["preview_noindex_via"], "header")
        self.assertEqual(production["mode"], "production")
        self.assertEqual(production["indexable_routes"], ["/"])

    def test_calculator_example_has_three_required_classes(self):
        catalog = json.loads((ROOT / "templates/calculations/cases.example.json").read_text())
        self.assertEqual({x["kind"] for x in catalog["cases"]},
                         {"normal", "boundary", "invalid"})


if __name__ == "__main__":
    unittest.main()
