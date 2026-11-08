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
        self.hreflang = []
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
            if "alternate" in rels and a.get("hreflang") and a.get("href"):
                self.hreflang.append({"code": a["hreflang"].strip(),
                                      "href": a["href"].strip()})
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


def audit(root, base_url, policy=None):
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
    seen_descriptions = {}
    sitemap_listed = None

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
        if parser.descriptions and parser.descriptions[0].strip():
            normalized = " ".join(parser.descriptions[0].split()).casefold()
            if normalized in seen_descriptions:
                issue("warning", "DUPLICATE_DESCRIPTION", url,
                      f"Also used on {seen_descriptions[normalized]}")
            else:
                seen_descriptions[normalized] = url
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
                      "robots_meta": parser.robots, "description": parser.descriptions,
                      "html_lang": parser.lang, "hreflang": parser.hreflang})

    # Validate every hreflang declaration that exists. Completeness for a
    # known language family is opt-in through policy.hreflang_groups below.
    page_by_route = {p["route"]: p for p in pages}
    for page in pages:
        route = page["route"]
        tags = page["hreflang"]
        seen_codes = {}
        self_code = None
        for item in tags:
            code = item["code"]
            href = item["href"]
            folded = code.casefold()
            if not (folded == "x-default" or
                    __import__("re").fullmatch(r"[a-z]{2,3}(?:-[a-z]{2})?", code, flags=__import__("re").I)):
                issue("warning", "HREFLANG_CODE_INVALID", route, code)
            if folded in seen_codes:
                issue("warning", "HREFLANG_DUPLICATE_CODE", route,
                      f"{code} also declared as {seen_codes[folded]}")
            else:
                seen_codes[folded] = href
            parsed = urlparse(href)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                issue("warning", "HREFLANG_NOT_ABSOLUTE", route, href)
            target = local_url(href, route, base_url)
            if target is None:
                issue("info", "HREFLANG_EXTERNAL_UNVERIFIED", route,
                      f"External alternate cannot be checked offline: {href}")
                continue
            destination = resolve_route(target)
            if destination is None:
                issue("warning", "HREFLANG_TARGET_MISSING", route, href)
                continue
            target_page = page_by_route.get(destination)
            if target_page:
                target_canonical = target_page["canonical"]
                if target_canonical != [base_url.rstrip("/") + destination]:
                    issue("warning", "HREFLANG_TARGET_CANONICAL", route,
                          f"{href} target canonical is {target_canonical}")
            if folded != "x-default" and destination == route:
                self_code = code
        if tags and self_code is None:
            issue("warning", "HREFLANG_SELF_MISSING", route,
                  "Page has alternate links but no hreflang entry pointing to its own canonical URL")
        if self_code and page["html_lang"]:
            html_language = page["html_lang"].split("-", 1)[0].casefold()
            hreflang_language = self_code.split("-", 1)[0].casefold()
            if html_language != hreflang_language:
                issue("warning", "HREFLANG_HTML_LANG_MISMATCH", route,
                      f"html lang={page['html_lang']} but self hreflang={self_code}")
        if self_code:
            for item in tags:
                if item["code"].casefold() == "x-default":
                    continue
                target = local_url(item["href"], route, base_url)
                destination = resolve_route(target) if target else None
                target_page = page_by_route.get(destination)
                if not target_page or destination == route:
                    continue
                reciprocal = any(
                    back["code"].casefold() == self_code.casefold() and
                    local_url(back["href"], destination, base_url) == route
                    for back in target_page["hreflang"]
                )
                if not reciprocal:
                    issue("warning", "HREFLANG_RETURN_MISSING", route,
                          f"{destination} does not link back with hreflang={self_code}")

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
        sitemap_listed = set()
        visited_sitemaps = set()

        def read_sitemap(file, depth):
            resolved = file.resolve()
            if not resolved.is_relative_to(root):
                issue("error", "SITEMAP_OUTSIDE_BUILD", "/sitemap.xml", str(file))
                return
            if resolved in visited_sitemaps:
                issue("warning", "SITEMAP_INDEX_CYCLE", "/sitemap.xml", str(file))
                return
            if depth > 5 or len(visited_sitemaps) >= 100:
                issue("error", "SITEMAP_INDEX_LIMIT", "/sitemap.xml",
                      "Sitemap traversal exceeded bounded depth/file count")
                return
            visited_sitemaps.add(resolved)
            try:
                root_tag = ET.parse(resolved).getroot()
            except ET.ParseError as exc:
                issue("error", "SITEMAP_XML_INVALID", "/sitemap.xml", f"{file}: {exc}")
                return
            tag = root_tag.tag.split("}")[-1]
            if tag == "urlset":
                for elem in root_tag.iter():
                    if elem.tag.split("}")[-1] == "loc" and elem.text:
                        target_url = elem.text.strip()
                        local = local_url(target_url, "/", base_url)
                        if local is None:
                            issue("warning", "SITEMAP_EXTERNAL_URL", "/sitemap.xml", target_url)
                        else:
                            sitemap_listed.add(local)
                            if resolve_route(local) is None:
                                issue("warning", "SITEMAP_ROUTE_MISSING", "/sitemap.xml", target_url)
            elif tag == "sitemapindex":
                entries = [e.text.strip() for e in root_tag.iter()
                           if e.tag.split("}")[-1] == "loc" and e.text]
                if not entries:
                    issue("warning", "SITEMAP_INDEX_EMPTY", "/sitemap.xml", str(file))
                for child_url in entries:
                    local = local_url(child_url, "/", base_url)
                    if local is None:
                        issue("warning", "SITEMAP_INDEX_EXTERNAL_CHILD", "/sitemap.xml", child_url)
                        continue
                    child = (root / local.lstrip("/")).resolve()
                    if not child.is_relative_to(root) or not child.is_file():
                        issue("warning", "SITEMAP_INDEX_CHILD_MISSING", "/sitemap.xml", child_url)
                        continue
                    read_sitemap(child, depth + 1)
            else:
                issue("warning", "SITEMAP_UNEXPECTED_ROOT", "/sitemap.xml", tag)

        read_sitemap(sitemap, 0)
        for url in routes:
            if url not in sitemap_listed:
                issue("info", "SITEMAP_PAGE_NOT_LISTED", url,
                      "May be intentional: verify indexation policy")

    # The default audit is advisory. An explicit release policy makes the
    # indexability contract fail-closed without assuming all sites are indexable.
    if policy is not None:
        if not isinstance(policy, dict) or policy.get("mode") not in {"preview", "production"}:
            raise ValueError("Policy must specify mode=preview or production")
        for field in ("required_routes", "indexable_routes"):
            if field in policy and (not isinstance(policy[field], list)
                                    or any(not isinstance(x, str) or not x.startswith("/")
                                           for x in policy[field])):
                raise ValueError(f"Policy {field} must contain absolute URL paths")
        groups = policy.get("hreflang_groups", [])
        if not isinstance(groups, list):
            raise ValueError("hreflang_groups must be a list")
        for index, group in enumerate(groups):
            if not isinstance(group, dict) or not isinstance(group.get("routes"), dict):
                raise ValueError(f"hreflang_groups[{index}] requires a routes object")
            mapping = group["routes"]
            if len(mapping) < 2:
                raise ValueError(f"hreflang_groups[{index}] requires at least two route variants")
            expected = {}
            for route, code in mapping.items():
                if not isinstance(route, str) or not route.startswith("/") or not isinstance(code, str):
                    raise ValueError(f"hreflang_groups[{index}] has invalid route/code")
                if code.casefold() != "x-default" and not __import__("re").fullmatch(
                        r"[a-z]{2,3}(?:-[a-z]{2})?", code, flags=__import__("re").I):
                    raise ValueError(f"hreflang_groups[{index}] has invalid language code {code}")
                if code.casefold() in {x.casefold() for x in expected.values()}:
                    raise ValueError(f"hreflang_groups[{index}] has duplicate language code {code}")
                expected[route] = code
                if resolve_route(route) is None:
                    issue("error", "HREFLANG_GROUP_ROUTE_MISSING", route,
                          f"Declared in hreflang group {index} but absent from build")
            for source_route in expected:
                source = page_by_route.get(resolve_route(source_route))
                if not source:
                    continue
                actual = {}
                for item in source["hreflang"]:
                    target = local_url(item["href"], source_route, base_url)
                    actual[item["code"].casefold()] = target
                for target_route, code in expected.items():
                    if actual.get(code.casefold()) != target_route:
                        issue("error", "HREFLANG_GROUP_INCOMPLETE", source_route,
                              f"Expected {code} -> {base_url.rstrip('/') + target_route}; "
                              f"found route {actual.get(code.casefold())!r}")
        for target in policy.get("required_routes", []):
            if resolve_route(target) is None:
                issue("error", "REQUIRED_ROUTE_MISSING", target, "Approved route absent from build")
        by_route = {p["route"]: p for p in pages}
        if policy["mode"] == "preview":
            if policy.get("indexable_routes"):
                raise ValueError("Preview policy cannot declare indexable_routes")
            mechanism = policy.get("preview_noindex_via", "meta")
            if mechanism not in {"meta", "header"}:
                raise ValueError("preview_noindex_via must be meta or header")
            if mechanism == "header":
                issue("info", "PREVIEW_HEADER_NOT_CHECKED", "/",
                      "Offline scan cannot verify Cloudflare X-Robots-Tag; check live preview headers")
            else:
                for p in pages:
                    if not any("noindex" in r.lower().replace(" ", "")
                               for r in p["robots_meta"]):
                        issue("error", "PREVIEW_INDEXABLE", p["route"],
                              "Preview HTML lacks meta noindex; HTTP headers require separate live checks")
        else:
            targets = policy.get("indexable_routes")
            if not isinstance(targets, list) or not targets:
                raise ValueError("Production policy needs nonempty explicit indexable_routes")
            for target in targets:
                route_key = resolve_route(target)
                if route_key not in by_route:
                    issue("error", "INDEXABLE_ROUTE_MISSING", target, "Approved indexable route absent")
                    continue
                p = by_route[route_key]
                if any("noindex" in r.lower().replace(" ", "") for r in p["robots_meta"]):
                    issue("error", "INDEXABLE_NOINDEX", route_key, "Production route has noindex")
                if p["canonical"] != [base_url.rstrip("/") + route_key]:
                    issue("error", "INDEXABLE_CANONICAL", route_key,
                          "Canonical must exactly match approved origin and route")
                if sitemap_listed is None or route_key not in sitemap_listed:
                    issue("error", "INDEXABLE_SITEMAP", route_key,
                          "Indexable route must be listed in a parsed urlset sitemap")
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
    cli.add_argument("--policy-json", type=Path, help="Optional explicit preview/production route contract")
    args = cli.parse_args(argv)
    if not args.site_dir.is_dir():
        cli.error("--site-dir must point to an existing directory")
    parsed = urlparse(args.base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path not in ("", "/"):
        cli.error("--base-url must be an absolute HTTP(S) site origin without a path")
    try:
        policy = json.loads(args.policy_json.read_text(encoding="utf8")) if args.policy_json else None
        report = audit(args.site_dir, args.base_url, policy)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        cli.error(f"Invalid release policy: {exc}")
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
