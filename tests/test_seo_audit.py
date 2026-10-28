"""Standard-library tests: python -m unittest discover -s tests -v"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "seo_audit.py"
spec = importlib.util.spec_from_file_location("seo_audit", SCRIPT)
audit_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_tool)


def page(title="Example", canon="https://example.org/", body="", extra_head=""):
    return (f'<!doctype html><html lang="en"><head><title>{title}</title>'
            f'<meta name="description" content="Useful example">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<link rel="canonical" href="{canon}">{extra_head}</head>'
            f'<body><h1>{title}</h1>{body}</body></html>')


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, text):
        f = self.root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf8")

    def codes(self, report):
        return [item["code"] for item in report["findings"]]

    def test_good_site_with_relative_parent_link_assets_and_sitemap(self):
        self.write("index.html", page(body='<a href="/tools/">Tools</a><img src="/logo.svg" alt="Logo">'))
        self.write("tools/index.html", page("Tools", "https://example.org/tools/", body='<a href="../">Home</a><link rel="stylesheet" href="/main.css">'))
        self.write("logo.svg", "<svg></svg>")
        self.write("main.css", "body{}")
        self.write("robots.txt", "User-agent: *\nAllow: /")
        self.write("sitemap.xml", '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.org/</loc></url><url><loc>https://example.org/tools/</loc></url></urlset>')
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertEqual(report["pages_scanned"], 2)
        self.assertEqual(report["summary"], {"error": 0, "warning": 0, "info": 0}, report["findings"])

    def test_bad_and_orphan_site(self):
        self.write("index.html", '<html><head><link rel="canonical" href="https://example.org/"><script type="application/ld+json">{BAD</script></head><body><a href="/missing/">Bad</a><img src="/absent.png"></body></html>')
        self.write("other/index.html", page("Unused", "https://example.org/", extra_head='<meta name="robots" content="noindex">'))
        report = audit_tool.audit(self.root, "https://example.org")
        codes = self.codes(report)
        for required in ("TITLE_MISSING", "JSON_LD_INVALID", "BROKEN_INTERNAL_LINK", "MISSING_LOCAL_ASSET", "ORPHAN_PAGE", "CANONICAL_SHARED", "CANONICAL_NONSELF", "NOINDEX"):
            self.assertIn(required, codes)

    def test_sitemap_parse_and_external_canonical(self):
        self.write("index.html", page(canon="https://another.example/"))
        self.write("sitemap.xml", "<notwellformed")
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("SITEMAP_XML_INVALID", self.codes(report))
        self.assertIn("EXTERNAL_CANONICAL", self.codes(report))

    def test_cli_exit_and_json_output(self):
        self.write("index.html", '<html lang="en"><body><h1>Hello</h1></body></html>')
        output = self.root / "result.json"
        args = [sys.executable, str(SCRIPT), "--site-dir", str(self.root), "--base-url", "https://example.org", "--output", str(output), "--fail-on", "error"]
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertGreater(json.loads(output.read_text())["summary"]["error"], 0)
        result2 = subprocess.run(args[:-1] + ["never"], capture_output=True, text=True)
        self.assertEqual(result2.returncode, 0)

    def test_empty_site_is_error(self):
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("NO_HTML", self.codes(report))


if __name__ == "__main__":
    unittest.main()
