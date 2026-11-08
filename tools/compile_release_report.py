#!/usr/bin/env python3
"""Compile independent release artifacts into a fail-closed evidence summary."""
import argparse
import json
import sys
from pathlib import Path


VALID = {"PASS", "FAIL", "PARTIAL", "NOT_RUN", "NOT_APPLICABLE"}


def classify(kind, evidence):
    if not isinstance(evidence, dict):
        return "FAIL", "Evidence root must be a JSON object"
    if kind == "seo":
        summary = evidence.get("summary")
        if not isinstance(summary, dict) or not isinstance(summary.get("error"), int):
            return "FAIL", "SEO evidence requires summary.error integer"
        errors = summary["error"]
        warnings = summary.get("warning", 0)
        return ("FAIL" if errors else "PASS",
                f"Offline static SEO scan: {errors} errors, {warnings} warnings")
    if kind == "calculation":
        status = evidence.get("status")
        if status == "PASS":
            return "PASS", "Independent golden cases compared with runtime outputs"
        if status == "SCHEMA_VALID":
            return "NOT_RUN", "Fixture schema only; calculation correctness was not executed"
        if status == "FAIL":
            return "FAIL", "Calculation golden-case comparison failed"
        return "FAIL", f"Unknown calculation status: {status!r}"
    if kind == "exports":
        status = evidence.get("status")
        if status == "PASS":
            return "PASS", f"{evidence.get('exports_checked', 0)} export artifacts verified"
        if status == "FAIL":
            return "FAIL", "One or more exported artifacts failed validation"
        return "FAIL", f"Unknown export status: {status!r}"
    if kind == "deployment":
        status = evidence.get("status")
        if status == "PASS":
            return "PASS", "Live HTTP release probe passed"
        if status == "PARTIAL":
            return "PARTIAL", "Live HTTP probe has unverified required evidence"
        if status == "FAIL":
            return "FAIL", "Live HTTP release probe failed"
        return "FAIL", f"Unknown deployment status: {status!r}"
    if kind == "playwright":
        stats = evidence.get("stats")
        if not isinstance(stats, dict):
            return "FAIL", "Playwright JSON evidence requires stats object"
        expected = stats.get("expected", 0)
        unexpected = stats.get("unexpected", 0)
        flaky = stats.get("flaky", 0)
        skipped = stats.get("skipped", 0)
        if not all(isinstance(x, int) and x >= 0 for x in (expected, unexpected, flaky, skipped)):
            return "FAIL", "Playwright stats must be nonnegative integers"
        if expected == 0:
            return "NOT_RUN", "No passing browser tests recorded"
        if unexpected or flaky:
            return "FAIL", f"Browser tests: unexpected={unexpected}, flaky={flaky}"
        if skipped:
            return "PARTIAL", f"Browser tests passed={expected}, skipped={skipped}"
        return "PASS", f"{expected} browser test results passed"
    if kind == "manual":
        status = evidence.get("status")
        if status not in VALID:
            return "FAIL", f"Manual evidence status must be one of {sorted(VALID)}"
        if status == "PASS" and not all(
            isinstance(evidence.get(field), str) and evidence[field].strip()
            for field in ("reviewer", "date", "evidence")
        ):
            return "FAIL", "Manual PASS requires reviewer, date and evidence reference"
        if status == "NOT_APPLICABLE" and not (
            isinstance(evidence.get("reason"), str) and evidence["reason"].strip()
        ):
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
    root = Path(evidence_root).resolve()
    results = []
    errors = []
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
            if required:
                required_count += 1
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
                errors.append(f"{key}: {detail}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            result = {"id": item.get("id") if isinstance(item, dict) else label,
                      "type": item.get("type") if isinstance(item, dict) else None,
                      "required": item.get("required", True) if isinstance(item, dict) else True,
                      "status": "FAIL", "detail": str(exc)}
            if result["required"] is True:
                required_count += 1
            errors.append(f"{label}: {exc}")
        results.append(result)
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
        "checks": results, "errors": errors,
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
