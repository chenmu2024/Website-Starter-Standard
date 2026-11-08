#!/usr/bin/env python3
"""Read-only live HTTP release checks. Not a Google/Bing/AI crawler simulation."""
import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urljoin


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.robots = []
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "link" and "canonical" in props.get("rel", "").lower().split():
            self.canonical.append(props.get("href", ""))
        if tag == "meta" and props.get("name", "").lower() in {"robots", "googlebot"}:
            self.robots.append(props.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def fetch(url, timeout=15):
    """GET bytes (limited to 2 MiB). An HTTP error is evidence, not an exception."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "WebsiteStarterStandard-ReleaseProbe/1.0 (read-only QA)",
        "Accept": "text/html, application/xml, application/json, */*",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "url": resp.geturl(),
                    "headers": dict(resp.headers.items()), "body": resp.read(2097153)}
    except urllib.error.HTTPError as exc:
        with exc:
            return {"status": exc.code, "url": exc.geturl(),
                    "headers": dict(exc.headers.items()), "body": exc.read(2097153)}


def inspect(base, routes=(), preview_url=None, expected_sha=None,
            version_path="/build-info.json", timeout=15):
    base = base.rstrip("/")
    problems = []
    checks = []

    def check(name, status, detail):
        checks.append({"name": name, "status": status, "detail": detail})
        if status == "FAIL":
            problems.append(name + ": " + detail)

    def get(path, origin=base):
        target = origin.rstrip("/") + path
        try:
            result = fetch(target, timeout)
            host = urlparse(result["url"]).netloc
            if host != urlparse(origin).netloc:
                check("host:" + path, "FAIL", "Unexpected final host " + host)
            if len(result["body"]) > 2097152:
                check("body-size:" + path, "FAIL", "Response exceeds 2 MiB inspection limit")
            return result
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            check("network:" + path, "FAIL", f"{type(exc).__name__}: {exc}")
            return None

    main = get("/")
    if main:
        check("homepage", "PASS" if main["status"] == 200 else "FAIL",
              f"HTTP {main['status']}")
        head = Head()
        head.feed(main["body"].decode("utf8", errors="replace"))
        check("home-canonical", "PASS" if head.canonical == [base + "/"] else "FAIL",
              f"canonical={head.canonical}; expected={base + '/'}")
        response_headers = {str(k).lower(): str(v).lower() for k, v in main["headers"].items()}
        robots = ",".join(head.robots).lower() + "," + response_headers.get("x-robots-tag", "")
        check("production-indexable", "FAIL" if "noindex" in robots else "PASS",
              f"homepage robots directives: {robots}")
        check("home-title", "PASS" if "".join(head.title).strip() else "FAIL",
              "Homepage must serve title in raw HTML")

    required_sitemap_paths = {"/", *routes}
    for path in ["/robots.txt", "/sitemap.xml", *routes]:
        res = get(path)
        if res:
            check("route:" + path, "PASS" if res["status"] == 200 else "FAIL",
                  f"HTTP {res['status']}")
            if path in routes and res["status"] == 200:
                page = Head()
                page.feed(res["body"].decode("utf8", errors="replace"))
                expect_url = base + path
                check("canonical:" + path, "PASS" if page.canonical == [expect_url] else "FAIL",
                      f"canonical={page.canonical}, expected={expect_url}")
                headers = {str(k).lower(): str(v).lower() for k, v in res["headers"].items()}
                directives = ",".join(page.robots).lower() + "," + headers.get("x-robots-tag", "")
                check("indexable:" + path, "FAIL" if "noindex" in directives else "PASS",
                      f"robots directives={directives}")
            if path == "/robots.txt" and res["status"] == 200:
                content = res["body"].decode("utf8", errors="replace")
                groups = []
                current_agents = []
                current_rules = []
                for line in content.splitlines():
                    line = line.split("#", 1)[0].strip()
                    if not line or ":" not in line:
                        if current_agents or current_rules:
                            groups.append((current_agents, current_rules))
                        current_agents, current_rules = [], []
                        continue
                    key, value = (part.strip().lower() for part in line.split(":", 1))
                    if key == "user-agent":
                        if current_rules:
                            groups.append((current_agents, current_rules))
                            current_agents, current_rules = [], []
                        current_agents.append(value)
                    elif key == "disallow":
                        current_rules.append(value)
                if current_agents or current_rules:
                    groups.append((current_agents, current_rules))
                sitewide_block = any("*" in agents and "/" in rules for agents, rules in groups)
                check("robots-global-indexing", "FAIL" if sitewide_block else "PASS",
                      "Sitewide User-agent:* Disallow:/ found" if sitewide_block
                      else "No obvious blanket Disallow:/ on default user agent")
            if path == "/sitemap.xml" and res["status"] == 200:
                try:
                    doc = ET.fromstring(res["body"])
                    tag = doc.tag.rsplit("}", 1)[-1]
                    check("sitemap-xml", "PASS" if tag in {"urlset", "sitemapindex"} else "FAIL",
                          f"XML root={tag}")
                    if tag == "sitemapindex":
                        check("sitemap-coverage", "NOT_RUN",
                              "Nested sitemap contents not traversed; verify URL coverage separately")
                    if tag == "urlset":
                        listed = set()
                        for element in doc.iter():
                            if element.tag.rsplit("}", 1)[-1] == "loc" and element.text:
                                listed.add(element.text.strip())
                        absent = sorted(base + route for route in required_sitemap_paths
                                        if base + route not in listed)
                        check("sitemap-coverage", "PASS" if not absent else "FAIL",
                              f"Missing critical canonical URLs: {absent}")
                except ET.ParseError as exc:
                    check("sitemap-xml", "FAIL", str(exc))

    not_found = get("/__website-standard-release-probe-missing-404__")
    if not_found:
        check("real-404", "PASS" if not_found["status"] == 404 else "FAIL",
              f"expected HTTP 404, found {not_found['status']}")

    if preview_url:
        preview = get("/", origin=preview_url.rstrip("/"))
        if preview:
            check("preview-home", "PASS" if preview["status"] == 200 else "FAIL",
                  f"HTTP {preview['status']}")
            head = Head()
            head.feed(preview["body"].decode("utf8", errors="replace"))
            headers = {str(k).lower(): str(v).lower() for k, v in preview["headers"].items()}
            directives = ",".join(head.robots).lower() + "," + headers.get("x-robots-tag", "")
            check("preview-noindex", "PASS" if "noindex" in directives else "FAIL",
                  "Preview must supply noindex via raw HTML or X-Robots-Tag")
    else:
        check("preview-noindex", "NOT_APPLICABLE", "No preview URL supplied; record manually if one exists")

    if expected_sha:
        result = get(version_path)
        if result:
            if result["status"] != 200:
                check("deployed-commit", "FAIL", f"version endpoint HTTP {result['status']}")
            else:
                try:
                    info = json.loads(result["body"].decode("utf8"))
                    actual = info.get("commit")
                    check("deployed-commit",
                          "PASS" if actual == expected_sha else "FAIL",
                          f"deployed commit={actual!r}, required={expected_sha!r}")
                except (ValueError, UnicodeError, AttributeError) as exc:
                    check("deployed-commit", "FAIL", f"unreadable version JSON: {exc}")
    else:
        check("deployed-commit", "NOT_RUN",
              "Pass --expected-sha and publish /build-info.json with a commit field")

    status = "FAIL" if problems else ("PARTIAL" if any(x["status"] == "NOT_RUN" for x in checks) else "PASS")
    return {"scope": "live HTTP only; not Cloudflare account/WAF/verified bot/GSC or AI citations",
            "production": base, "preview": preview_url, "status": status,
            "checks": checks, "errors": problems}


def origin(value):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/"):
        raise argparse.ArgumentTypeError("Production/preview URL must be an HTTPS origin without path")
    return value.rstrip("/")


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--url", type=origin, required=True)
    cli.add_argument("--route", action="append", default=[])
    cli.add_argument("--preview-url", type=origin)
    cli.add_argument("--expected-sha")
    cli.add_argument("--version-path", default="/build-info.json")
    cli.add_argument("--timeout", type=int, default=15)
    cli.add_argument("--output", type=Path)
    args = cli.parse_args(argv)
    if any(not r.startswith("/") or r.startswith("//") for r in args.route):
        cli.error("--route values must be same-site absolute URL paths")
    if not args.version_path.startswith("/") or args.version_path.startswith("//"):
        cli.error("--version-path must be a same-site URL path")
    if args.timeout < 1 or args.timeout > 60:
        cli.error("--timeout must be 1..60 seconds")
    report = inspect(args.url, args.route, args.preview_url,
                     args.expected_sha, args.version_path, args.timeout)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf8")
    else:
        print(payload, end="")
    print(f"Production HTTP release gate: {report['status']}", file=sys.stderr)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
