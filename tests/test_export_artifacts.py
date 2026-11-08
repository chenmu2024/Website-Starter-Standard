"""Tests for real CSV/PDF/SVG export artifact validation."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "validate_export_artifacts.py"
spec = importlib.util.spec_from_file_location("export_artifact_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def minimal_pdf(text="Cut list", width=612, height=792):
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>".encode(),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode())
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects)+1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(output)


class ExportArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "result.csv").write_text(
            "Dimension,Value,Unit\nLength,304.8,mm\n", encoding="utf-8")
        (self.root / "report.pdf").write_bytes(minimal_pdf())
        (self.root / "diagram.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400"><rect width="800" height="400"/></svg>',
            encoding="utf8")

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self):
        return {"version": 1, "exports": [
            {"id": "cut-list-csv", "kind": "csv", "path": "result.csv",
             "expected_headers": ["Dimension", "Value", "Unit"],
             "expected_rows": [{"Dimension": "Length", "Value": 304.8, "Unit": "mm"}],
             "numeric_tolerance": {"Value": 0.001}},
            {"id": "summary-pdf", "kind": "pdf", "path": "report.pdf",
             "expected_page_count": 1, "expected_text_contains": ["Cut list"],
             "expected_page_size_pt": [612, 792]},
            {"id": "diagram-svg", "kind": "svg", "path": "diagram.svg",
             "expected_viewbox": "0 0 800 400", "expected_width": "800", "expected_height": "400"}
        ]}

    def test_csv_pdf_svg_artifacts_match_reviewed_expectations(self):
        report = validator.validate(self.manifest(), self.root)
        self.assertEqual(report["status"], "PASS", report["errors"])
        self.assertEqual(report["exports_checked"], 3)

    def test_csv_numeric_drift_and_ragged_rows_fail(self):
        (self.root / "result.csv").write_text(
            "Dimension,Value,Unit\nLength,300,mm\n", encoding="utf8")
        report = validator.validate(self.manifest(), self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("row[0].Value", report["errors"][0])
        (self.root / "result.csv").write_text(
            "Dimension,Value,Unit\nLength,304.8\n", encoding="utf8")
        report = validator.validate(self.manifest(), self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("different number of cells", report["errors"][0])

    def test_pdf_missing_expected_text_or_wrong_print_page_size_fails(self):
        manifest = self.manifest()
        manifest["exports"][1]["expected_text_contains"] = ["Nonexistent label"]
        report = validator.validate(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("missing expected extracted text", report["errors"][0])
        (self.root / "report.pdf").write_bytes(minimal_pdf(width=595, height=842))
        manifest = self.manifest()
        report = validator.validate(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("page 1 width", report["errors"][0])

    def test_svg_geometry_and_path_traversal_fail_closed(self):
        manifest = self.manifest()
        manifest["exports"][2]["expected_viewbox"] = "0 0 100 100"
        report = validator.validate(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("viewBox", report["errors"][0])
        manifest = {"version": 1, "exports": [
            {"id": "escape", "kind": "svg", "path": "../outside.svg",
             "expected_viewbox": "0 0 1 1"}]}
        report = validator.validate(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("escapes output directory", report["errors"][0])

    def test_duplicate_ids_and_unsupported_exports_fail(self):
        manifest = {"version": 1, "exports": [
            {"id": "same", "kind": "csv", "path": "result.csv",
             "expected_headers": ["Dimension", "Value", "Unit"], "expected_rows": [
                 {"Dimension": "Length", "Value": 304.8, "Unit": "mm"}]},
            {"id": "same", "kind": "xlsx", "path": "report.xlsx"}]}
        report = validator.validate(manifest, self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("unique", report["errors"][0])


if __name__ == "__main__":
    unittest.main()
