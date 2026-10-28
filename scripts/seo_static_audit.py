#!/usr/bin/env python3
"""Offline HTML SEO sanity audit (standard library only; no network/API).

python scripts/seo_static_audit.py --site-dir dist --base-url https://example.com --output report.json
This is NOT a live crawl, JavaScript-rendered inspection, CWV test or Google indexing check.
"""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = []
        self.h1 = 0
        self.desc = []
        self.canonical = []
        self.robots = []
        self.links = []
        self.images = []
        self.viewport = False
        self.jsonld = []
        self._title = False
        self._ld = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "title":
            self._title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical.append(a.get("href", ""))
        if tag == "meta":
            key = a.get("name", "").lower()
            if key == "description":
                self.desc.append(a.get("content", ""))
            if key == "robots":
                self.robots.append(a.get("content", ""))
            if key == "viewport":
                self.viewport = True
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._ld = []

    def handle_data(self, data):
        if self._title:
            self.title.append(data)
        if self._ld is not None:
            self._ld.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        if tag == "script" and self._ld is not None:
            self.jsonld.append("".join(self._ld))
            self._ld = None


def route(path, root):
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[:-len("index.html")]
    return "/" + relative


def audit(root, base):
    root = Path(root).resolve()
    files = sorted(root.rglob("*.html"))
    urls = {route(f, root): f for f in files}
    inbound = {url: 0 for url in urls}
    findings = []
    canonical_owners = {}

    def flag(severity, code, url, detail):
        findings.append({"severity": severity, "code": code, "url": url, "detail": detail})

    if not files:
        flag("error", "NO_HTML", "/", "No *.html found under build directory")

    origin = urlsplit(base).netloc.lower()
    for url, path in urls.items():
        doc = Page()
        try:
            doc.feed(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            flag("error", "PARSE_ERROR", url, str(exc))
            continue

        if not "".join(doc.title).strip():
            flag("error", "MISSING_TITLE", url, "Nonempty <title> required")
        if doc.h1 != 1:
            flag("warning", "H1_COUNT", url, str(doc.h1))
        if not any(d.strip() for d in doc.desc):
            flag("warning", "DESCRIPTION_MISSING", url, "No nonempty meta description")
        if not doc.lang:
            flag("warning", "LANG_MISSING", url, "html lang is absent")
        if not doc.viewport:
            flag("warning", "VIEWPORT_MISSING", url, "viewport meta not found")
        if len(doc.canonical) != 1:
            flag("warning", "CANONICAL_COUNT", url, str(len(doc.canonical)))
        for canonical in doc.canonical:
            parsed = urlsplit(canonical)
            if parsed.scheme not in ("https", "http") or not parsed.netloc:
                flag("warning", "CANONICAL_NOT_ABSOLUTE", url, canonical)
            if parsed.netloc and parsed.netloc.lower() != origin:
                flag("warning", "CANONICAL_EXTERNAL", url, canonical)
            if canonical in canonical_owners and canonical_owners[canonical] != url:
                flag("warning", "SHARED_CANONICAL", url, canonical_owners[canonical])
            canonical_owners[canonical] = url
        if any(re.search(r"\bnoindex\b", x, re.I) for x in doc.robots):
            flag("warning", "NOINDEX_META", url, "Check whether intentionally excluded")
        for image in doc.images:
            if "alt" not in image:
                flag("warning", "IMAGE_ALT_MISSING", url, image.get("src", ""))
        for raw in doc.jsonld:
            try:
                json.loads(raw)
            except ValueError:
                flag("warning", "INVALID_JSONLD", url, "Invalid JSON syntax, not schema eligibility")
        for href in doc.links:
            if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            absolute = urljoin(base.rstrip("/") + url, href)
            target = urlsplit(absolute)
            if target.scheme not in ("http", "https") or target.netloc.lower() != origin:
                continue
            pathname = unquote(target.path)
            candidates = [pathname, pathname.rstrip("/") + "/", pathname.rstrip("/") + ".html"]
            match = next((c for c in candidates if c in urls), None)
            if match:
                inbound[match] += 1
            elif not any((root / pathname.lstrip("/")).is_file() for _ in (0,)):
                flag("warning", "BROKEN_INTERNAL_LINK", url, href)

    for url, count in inbound.items():
        if url != "/" and count == 0:
            flag("warning", "ORPHAN_HTML_PAGE", url, "No incoming HTML link among scanned pages")
    for item in ("sitemap.xml", "robots.txt"):
        if not (root / item).is_file():
            flag("info", "MISSING_" + item.upper().replace(".", "_"), "/" + item, "May be generated by the host")
    return {
        "scope": "offline built HTML only; not runtime/JS DOM/live HTTP/CWV/GSC",
        "base_url": base,
        "scanned": len(files),
        "summary": {s: sum(f["severity"] == s for f in findings) for s in ("error", "warning", "info")},
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", required=True, type=Path)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on", choices=("never", "error", "warning"), default="error")
    args = parser.parse_args()
    if not args.site_dir.is_dir():
        parser.error("--site-dir must be a directory")
    parsed = urlsplit(args.base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        parser.error("--base-url must be an absolute http(s) URL")
    result = audit(args.site_dir, args.base_url)
    data = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data)
    print("scanned=%s findings=%s" % (result["scanned"], result["summary"]))
    severe = result["summary"]
    if args.fail_on == "error" and severe["error"]:
        raise SystemExit(1)
    if args.fail_on == "warning" and (severe["error"] or severe["warning"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
