"""Deterministic offline sanity checks for seo_static_audit (Python stdlib)."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from seo_static_audit import audit


class AuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def page(self, name, body, title="Example"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            '<html lang="en"><head><title>' + title + '</title>'
            '<meta name="description" content="Useful tool">'
            '<meta name="viewport" content="width=device-width">'
            '<link rel="canonical" href="https://example.com/' + ("" if name == "index.html" else name.replace("index.html", "")) + '">'
            '</head><body><h1>Tool</h1>' + body + "</body></html>", encoding="utf-8"
        )

    def test_valid_internal_navigation(self):
        self.page("index.html", '<a href="/tool/">Tool</a>')
        self.page("tool/index.html", '<a href="/">Home</a>')
        result = audit(self.root, "https://example.com")
        self.assertEqual(result["summary"]["error"], 0)
        self.assertNotIn("BROKEN_INTERNAL_LINK", [x["code"] for x in result["findings"]])
        self.assertNotIn("ORPHAN_HTML_PAGE", [x["code"] for x in result["findings"]])

    def test_broken_link_and_missing_title(self):
        self.page("index.html", '<a href="/missing/">Missing</a>', title="")
        result = audit(self.root, "https://example.com")
        codes = [x["code"] for x in result["findings"]]
        self.assertIn("BROKEN_INTERNAL_LINK", codes)
        self.assertIn("MISSING_TITLE", codes)

    def test_no_files(self):
        result = audit(self.root, "https://example.com")
        self.assertIn("NO_HTML", [x["code"] for x in result["findings"]])


if __name__ == "__main__":
    unittest.main()
