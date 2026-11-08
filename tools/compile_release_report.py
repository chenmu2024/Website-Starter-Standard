#!/usr/bin/env python3
"""Compile independent release artifacts into a fail-closed evidence summary."""
import argparse
import json
import sys
from pathlib import Path


VALID = {"PASS", "FAIL", "PARTIAL", "NOT_RUN", "NOT_APPLICABLE"}
EVIDENCE_TYPES = {"seo", "calculation", "exports", "deployment", "playwright", "manual"}


def _count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _playwright_result_count(suites):
    """Count concrete Playwright test result records, not just a claimed stats total."""
    total = 0
    malformed = False

    def visit(items):
        nonlocal total, malformed
        if not isinstance(items, list):
            malformed = True
            return
        for suite in items:
            if not isinstance(suite, dict):
                malformed = True
                continue
            specs = suite.get("specs", [])
            if not isinstance(specs, list):
                malformed = True
                continue
            for spec in specs:
                if not isinstance(spec, dict):
                    malformed = True
                    continue
                tests = spec.get("tests", [])
                if not isinstance(tests, list):
                    malformed = True
                    continue
                for test in tests:
                    if not isinstance(test, dict) or not isinstance(test.get("results"), list):
                        malformed = True
                        continue
                    total += len(test["results"])
            children = suite.get("suites", [])
            if children:
                visit(children)

    visit(suites)
    return total, malformed


def classify(kind, evidence):
    if not isinstance(evidence, dict):
        return "FAIL", "Evidence root must be a JSON object"

    if kind == "seo":
        summary = evidence.get("summary")
        pages = evidence.get("pages")
        findings = evidence.get("findings")
        pages_scanned = evidence.get("pages_scanned")
        if not isinstance(summary, dict):
            return "FAIL", "SEO evidence requires a summary object"
        counts = {name: summary.get(name) for name in ("error", "warning", "info")}
        if not all(_count(value) for value in counts.values()):
            return "FAIL", "SEO summary error/warning/info counts must be nonnegative integers (not booleans)"
        if not _count(pages_scanned) or pages_scanned < 1:
            return "FAIL", "SEO evidence must confirm at least one scanned HTML page"
        if not isinstance(pages, list) or len(pages) != pages_scanned:
            return "FAIL", "SEO pages list must match the positive pages_scanned count"
        if not all(isinstance(page, dict) and _nonempty(page.get("route")) for page in pages):
            return "FAIL", "SEO pages must contain route records"
        if not isinstance(findings, list):
            return "FAIL", "SEO evidence requires a findings list"
        observed = {"error": 0, "warning": 0, "info": 0}
        for finding in findings:
            if not isinstance(finding, dict) or finding.get("severity") not in observed:
                return "FAIL", "SEO findings must be objects with error/warning/info severity"
            if not all(_nonempty(finding.get(field)) for field in ("code", "page", "message")):
                return "FAIL", "SEO findings require code, page and message"
            observed[finding["severity"]] += 1
        if observed != counts:
            return "FAIL", f"SEO summary counts disagree with findings: summary={counts}, observed={observed}"
        errors = counts["error"]
        return ("FAIL" if errors else "PASS",
                f"Offline static SEO scan: {errors} errors, {counts['warning']} warnings across {pages_scanned} pages")

    if kind == "calculation":
        status = evidence.get("status")
        cases_checked = evidence.get("cases_checked")
        errors = evidence.get("errors")
        scope = evidence.get("scope")
        if not _count(cases_checked) or cases_checked < 1 or not isinstance(errors, list):
            return "FAIL", "Calculation evidence requires positive cases_checked and an errors list"
        if errors:
            return "FAIL", f"Calculation evidence contains {len(errors)} error(s)"
        if status == "SCHEMA_VALID":
            if scope != "schema-only; NOT a calculation pass":
                return "FAIL", "Schema-only calculation evidence has an unexpected scope"
            return "NOT_RUN", "Fixture schema only; calculation correctness was not executed"
        if status == "PASS":
            if scope != "actual runtime outputs compared to independent golden fixtures":
                return "FAIL", "Calculation PASS must identify actual runtime/golden-fixture comparison scope"
            return "PASS", f"{cases_checked} independent golden cases compared with runtime outputs"
        if status == "FAIL":
            return "FAIL", "Calculation golden-case comparison failed"
        return "FAIL", f"Unknown calculation status: {status!r}"

    if kind == "exports":
        status = evidence.get("status")
        if status == "FAIL":
            return "FAIL", "One or more exported artifacts failed validation"
        checked = evidence.get("exports_checked")
        results = evidence.get("results")
        errors = evidence.get("errors")
        scope = evidence.get("scope")
        if status != "PASS":
            return "FAIL", f"Unknown export status: {status!r}"
        if not _count(checked) or checked < 1 or not isinstance(results, list) or len(results) != checked:
            return "FAIL", "Export PASS requires a positive exports_checked count matching its results list"
        if not isinstance(errors, list) or errors:
            return "FAIL", "Export PASS requires an empty errors list"
        if not _nonempty(scope) or not scope.startswith("Generated artifact content/structure only"):
            return "FAIL", "Export evidence must retain the generated-artifact-only scope"
        ids = set()
        for result in results:
            if (not isinstance(result, dict) or result.get("status") != "PASS" or
                    not _nonempty(result.get("id")) or result["id"] in ids or
                    not _nonempty(result.get("path"))):
                return "FAIL", "Every export result must have a unique id, path and PASS status"
            ids.add(result["id"])
        return "PASS", f"{checked} export artifacts verified"

    if kind == "deployment":
        status = evidence.get("status")
        if status == "FAIL":
            return "FAIL", "Live HTTP release probe failed"
        if status not in {"PASS", "PARTIAL"}:
            return "FAIL", f"Unknown deployment status: {status!r}"
        checks = evidence.get("checks")
        errors = evidence.get("errors")
        production = evidence.get("production")
        scope = evidence.get("scope")
        if not isinstance(checks, list) or not checks or not isinstance(errors, list):
            return "FAIL", "Deployment evidence requires nonempty checks and an errors list"
        if errors:
            return "FAIL", "Deployment report has errors despite its non-failing status"
        if not _nonempty(production) or not production.startswith("https://"):
            return "FAIL", "Deployment evidence requires an HTTPS production origin"
        if not _nonempty(scope) or not scope.startswith("live HTTP only"):
            return "FAIL", "Deployment evidence must identify its live-HTTP-only scope"
        by_name = {}
        allowed = {"PASS", "FAIL", "PARTIAL", "NOT_RUN", "NOT_APPLICABLE"}
        for check in checks:
            if (not isinstance(check, dict) or not _nonempty(check.get("name")) or
                    check.get("status") not in allowed or not _nonempty(check.get("detail"))):
                return "FAIL", "Deployment checks require unique names, valid statuses and details"
            if check["name"] in by_name:
                return "FAIL", f"Duplicate deployment check: {check['name']}"
            by_name[check["name"]] = check["status"]
        if status == "PARTIAL":
            return "PARTIAL", "Live HTTP probe has unverified required evidence"
        required_names = (
            "homepage", "home-canonical", "production-indexable", "home-title",
            "route:/robots.txt", "route:/sitemap.xml", "sitemap-xml",
            "sitemap-coverage", "real-404", "deployed-commit",
        )
        missing = [name for name in required_names if name not in by_name]
        if missing:
            return "FAIL", f"Deployment PASS is missing required checks: {missing}"
        failed = [name for name, value in by_name.items()
                  if value not in {"PASS", "NOT_APPLICABLE"}]
        if failed:
            return "FAIL", f"Deployment PASS contains non-passing checks: {failed}"
        critical_routes = [name for name in by_name
                           if name.startswith("route:/") and name not in {"route:/robots.txt", "route:/sitemap.xml"}]
        if not critical_routes:
            return "FAIL", "Deployment PASS requires at least one project critical route"
        for route in critical_routes:
            path = route[len("route:"):]
            for prefix in ("canonical:", "indexable:"):
                name = prefix + path
                if by_name.get(name) != "PASS":
                    return "FAIL", f"Deployment PASS requires {name} to PASS"
        if by_name.get("deployed-commit") != "PASS":
            return "FAIL", "Deployment PASS requires verified deployed commit SHA"
        return "PASS", "Live HTTP release checks and deployed source SHA passed"

    if kind == "playwright":
        run_errors = evidence.get("errors")
        if not isinstance(run_errors, list):
            return "FAIL", "Playwright JSON evidence requires a top-level errors list"
        if run_errors:
            return "FAIL", f"Playwright run-level setup/teardown errors: {len(run_errors)}"
        stats = evidence.get("stats")
        if not isinstance(stats, dict):
            return "FAIL", "Playwright JSON evidence requires stats object"
        fields = ("expected", "unexpected", "flaky", "skipped")
        values = {field: stats.get(field) for field in fields}
        if not all(_count(value) for value in values.values()):
            return "FAIL", "Playwright stats must contain nonnegative integer counts (not booleans)"
        suites = evidence.get("suites")
        if not isinstance(suites, list) or not suites:
            return "FAIL", "Playwright evidence requires nonempty suite records"
        result_count, malformed = _playwright_result_count(suites)
        if malformed:
            return "FAIL", "Playwright suite/spec/test result structure is malformed"
        if values["unexpected"] or values["flaky"]:
            return "FAIL", f"Browser tests: unexpected={values['unexpected']}, flaky={values['flaky']}"
        if values["skipped"]:
            return "PARTIAL", f"Browser tests passed={values['expected']}, skipped={values['skipped']}"
        if values["expected"] == 0:
            return "FAIL" if result_count else "NOT_RUN", (
                "Playwright suite has result records but zero passing tests" if result_count
                else "No passing browser tests recorded"
            )
        if result_count < values["expected"]:
            return "FAIL", f"Playwright stats claim {values['expected']} passes but only {result_count} result records exist"
        return "PASS", f"{values['expected']} browser test results passed"

    if kind == "manual":
        status = evidence.get("status")
        if status not in VALID:
            return "FAIL", f"Manual evidence status must be one of {sorted(VALID)}"
        if status == "PASS" and not all(
            _nonempty(evidence.get(field))
            for field in ("reviewer", "date", "evidence")
        ):
            return "FAIL", "Manual PASS requires reviewer, date and evidence reference"
        if status == "NOT_APPLICABLE" and not _nonempty(evidence.get("reason")):
            return "FAIL", "NOT_APPLICABLE requires a written reason"
        return status, evidence.get("reason") or evidence.get("notes") or "Manual review evidence"

    return "FAIL", f"Unsupported evidence type: {kind!r}"

def compile_report(manifest, evidence_root):
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        return {"status": "FAIL", "decision": "INVALID_MANIFEST",
                "checks": [], "errors": ["Manifest must be an object with version=1"]}
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        return {"status": "FAIL", "decision": "INVALID_MANIFEST",
                "checks": [], "errors": ["Manifest requires a nonempty checks list"]}

    # Validate the complete manifest before reading evidence. A malformed
    # optional-looking entry must not be downgraded to a warning and ignored.
    manifest_errors = []
    manifest_ids = set()
    required_count = 0
    for index, item in enumerate(checks):
        label = f"checks[{index}]"
        if not isinstance(item, dict):
            manifest_errors.append(f"{label}: entry must be an object")
            continue
        key = item.get("id")
        kind = item.get("type")
        required = item.get("required")
        relative = item.get("file")
        if not isinstance(key, str) or not key.strip() or key in manifest_ids:
            manifest_errors.append(f"{label}: check id must be unique and nonempty")
        else:
            manifest_ids.add(key)
            label = key
        if kind not in EVIDENCE_TYPES:
            manifest_errors.append(f"{label}: unsupported evidence type {kind!r}")
        if not isinstance(required, bool):
            manifest_errors.append(f"{label}: required must be boolean")
        elif required:
            required_count += 1
        if not _nonempty(relative):
            manifest_errors.append(f"{label}: file must be a nonempty relative path")
    if required_count == 0:
        manifest_errors.append("At least one required release check must be declared")
    if manifest_errors:
        return {"status": "FAIL", "decision": "INVALID_MANIFEST",
                "checks": [], "errors": manifest_errors}

    root = Path(evidence_root).resolve()
    results = []
    errors = []
    warnings = []
    seen = set()
    required_count = 0
    for index, item in enumerate(checks):
        label = f"checks[{index}]"
        try:
            if not isinstance(item, dict):
                raise ValueError("entry must be an object")
            key = item.get("id")
            if not isinstance(key, str) or not key.strip() or key in seen:
                raise ValueError("check id must be unique and nonempty")
            seen.add(key)
            label = key
            kind = item.get("type")
            required = item.get("required")
            if not isinstance(required, bool):
                raise ValueError("required must be boolean")
            relative = item.get("file")
            if not isinstance(relative, str) or not relative.strip():
                raise ValueError("file must be a nonempty relative path")
            path = (root / relative).resolve()
            if not path.is_relative_to(root) or path == root:
                raise ValueError("evidence path escapes evidence directory")
            if not path.is_file():
                status, detail = "NOT_RUN", f"Evidence file missing: {relative}"
            else:
                evidence = json.loads(path.read_text(encoding="utf8"))
                status, detail = classify(kind, evidence)
            result = {"id": key, "type": kind, "required": required,
                      "status": status, "file": relative, "detail": detail}
            if status == "FAIL":
                (errors if required else warnings).append(f"{key}: {detail}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            result = {"id": item.get("id") if isinstance(item, dict) else label,
                      "type": item.get("type") if isinstance(item, dict) else None,
                      "required": item.get("required", True) if isinstance(item, dict) else True,
                      "status": "FAIL", "detail": str(exc)}
            (errors if result["required"] is True else warnings).append(f"{label}: {exc}")
        results.append(result)
        if result["required"] is True:
            required_count += 1
    if required_count == 0:
        errors.append("At least one required release check must be declared")
        status, decision = "FAIL", "INVALID_MANIFEST"
    else:
        required = [item for item in results if item["required"]]
        if any(item["status"] == "FAIL" for item in required):
            status, decision = "FAIL", "BLOCKED"
        elif any(item["status"] in {"NOT_RUN", "PARTIAL"} for item in required):
            status, decision = "PARTIAL", "EVIDENCE_INCOMPLETE"
        else:
            status, decision = "PASS", "REQUIRED_GATES_PASS"
    return {
        "status": status, "decision": decision,
        "project": manifest.get("project", "UNSPECIFIED"),
        "required_checks": required_count,
        "required_passed": sum(x["required"] and x["status"] in {"PASS", "NOT_APPLICABLE"} for x in results),
        "checks": results, "errors": errors, "warnings": warnings,
        "scope": "Overall status evaluates required checks only; optional gaps remain visible. No missing evidence is inferred as PASS."
    }


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--manifest", required=True, type=Path)
    cli.add_argument("--evidence-dir", required=True, type=Path)
    cli.add_argument("--output", type=Path)
    args = cli.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf8"))
        report = compile_report(manifest, args.evidence_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {"status": "FAIL", "decision": "INVALID_MANIFEST",
                  "checks": [], "errors": [str(exc)]}
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf8")
    else:
        print(payload, end="")
    print(f"Release evidence summary: {report['status']}", file=sys.stderr)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
