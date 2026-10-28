#!/usr/bin/env python3
"""Offline, standard-library audit of *built static HTML*, not a live crawler.

Usage:
  python tools/seo_audit.py --site-dir dist --base-url https://example.com \
      --output seo-audit.json --fail-on error

This cannot verify JS-rendered content, HTTP response codes, actual crawler access,
Core Web Vitals, Google indexation, ranking or revenue.
"""

import argparse
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title_nodes = []
        self.title_depth = 0
        self.h1_nodes = []
        self.h1_depth = 0
        self.descriptions = []
        self.canonicals = []
        self.robots = []
        self.viewport = []
        self.links = []
        self.images = []
        self.assets = []
        self.json_ld = []
        self.script_data = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = (a.get("lang") or "").strip()
        elif tag == "title":
            self.title_nodes.append("")
            self.title_depth += 1
        elif tag == "h1":
            self.h1_nodes.append("")
            self.h1_depth += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt")})
            if a.get("src"):
                self.assets.append(a["src"])
        elif tag == "script":
            if (a.get("type") or "").lower() == "application/ld+json":
                self.script_data = []
            if a.get("src"):
                self.assets.append(a["src"])
        elif tag == "link":
            rels = (a.get("rel") or "").lower().split()
            if "canonical" in rels:
                self.canonicals.append(a.get("href") or "")
            if "stylesheet" in rels and a.get("href"):
                self.assets.append(a["href"])
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            if name == "description":
                self.descriptions.append(a.get("content") or "")
            elif name in {"robots", "googlebot"}:
                self.robots.append(a.get("content") or "")
            elif name == "viewport":
                self.viewport.append(a.get("content") or "")

    def handle_data(self, data):
        if self.title_depth and self.title_nodes:
            self.title_nodes[-1] += data
        if self.h1_depth and self.h1_nodes:
            self.h1_nodes[-1] += data
        if self.script_data is not None:
            self.script_data.append(data)

    def handle_endtag(self, tag):
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        elif tag == "h1" and self.h1_depth:
            self.h1_depth -= 1
        elif tag == "script" and self.script_data is not None:
            self.json_ld.append("".join(self.script_data))
            self.script_data = None


def built_route(path, root):
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[:-10]  # includes trailing slash
    return "/" + relative


def normalized_path(path):
    """Normalize a decoded URL path while preserving its trailing slash."""
    original = path or "/"
    result = posixpath.normpath(original)
    if not result.startswith("/"):
        result = "/" + result
    if original.endswith("/") and result != "/":
        result += "/"
    return result


def local_url(target, current_route, base_url):
    """Return normalized path for a same-origin HTTP URL, otherwise None."""
    absolute = urljoin(base_url.rstrip("/") + current_route, target)
    parsed = urlparse(absolute)
    base = urlparse(base_url)
    if parsed.scheme not in {"https", "http"} or parsed.netloc.lower() != base.netloc.lower():
        return None
    return normalized_path(unquote(parsed.path))


def audit(root, base_url):
    root = root.resolve()
    html_files = sorted(root.rglob("*.html"))
    routes = {built_route(f, root): f for f in html_files}
    aliases = {}
    for url in routes:
        if url.endswith("/") and url != "/":
            aliases[url.rstrip("/")] = url  # host may redirect slash, check production separately
            aliases[url + "index.html"] = url
    findings = []
    pages = []
    inbound = Counter({url: 0 for url in routes})
    seen_titles = {}
    seen_canonicals = {}

    def issue(level, code, route, detail):
        findings.append({"severity": level, "code": code, "page": route, "message": detail})

    def resolve_route(path):
        return path if path in routes else aliases.get(path)

    for file in html_files:
        url = built_route(file, root)
        parser = PageParser()
        try:
            parser.feed(file.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            issue("error", "HTML_PARSE", url, str(exc))
            continue

        title = " ".join(" ".join(parser.title_nodes).split())
        if not title:
            issue("error", "TITLE_MISSING", url, "Missing non-empty HTML title")
        elif title.casefold() in seen_titles:
            issue("warning", "DUPLICATE_TITLE", url, f"Also used on {seen_titles[title.casefold()]}")
        else:
            seen_titles[title.casefold()] = url
        if len(parser.h1_nodes) != 1:
            issue("warning", "H1_COUNT", url, f"Expected one H1; found {len(parser.h1_nodes)}")
        if not any(x.strip() for x in parser.descriptions):
            issue("warning", "DESCRIPTION_MISSING", url, "Missing non-empty meta description")
        if len(parser.descriptions) > 1:
            issue("warning", "DESCRIPTION_MULTIPLE", url, "Multiple meta descriptions")
        if not parser.lang:
            issue("warning", "LANG_MISSING", url, "html lang missing")
        if not parser.viewport:
            issue("warning", "VIEWPORT_MISSING", url, "Mobile viewport meta missing")

        if len(parser.canonicals) != 1:
            issue("warning", "CANONICAL_COUNT", url, f"Expected one canonical; found {len(parser.canonicals)}")
        for canonical in parser.canonicals:
            parsed = urlparse(canonical)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                issue("warning", "CANONICAL_NOT_ABSOLUTE", url, canonical)
                continue
            if parsed.netloc.lower() != urlparse(base_url).netloc.lower():
                issue("warning", "EXTERNAL_CANONICAL", url, canonical)
            if canonical in seen_canonicals:
                issue("warning", "CANONICAL_SHARED", url, f"Also used on {seen_canonicals[canonical]}")
            else:
                seen_canonicals[canonical] = url
            if local_url(canonical, url, base_url) != url:
                issue("warning", "CANONICAL_NONSELF", url, canonical)

        if any("noindex" in r.lower().replace(" ", "") for r in parser.robots):
            issue("warning", "NOINDEX", url, "Robots or Googlebot meta requests noindex; confirm intentionally")
        for img in parser.images:
            if img["alt"] is None:
                issue("warning", "IMG_ALT_MISSING", url, img["src"])
        for script in parser.json_ld:
            try:
                json.loads(script)
            except ValueError:
                issue("warning", "JSON_LD_INVALID", url, "JSON-LD is not valid JSON; semantic validity not checked")

        valid_links = 0
        for href in parser.links:
            path = local_url(href, url, base_url)
            if path is None:
                continue
            destination = resolve_route(path)
            if destination is None:
                issue("warning", "BROKEN_INTERNAL_LINK", url, href)
            else:
                valid_links += 1
                if destination != url:  # self links cannot prove an orphan is discovered
                    inbound[destination] += 1

        for asset in parser.assets:
            path = local_url(asset, url, base_url)
            if path is None:
                continue
            target = (root / path.lstrip("/")).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                issue("warning", "MISSING_LOCAL_ASSET", url, asset)

        pages.append({"route": url, "title": title, "h1_count": len(parser.h1_nodes),
                      "canonical": parser.canonicals, "in_site_links": valid_links,
                      "robots_meta": parser.robots})

    if not html_files:
        issue("error", "NO_HTML", "/", "No built HTML files found")
    for url in routes:
        if url != "/" and not inbound[url]:
            issue("warning", "ORPHAN_PAGE", url, "No inbound links from other built HTML pages")
    if not (root / "robots.txt").is_file():
        issue("info", "ROBOTS_MISSING", "/robots.txt", "Not always mandatory; check real production policy")

    sitemap = root / "sitemap.xml"
    if not sitemap.is_file():
        issue("info", "SITEMAP_MISSING", "/sitemap.xml", "Recommended for discoverability")
    else:
        try:
            sitemap_root = ET.parse(sitemap).getroot()
            tag = sitemap_root.tag.split("}")[-1]
            if tag == "urlset":
                listed = set()
                for elem in sitemap_root.iter():
                    if elem.tag.split("}")[-1] == "loc" and elem.text:
                        path = local_url(elem.text.strip(), "/", base_url)
                        if path is None:
                            issue("warning", "SITEMAP_EXTERNAL_URL", "/sitemap.xml", elem.text.strip())
                        else:
                            listed.add(path)
                            if resolve_route(path) is None:
                                issue("warning", "SITEMAP_ROUTE_MISSING", "/sitemap.xml", elem.text.strip())
                for url in routes:
                    if url not in listed:
                        issue("info", "SITEMAP_PAGE_NOT_LISTED", url, "May be intentional: verify indexation policy")
            elif tag != "sitemapindex":
                issue("warning", "SITEMAP_UNEXPECTED_ROOT", "/sitemap.xml", tag)
        except ET.ParseError as exc:
            issue("error", "SITEMAP_XML_INVALID", "/sitemap.xml", str(exc))

    counts = {s: sum(f["severity"] == s for f in findings) for s in ("error", "warning", "info")}
    return {
        "scope": "Built static HTML only; no HTTP/crawl rendering, Search Console, field CWV or ranking checks",
        "base_url": base_url, "pages_scanned": len(pages), "summary": counts,
        "pages": pages, "findings": findings,
    }


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--site-dir", required=True, type=Path)
    cli.add_argument("--base-url", required=True)
    cli.add_argument("--output", type=Path)
    cli.add_argument("--fail-on", choices=("error", "warning", "never"), default="error")
    args = cli.parse_args(argv)
    if not args.site_dir.is_dir():
        cli.error("--site-dir must point to an existing directory")
    parsed = urlparse(args.base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path not in ("", "/"):
        cli.error("--base-url must be an absolute HTTP(S) site origin without a path")
    report = audit(args.site_dir, args.base_url)
    data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")
    print(f"Scanned {report['pages_scanned']} pages; findings {report['summary']}", file=sys.stderr)
    fail = (args.fail_on == "error" and report["summary"]["error"] > 0 or
            args.fail_on == "warning" and sum(report["summary"][x] for x in ("error", "warning")) > 0)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
