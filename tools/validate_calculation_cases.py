#!/usr/bin/env python3
"""Validate independently reviewed calculator golden cases against observed outputs.

No calculator formula is implemented here: downstream projects must execute the
actual production engine separately and export observed JSON. Schema-only mode
cannot count as calculation correctness verification.
"""
import argparse
import json
import math
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

KINDS = {"normal", "boundary", "invalid"}


def finite_decimal(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("Expected a finite numeric scalar")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"Not a decimal number: {value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"NaN/Infinity forbidden: {value!r}")
    return number


def load_json(path):
    value = json.loads(Path(path).read_text(encoding="utf8"))
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("JSON requires object with version=1")
    return value


def validate_cases(catalog, observed=None):
    issues = []
    cases = catalog.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["Golden-case catalog requires nonempty cases list"], 0
    ids = set()
    classes = defaultdict(set)
    for i, case in enumerate(cases):
        label = f"cases[{i}]"
        if not isinstance(case, dict):
            issues.append(f"{label}: must be an object")
            continue
        key = case.get("id")
        tool = case.get("tool")
        kind = case.get("kind")
        if not isinstance(key, str) or not key.strip() or key in ids:
            issues.append(f"{label}: id must be unique and nonempty")
        else:
            ids.add(key)
            label = key
        if not isinstance(tool, str) or not tool.strip():
            issues.append(f"{label}: tool must be nonempty")
        if kind not in KINDS:
            issues.append(f"{label}: kind must be normal/boundary/invalid")
        if isinstance(tool, str) and tool and kind in KINDS:
            classes[tool].add(kind)
        if not isinstance(case.get("inputs"), dict):
            issues.append(f"{label}: inputs must be a dictionary")
        reference = case.get("independent_reference")
        if (not isinstance(reference, dict) or
                not isinstance(reference.get("method"), str) or
                not reference["method"].strip() or
                not isinstance(reference.get("evidence"), str) or
                not reference["evidence"].strip()):
            issues.append(f"{label}: independently worked reference method and evidence path/URL required")
        if kind == "invalid":
            if not isinstance(case.get("expected_error"), str) or not case["expected_error"]:
                issues.append(f"{label}: invalid case needs expected_error code")
            if "expected" in case:
                issues.append(f"{label}: invalid case must not have numeric expected result")
        else:
            expected = case.get("expected")
            tolerance = case.get("tolerance", {})
            if not isinstance(expected, dict) or not expected:
                issues.append(f"{label}: expected must contain at least one output")
            if not isinstance(tolerance, dict):
                issues.append(f"{label}: tolerance must be an object")
            if isinstance(expected, dict):
                for field, value in expected.items():
                    if not isinstance(field, str) or not field:
                        issues.append(f"{label}: expected output name invalid")
                        continue
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        try:
                            finite_decimal(value)
                            finite_decimal(tolerance.get(field, 0))
                            if finite_decimal(tolerance.get(field, 0)) < 0:
                                issues.append(f"{label}: negative tolerance for {field}")
                        except ValueError as exc:
                            issues.append(f"{label}: {field}: {exc}")
                    elif not isinstance(value, (str, bool)):
                        issues.append(f"{label}: {field}: expected type must be numeric/string/bool")
    for tool, present in classes.items():
        for missing in sorted(KINDS - present):
            issues.append(f"{tool}: missing independent {missing} golden case")
    if observed is None or issues:
        return issues, len(cases)
    results = observed.get("results")
    if not isinstance(results, list):
        return ["Observed output requires results list"], len(cases)
    by_id = {}
    for row in results:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            issues.append("Observed result requires id and object")
            continue
        if row["id"] in by_id:
            issues.append(f"Duplicate observed case: {row['id']}")
        by_id[row["id"]] = row
    if set(by_id) != ids:
        issues.append(f"Observed cases mismatch: missing={sorted(ids-set(by_id))}; extra={sorted(set(by_id)-ids)}")
    for case in cases:
        if not isinstance(case, dict) or case.get("id") not in by_id:
            continue
        key = case["id"]
        row = by_id[key]
        if case.get("kind") == "invalid":
            if row.get("status") != "error" or row.get("error") != case.get("expected_error"):
                issues.append(f"{key}: expected precise error {case.get('expected_error')!r}")
            continue
        if row.get("status") != "ok" or not isinstance(row.get("outputs"), dict):
            issues.append(f"{key}: missing successful runtime outputs")
            continue
        expected = case["expected"]
        actual = row["outputs"]
        if set(actual) != set(expected):
            issues.append(f"{key}: output keys differ expected={sorted(expected)} observed={sorted(actual)}")
            continue
        for field, value in expected.items():
            item = actual[field]
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                try:
                    diff = abs(finite_decimal(item) - finite_decimal(value))
                    limit = finite_decimal(case.get("tolerance", {}).get(field, 0))
                    if diff > limit:
                        issues.append(f"{key}.{field}: difference={diff} exceeds tolerance={limit}")
                except ValueError as exc:
                    issues.append(f"{key}.{field}: {exc}")
            elif type(item) is not type(value) or item != value:
                issues.append(f"{key}.{field}: expected {value!r}, got {item!r}")
    return issues, len(cases)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--observed", type=Path)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not args.schema_only and not args.observed:
        parser.error("--observed required for release verification; --schema-only only validates the fixture contract")
    if args.schema_only and args.observed:
        parser.error("--schema-only cannot be combined with observed results")
    try:
        catalog = load_json(args.cases)
        observations = load_json(args.observed) if args.observed else None
        issues, count = validate_cases(catalog, observations)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues, count = [str(exc)], 0
    report = {"scope": "schema-only; NOT a calculation pass" if args.schema_only else
              "actual runtime outputs compared to independent golden fixtures",
              "cases_checked": count, "status": "FAIL" if issues else
              ("SCHEMA_VALID" if args.schema_only else "PASS"),
              "errors": issues}
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf8")
    else:
        print(payload, end="")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
