"""Golden-case contract tests; the validator must not recalculate the product formula."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "validate_calculation_cases.py"
spec = importlib.util.spec_from_file_location("golden_case_validator", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixtures():
    reference = {"method": "independent hand calculation",
                 "evidence": "reviewed-notes/geometry-worked-example.md"}
    return {"version": 1, "cases": [
        {"id": "cut-normal", "tool": "board-cut", "kind": "normal",
         "inputs": {"inches": 12}, "expected": {"mm": 304.8},
         "tolerance": {"mm": 0.0001}, "independent_reference": reference},
        {"id": "cut-boundary", "tool": "board-cut", "kind": "boundary",
         "inputs": {"inches": 0}, "expected": {"mm": 0},
         "independent_reference": reference},
        {"id": "cut-invalid", "tool": "board-cut", "kind": "invalid",
         "inputs": {"inches": -1}, "expected_error": "NEGATIVE_LENGTH",
         "independent_reference": reference}
    ]}


def observations():
    return {"version": 1, "results": [
        {"id": "cut-normal", "status": "ok", "outputs": {"mm": 304.8}},
        {"id": "cut-boundary", "status": "ok", "outputs": {"mm": 0}},
        {"id": "cut-invalid", "status": "error", "error": "NEGATIVE_LENGTH"}
    ]}


class CalculationQualityTests(unittest.TestCase):
    def test_all_classes_and_matching_production_outputs_pass(self):
        issues, count = mod.validate_cases(fixtures(), observations())
        self.assertEqual(count, 3)
        self.assertEqual(issues, [])

    def test_drift_and_error_path_are_detected(self):
        actual = observations()
        actual["results"][0]["outputs"]["mm"] = 300
        actual["results"][2]["error"] = "SILENT_ZERO"
        issues, _ = mod.validate_cases(fixtures(), actual)
        self.assertTrue(any("difference=" in x for x in issues))
        self.assertTrue(any("NEGATIVE_LENGTH" in x for x in issues))

    def test_missing_boundary_golden_case_blocks_contract(self):
        catalog = fixtures()
        catalog["cases"] = catalog["cases"][:1] + catalog["cases"][2:]
        issues, _ = mod.validate_cases(catalog)
        self.assertTrue(any("missing independent boundary" in x for x in issues))

    def test_extra_observation_and_nonfinite_values_fail(self):
        actual = observations()
        actual["results"][0]["outputs"]["mm"] = float("nan")
        actual["results"].append({"id": "hidden", "status": "ok", "outputs": {}})
        issues, _ = mod.validate_cases(fixtures(), actual)
        self.assertTrue(any("NaN/Infinity forbidden" in x for x in issues))
        self.assertTrue(any("extra=" in x for x in issues))

    def test_cli_schema_only_is_not_claimed_as_correctness(self):
        with tempfile.TemporaryDirectory() as td:
            golden = Path(td) / "golden.json"
            golden.write_text(json.dumps(fixtures()), encoding="utf8")
            completed = subprocess.run([sys.executable, str(SCRIPT), "--cases", str(golden),
                                        "--schema-only"], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "SCHEMA_VALID")
            without_engine = subprocess.run([sys.executable, str(SCRIPT), "--cases", str(golden)],
                                            capture_output=True, text=True)
            self.assertNotEqual(without_engine.returncode, 0)

    def test_cli_with_observed_file_is_a_real_gate(self):
        with tempfile.TemporaryDirectory() as td:
            golden = Path(td) / "golden.json"
            observed = Path(td) / "observed.json"
            golden.write_text(json.dumps(fixtures()), encoding="utf8")
            observed.write_text(json.dumps(observations()), encoding="utf8")
            completed = subprocess.run([sys.executable, str(SCRIPT), "--cases", str(golden),
                                        "--observed", str(observed)],
                                       capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
