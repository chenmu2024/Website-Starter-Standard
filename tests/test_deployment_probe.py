"""Read-only deployment probe contract tests; no external HTTP calls."""
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "verify_deployment.py"
spec = importlib.util.spec_from_file_location("release_http_probe", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

PROD = "https://example.org"
PREVIEW = "https://preview.pages.dev"


def fake_response(url, status, text, headers=None):
    return {"status": status, "url": url, "headers": headers or {},
            "body": text.encode("utf8")}


def responses(preview_noindex=True, sha="abc123", prod_noindex=False):
    header = ('<meta name="robots" content="noindex">' if prod_noindex else "")
    mapping = {
        PROD + "/": fake_response(PROD + "/", 200,
            '<!doctype html><html><head><title>Tool</title>' + header +
            '<link rel="canonical" href="https://example.org/"></head><body>Tool</body></html>'),
        PROD + "/robots.txt": fake_response(PROD + "/robots.txt", 200, "User-agent: *\nAllow: /"),
        PROD + "/sitemap.xml": fake_response(PROD + "/sitemap.xml", 200,
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.org/</loc></url><url><loc>https://example.org/tool/</loc></url></urlset>'),
        PROD + "/tool/": fake_response(PROD + "/tool/", 200,
            '<html><head><link rel="canonical" href="https://example.org/tool/"></head></html>'),
        PROD + "/__website-standard-release-probe-missing-404__":
            fake_response(PROD + "/__website-standard-release-probe-missing-404__", 404, ""),
        PROD + "/build-info.json": fake_response(PROD + "/build-info.json", 200,
                                                  json.dumps({"commit": sha})),
        PREVIEW + "/": fake_response(PREVIEW + "/", 200, "<html><head><title>Preview</title></head></html>",
                                     {"x-robots-tag": "noindex,nofollow"} if preview_noindex else {})
    }
    return mapping


class DeploymentProbeTests(unittest.TestCase):
    def test_actual_http_and_deployed_commit_pass(self):
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: responses()[url]):
            report = probe.inspect(PROD, routes=["/tool/"], preview_url=PREVIEW,
                                   expected_sha="abc123")
        self.assertEqual(report["status"], "PASS", report["checks"])
        self.assertEqual(report["errors"], [])

    def test_preview_without_noindex_blocks(self):
        with patch.object(probe, "fetch",
                          side_effect=lambda url, timeout: responses(preview_noindex=False)[url]):
            report = probe.inspect(PROD, preview_url=PREVIEW, expected_sha="abc123")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("preview-noindex" in x for x in report["errors"]))

    def test_stale_commit_and_production_noindex_block(self):
        with patch.object(probe, "fetch",
                          side_effect=lambda url, timeout: responses(sha="old", prod_noindex=True)[url]):
            report = probe.inspect(PROD, expected_sha="abc123")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("deployed-commit" in x for x in report["errors"]))
        self.assertTrue(any("production-indexable" in x for x in report["errors"]))

    def test_no_commit_evidence_is_partial_not_pass(self):
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: responses()[url]):
            report = probe.inspect(PROD)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertTrue(any(x["name"] == "deployed-commit" and x["status"] == "NOT_RUN"
                            for x in report["checks"]))

    def test_sitemap_bad_xml_blocks(self):
        mapping = responses()
        mapping[PROD + "/sitemap.xml"] = fake_response(PROD + "/sitemap.xml", 200, "<broken")
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: mapping[url]):
            report = probe.inspect(PROD, expected_sha="abc123")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("sitemap-xml" in x for x in report["errors"]))

    def test_empty_sitemap_or_global_robots_disallow_blocks_release(self):
        mapping = responses()
        mapping[PROD + "/sitemap.xml"] = fake_response(PROD + "/sitemap.xml", 200,
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>')
        mapping[PROD + "/robots.txt"] = fake_response(PROD + "/robots.txt", 200,
            "User-agent: *\nDisallow: /")
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: mapping[url]):
            report = probe.inspect(PROD, expected_sha="abc123")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("sitemap-coverage" in x for x in report["errors"]))
        self.assertTrue(any("robots-global-indexing" in x for x in report["errors"]))

    def test_case_insensitive_production_x_robots_tag_blocks(self):
        mapping = responses()
        mapping[PROD + "/"]["headers"] = {"x-robots-tag": "noindex,nofollow"}
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: mapping[url]):
            report = probe.inspect(PROD, expected_sha="abc123")
        self.assertTrue(any("production-indexable" in x for x in report["errors"]))

    def test_critical_page_canonical_and_noindex_are_verified(self):
        mapping = responses()
        mapping[PROD + "/tool/"] = fake_response(PROD + "/tool/", 200,
            '<html><head><meta name="robots" content="noindex">'
            '<link rel="canonical" href="https://example.org/wrong/"></head></html>')
        with patch.object(probe, "fetch", side_effect=lambda url, timeout: mapping[url]):
            report = probe.inspect(PROD, routes=["/tool/"], expected_sha="abc123")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("canonical:/tool/" in x for x in report["errors"]))
        self.assertTrue(any("indexable:/tool/" in x for x in report["errors"]))


if __name__ == "__main__":
    unittest.main()
