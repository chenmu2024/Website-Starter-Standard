#!/usr/bin/env python3
"""Legacy entrypoint for the single canonical offline SEO audit.

Keep existing import/CLI callers working; no duplicate scanning logic lives here.
New integrations should use tools/seo_audit.py directly.
"""
import argparse
import importlib.util
import json
from pathlib import Path

_CANONICAL = Path(__file__).resolve().parents[1] / "tools" / "seo_audit.py"
_spec = importlib.util.spec_from_file_location("website_standard_seo_audit", _CANONICAL)
_engine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_engine)

_LEGACY_NAMES = {
    "TITLE_MISSING": "MISSING_TITLE",
    "ORPHAN_PAGE": "ORPHAN_HTML_PAGE",
    "IMG_ALT_MISSING": "IMAGE_ALT_MISSING",
    "JSON_LD_INVALID": "INVALID_JSONLD",
    "CANONICAL_SHARED": "SHARED_CANONICAL",
    "EXTERNAL_CANONICAL": "CANONICAL_EXTERNAL",
    "CANONICAL_NOT_ABSOLUTE": "CANONICAL_NOT_ABSOLUTE",
    "NOINDEX": "NOINDEX_META",
}


def audit(root, base):
    """Return the legacy report shape while delegating all checks to one engine."""
    report = _engine.audit(Path(root), base)
    findings = [
        {
            "severity": f["severity"],
            "code": _LEGACY_NAMES.get(f["code"], f["code"]),
            "url": f["page"],
            "detail": f["message"],
        }
        for f in report["findings"]
    ]
    return {
        "scope": report["scope"],
        "base_url": report["base_url"],
        "scanned": report["pages_scanned"],
        "summary": report["summary"],
        "findings": findings,
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--site-dir", required=True, type=Path)
    cli.add_argument("--base-url", required=True)
    cli.add_argument("--output", type=Path)
    cli.add_argument("--fail-on", choices=("never", "error", "warning"), default="error")
    args = cli.parse_args()
    if not args.site_dir.is_dir():
        cli.error("--site-dir must be a directory")
    from urllib.parse import urlparse
    parsed = urlparse(args.base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.path not in ("", "/"):
        cli.error("--base-url must be an HTTP(S) origin without a path")
    report = audit(args.site_dir, args.base_url)
    data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf8")
    else:
        print(data, end="")
    summary = report["summary"]
    fail = (args.fail_on == "error" and summary["error"] > 0 or
            args.fail_on == "warning" and summary["error"] + summary["warning"] > 0)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
