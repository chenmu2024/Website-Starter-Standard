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


def page(title="Example", canon="https://example.org/", body="", extra_head="", lang="en"):
    return (f'<!doctype html><html lang="{lang}"><head><title>{title}</title>'
            f'<meta name="description" content="Useful {title} example">'
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

    def test_duplicate_descriptions_are_review_flags_not_fake_length_rules(self):
        self.write("index.html", page(title="Home"))
        self.write("tools/index.html",
                   page("Tools", "https://example.org/tools/",
                        body='<a href="/">Home</a>').replace(
                            'content="Useful Tools example"', 'content="Useful Home example"'))
        self.write("index.html", page(title="Home", body='<a href="/tools/">Tools</a>'))
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("DUPLICATE_DESCRIPTION", self.codes(report))

    def test_preview_contract_requires_noindex_on_every_built_html(self):
        self.write("index.html", page())
        policy = {"mode": "preview", "required_routes": ["/"]}
        self.assertIn("PREVIEW_INDEXABLE",
                      self.codes(audit_tool.audit(self.root, "https://example.org", policy)))
        self.write("index.html", page(extra_head='<meta name="robots" content="noindex,nofollow">'))
        report = audit_tool.audit(self.root, "https://example.org", policy)
        self.assertNotIn("PREVIEW_INDEXABLE", self.codes(report))

    def test_production_contract_checks_route_noindex_canonical_and_sitemap(self):
        self.write("index.html", page(extra_head='<meta name="robots" content="noindex">'))
        self.write("sitemap.xml", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>')
        policy = {"mode": "production", "required_routes": ["/", "/not-built/"],
                  "indexable_routes": ["/"]}
        findings = self.codes(audit_tool.audit(self.root, "https://example.org", policy))
        self.assertIn("REQUIRED_ROUTE_MISSING", findings)
        self.assertIn("INDEXABLE_NOINDEX", findings)
        self.assertIn("INDEXABLE_SITEMAP", findings)
        self.write("index.html", page())
        self.write("sitemap.xml", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.org/</loc></url></urlset>')
        report = audit_tool.audit(self.root, "https://example.org",
                                  {"mode": "production", "indexable_routes": ["/"]})
        self.assertEqual(report["summary"]["error"], 0, report["findings"])

    def test_production_policy_must_explicitly_list_indexable_routes(self):
        self.write("index.html", page())
        with self.assertRaises(ValueError):
            audit_tool.audit(self.root, "https://example.org", {"mode": "production"})

    def test_production_policy_accepts_local_sitemap_index_children(self):
        self.write("index.html", page(body='<a href="/tools/">Tools</a>'))
        self.write("tools/index.html", page("Tools", "https://example.org/tools/",
                                            body='<a href="/">Home</a>'))
        self.write("sitemap.xml",
                   '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                   '<sitemap><loc>https://example.org/maps/content.xml</loc></sitemap></sitemapindex>')
        self.write("maps/content.xml",
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                   '<url><loc>https://example.org/</loc></url>'
                   '<url><loc>https://example.org/tools/</loc></url></urlset>')
        policy = {"mode": "production",
                  "required_routes": ["/", "/tools/"],
                  "indexable_routes": ["/", "/tools/"]}
        result = audit_tool.audit(self.root, "https://example.org", policy)
        self.assertNotIn("INDEXABLE_SITEMAP", self.codes(result), result["findings"])
        self.assertEqual(result["summary"]["error"], 0, result["findings"])

    def test_missing_sitemap_index_child_is_not_a_false_pass(self):
        self.write("index.html", page())
        self.write("sitemap.xml",
                   '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                   '<sitemap><loc>https://example.org/not-present.xml</loc></sitemap></sitemapindex>')
        report = audit_tool.audit(self.root, "https://example.org",
                                  {"mode": "production", "indexable_routes": ["/"]})
        self.assertIn("SITEMAP_INDEX_CHILD_MISSING", self.codes(report))
        self.assertIn("INDEXABLE_SITEMAP", self.codes(report))

    def test_hreflang_valid_self_and_return_links_pass_explicit_group(self):
        es_tags = ('<link rel="alternate" hreflang="es-ES" href="https://example.org/es/">'
                   '<link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/">'
                   '<link rel="alternate" hreflang="x-default" href="https://example.org/es/">')
        pt_tags = ('<link rel="alternate" hreflang="es-ES" href="https://example.org/es/">'
                   '<link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/">'
                   '<link rel="alternate" hreflang="x-default" href="https://example.org/es/">')
        self.write("es/index.html", page("Español", "https://example.org/es/",
                                         extra_head=es_tags, lang="es-ES"))
        self.write("pt/index.html", page("Português", "https://example.org/pt/",
                                         extra_head=pt_tags, lang="pt-BR"))
        self.write("sitemap.xml",
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                   '<url><loc>https://example.org/es/</loc></url>'
                   '<url><loc>https://example.org/pt/</loc></url></urlset>')
        policy = {"mode": "production", "indexable_routes": ["/es/", "/pt/"],
                  "hreflang_groups": [{"routes": {
                      "es-ES": "/es/", "pt-BR": "/pt/", "x-default": "/es/"}}]}
        report = audit_tool.audit(self.root, "https://example.org", policy)
        self.assertNotIn("HREFLANG_GROUP_INCOMPLETE", self.codes(report), report["findings"])
        self.assertNotIn("HREFLANG_RETURN_MISSING", self.codes(report), report["findings"])

    def test_hreflang_group_missing_variant_and_return_is_reported(self):
        es_tags = ('<link rel="alternate" hreflang="es-ES" href="https://example.org/es/">'
                   '<link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/">')
        pt_tags = '<link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/">'
        self.write("es/index.html", page("Español", "https://example.org/es/", extra_head=es_tags))
        self.write("pt/index.html", page("Português", "https://example.org/pt/", extra_head=pt_tags))
        policy = {"mode": "production", "indexable_routes": ["/es/", "/pt/"],
                  "hreflang_groups": [{"routes": {"es-ES": "/es/", "pt-BR": "/pt/"}}]}
        report = audit_tool.audit(self.root, "https://example.org", policy)
        self.assertIn("HREFLANG_GROUP_INCOMPLETE", self.codes(report))
        self.assertIn("HREFLANG_RETURN_MISSING", self.codes(report))

    def test_hreflang_invalid_duplicate_code_and_missing_target_are_reported(self):
        tags = ('<link rel="alternate" hreflang="bad_code" href="https://example.org/">'
                '<link rel="alternate" hreflang="es" href="https://example.org/missing/">'
                '<link rel="alternate" hreflang="es" href="https://example.org/">')
        self.write("index.html", page(extra_head=tags))
        report = audit_tool.audit(self.root, "https://example.org")
        codes = self.codes(report)
        self.assertIn("HREFLANG_CODE_INVALID", codes)
        self.assertIn("HREFLANG_DUPLICATE_CODE", codes)
        self.assertIn("HREFLANG_TARGET_MISSING", codes)

    def test_hreflang_external_alternate_is_explicitly_unverified(self):
        tags = ('<link rel="alternate" hreflang="es" href="https://example.org/">'
                '<link rel="alternate" hreflang="pt-BR" href="https://example.com.br/">')
        self.write("index.html", page(extra_head=tags))
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("HREFLANG_EXTERNAL_UNVERIFIED", self.codes(report))

    def test_hreflang_accepts_script_and_numeric_region_subtags(self):
        tags = ('<link rel="alternate" hreflang="zh-Hans" href="https://example.org/">'
                '<link rel="alternate" hreflang="es-419" href="https://example.org/">')
        self.write("index.html", page(extra_head=tags, lang="zh-Hans"))
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertNotIn("HREFLANG_CODE_INVALID", self.codes(report))


    def test_sitemap_hreflang_group_passes_without_html_alternate_tags(self):
        self.write("es/index.html", page("Español", "https://example.org/es/", lang="es-ES"))
        self.write("pt/index.html", page("Português", "https://example.org/pt/", lang="pt-BR"))
        sitemap = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                   'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
                   '<url><loc>https://example.org/es/</loc>'
                   '<xhtml:link rel="alternate" hreflang="es-ES" href="https://example.org/es/"/>'
                   '<xhtml:link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/"/>'
                   '</url>'
                   '<url><loc>https://example.org/pt/</loc>'
                   '<xhtml:link rel="alternate" hreflang="es-ES" href="https://example.org/es/"/>'
                   '<xhtml:link rel="alternate" hreflang="pt-BR" href="https://example.org/pt/"/>'
                   '</url></urlset>')
        self.write("sitemap.xml", sitemap)
        policy = {"mode": "production", "indexable_routes": ["/es/", "/pt/"],
                  "hreflang_groups": [{"routes": {"es-ES": "/es/", "pt-BR": "/pt/"}}]}
        report = audit_tool.audit(self.root, "https://example.org", policy)
        self.assertNotIn("HREFLANG_GROUP_INCOMPLETE", self.codes(report), report["findings"])
        self.assertNotIn("HREFLANG_RETURN_MISSING", self.codes(report), report["findings"])

    def test_html_and_sitemap_hreflang_mismatch_is_reported(self):
        html_tags = ('<link rel="alternate" hreflang="es" href="https://example.org/">'
                     '<link rel="alternate" hreflang="pt" href="https://example.org/pt/">')
        self.write("index.html", page(extra_head=html_tags))
        sitemap = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                   'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
                   '<url><loc>https://example.org/</loc>'
                   '<xhtml:link rel="alternate" hreflang="es" href="https://example.org/"/>'
                   '</url></urlset>')
        self.write("sitemap.xml", sitemap)
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("HREFLANG_SOURCE_MISMATCH", self.codes(report))

    def test_malformed_sitemap_hreflang_entry_is_not_silently_ignored(self):
        self.write("index.html", page())
        sitemap = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                   'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
                   '<url><loc>https://example.org/</loc>'
                   '<xhtml:link rel="alternate" hreflang="es"/>'
                   '</url></urlset>')
        self.write("sitemap.xml", sitemap)
        report = audit_tool.audit(self.root, "https://example.org")
        self.assertIn("SITEMAP_HREFLANG_INVALID_ENTRY", self.codes(report))


    def test_hreflang_source_mismatch_blocks_explicit_production_policy(self):
        tags = ('<link rel="alternate" hreflang="en" href="https://example.org/">'
                '<link rel="alternate" hreflang="es" href="https://example.org/es/">'
                '<link rel="alternate" hreflang="pt" href="https://example.org/pt/">')
        self.write("index.html", page("Home", "https://example.org/", extra_head=tags, lang="en"))
        self.write("es/index.html", page("Español", "https://example.org/es/", extra_head=tags, lang="es"))
        self.write("pt/index.html", page("Português", "https://example.org/pt/", extra_head=tags, lang="pt"))
        sitemap = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                   'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
                   '<url><loc>https://example.org/</loc>'
                   '<xhtml:link rel="alternate" hreflang="en" href="https://example.org/"/>'
                   '</url></urlset>')
        self.write("sitemap.xml", sitemap)
        report = audit_tool.audit(self.root, "https://example.org",
                                  {"mode": "production", "indexable_routes": ["/"]})
        finding = next(x for x in report["findings"] if x["code"] == "HREFLANG_SOURCE_MISMATCH")
        self.assertEqual(finding["severity"], "error")



if __name__ == "__main__":
    unittest.main()
