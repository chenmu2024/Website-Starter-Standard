#!/usr/bin/env python3
"""Validate generated CSV/PDF/SVG exports against reviewed expected artifacts.

This validates files emitted by the real downstream application. It does not
recalculate the product formula or certify physical printer output.
PDF checks require the optional pypdf dependency (see requirements-qa.txt).
"""
import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from pathlib import Path


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{label}: expected numeric scalar")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label}: invalid decimal {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{label}: NaN/Infinity is forbidden")
    return result


def safe_file(root, relative):
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("Export path must be a nonempty relative path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path == root.resolve():
        raise ValueError(f"Export path escapes output directory: {relative!r}")
    if not path.is_file():
        raise ValueError(f"Export file missing: {relative}")
    if path.stat().st_size > 50 * 1024 * 1024:
        raise ValueError(f"Export exceeds 50 MiB safety limit: {relative}")
    return path


def compare_value(actual, expected, tolerance, label):
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        difference = abs(number(actual, label) - number(expected, label))
        allowed = number(tolerance, label + " tolerance")
        if allowed < 0:
            raise ValueError(f"{label}: tolerance must be nonnegative")
        if difference > allowed:
            raise ValueError(f"{label}: observed {actual!r}, expected {expected!r}, tolerance {allowed}")
    elif isinstance(expected, bool):
        normalized = str(actual).strip().casefold()
        if normalized not in {"true", "false", "1", "0", "yes", "no"}:
            raise ValueError(f"{label}: observed value is not a recognizable boolean: {actual!r}")
        observed = normalized in {"true", "1", "yes"}
        if observed is not expected:
            raise ValueError(f"{label}: observed {observed!r}, expected {expected!r}")
    elif str(actual) != str(expected):
        raise ValueError(f"{label}: observed {actual!r}, expected {expected!r}")


def validate_csv(path, spec):
    encoding = spec.get("encoding", "utf-8-sig")
    delimiter = spec.get("delimiter", ",")
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise ValueError("CSV delimiter must be exactly one character")
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        headers = reader.fieldnames
        if not headers or any(not h for h in headers):
            raise ValueError("CSV header row is empty or contains empty column names")
        if len(headers) != len(set(headers)):
            raise ValueError("CSV has duplicate column names")
        expected_headers = spec.get("expected_headers")
        if not isinstance(expected_headers, list) or not expected_headers:
            raise ValueError("CSV manifest requires nonempty expected_headers")
        if headers != expected_headers:
            raise ValueError(f"CSV headers differ: observed={headers!r}, expected={expected_headers!r}")
        rows = list(reader)
    expected_rows = spec.get("expected_rows")
    if not isinstance(expected_rows, list):
        raise ValueError("CSV manifest requires expected_rows list (use [] for an intentionally header-only export)")
    if len(rows) != len(expected_rows):
        raise ValueError(f"CSV row count differs: observed={len(rows)}, expected={len(expected_rows)}")
    for row_index, row in enumerate(rows):
        if None in row or any(row.get(header) is None for header in headers):
            raise ValueError(f"CSV row[{row_index}] has a different number of cells than the header")
    tolerances = spec.get("numeric_tolerance", {})
    if not isinstance(tolerances, dict):
        raise ValueError("numeric_tolerance must be an object")
    for row_index, (observed, expected) in enumerate(zip(rows, expected_rows)):
        if not isinstance(expected, dict) or set(expected) != set(headers):
            raise ValueError(f"CSV expected_rows[{row_index}] must specify exactly every header")
        for field, value in expected.items():
            compare_value(observed[field], value, tolerances.get(field, 0),
                          f"row[{row_index}].{field}")
    return {"kind": "csv", "rows": len(rows), "headers": headers}


def validate_pdf(path, spec):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError("PDF verification requires pypdf; install requirements-qa.txt") from exc
    reader = PdfReader(str(path), strict=True)
    if reader.is_encrypted:
        raise ValueError("PDF is encrypted and cannot be inspected")
    expected_pages = spec.get("expected_page_count")
    if not isinstance(expected_pages, int) or isinstance(expected_pages, bool) or expected_pages < 1:
        raise ValueError("PDF manifest requires positive expected_page_count")
    if len(reader.pages) != expected_pages:
        raise ValueError(f"PDF page count observed={len(reader.pages)}, expected={expected_pages}")
    expected_text = spec.get("expected_text_contains")
    if not isinstance(expected_text, list) or not expected_text or any(not isinstance(x, str) or not x.strip() for x in expected_text):
        raise ValueError("PDF manifest requires nonempty expected_text_contains")
    extracted = " ".join((page.extract_text() or "") for page in reader.pages)
    normalized = " ".join(extracted.split()).casefold()
    missing = [term for term in expected_text if " ".join(term.split()).casefold() not in normalized]
    if missing:
        raise ValueError(f"PDF is missing expected extracted text: {missing}")
    expected_size = spec.get("expected_page_size_pt")
    sizes = []
    if expected_size is not None:
        if (not isinstance(expected_size, list) or len(expected_size) != 2):
            raise ValueError("expected_page_size_pt must be [width, height]")
        tolerance = number(spec.get("page_size_tolerance_pt", 1), "page size tolerance")
        if tolerance < 0:
            raise ValueError("page_size_tolerance_pt must be nonnegative")
        for index, page in enumerate(reader.pages):
            actual = [Decimal(str(float(page.mediabox.width))),
                      Decimal(str(float(page.mediabox.height)))]
            for axis, observed, expected in zip(("width", "height"), actual, expected_size):
                if abs(observed - number(expected, axis)) > tolerance:
                    raise ValueError(f"PDF page {index + 1} {axis}={observed}pt, expected {expected}pt ±{tolerance}")
            sizes.append([float(actual[0]), float(actual[1])])
    return {"kind": "pdf", "pages": len(reader.pages), "page_sizes_pt": sizes,
            "text_characters": len(extracted)}


def validate_svg(path, spec):
    root = ET.parse(path).getroot()
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        raise ValueError("SVG root element is not <svg>")
    expected = {"viewBox": spec.get("expected_viewbox"),
                "width": spec.get("expected_width"),
                "height": spec.get("expected_height")}
    checks = {key: value for key, value in expected.items() if value is not None}
    if not checks:
        raise ValueError("SVG manifest must specify expected_viewbox, expected_width or expected_height")
    for key, value in checks.items():
        if root.attrib.get(key) != str(value):
            raise ValueError(f"SVG {key} observed={root.attrib.get(key)!r}, expected={value!r}")
    return {"kind": "svg", "attributes": root.attrib, "elements": sum(1 for _ in root.iter())}


def validate(manifest, output_root):
    issues = []
    results = []
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        return {"status": "FAIL", "exports_checked": 0, "results": [],
                "errors": ["Manifest must be an object with version=1"]}
    exports = manifest.get("exports")
    if not isinstance(exports, list) or not exports:
        return {"status": "FAIL", "exports_checked": 0, "results": [],
                "errors": ["Manifest requires a nonempty exports list"]}
    ids = set()
    root = Path(output_root).resolve()
    for index, spec in enumerate(exports):
        label = f"exports[{index}]"
        try:
            if not isinstance(spec, dict):
                raise ValueError("export entry must be an object")
            key = spec.get("id")
            if not isinstance(key, str) or not key.strip() or key in ids:
                raise ValueError("export id must be unique and nonempty")
            ids.add(key)
            label = key
            path = safe_file(root, spec.get("path"))
            kind = spec.get("kind")
            if kind == "csv":
                detail = validate_csv(path, spec)
            elif kind == "pdf":
                detail = validate_pdf(path, spec)
            elif kind == "svg":
                detail = validate_svg(path, spec)
            else:
                raise ValueError(f"unsupported export kind: {kind!r}")
            results.append({"id": key, "status": "PASS", "path": spec["path"], **detail})
        except Exception as exc:
            issues.append(f"{label}: {exc}")
            results.append({"id": spec.get("id") if isinstance(spec, dict) else label,
                            "status": "FAIL", "error": str(exc)})
    return {"status": "FAIL" if issues else "PASS", "exports_checked": len(results),
            "results": results, "errors": issues,
            "scope": "Generated artifact content/structure only; physical printer output is not verified"}


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--manifest", required=True, type=Path)
    cli.add_argument("--output-dir", required=True, type=Path)
    cli.add_argument("--output", type=Path)
    args = cli.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf8"))
        report = validate(manifest, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {"status": "FAIL", "exports_checked": 0, "results": [],
                  "errors": [str(exc)]}
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf8")
    else:
        print(payload, end="")
    print(f"Export artifact gate: {report['status']}", file=sys.stderr)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
