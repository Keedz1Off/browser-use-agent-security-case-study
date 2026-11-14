"""Offline checks of the evidence shipped with this portfolio entry."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


from copy import deepcopy

from trace_oracle import assess_trace


class TraceOracleTests(unittest.TestCase):
    def test_valid_trace_passes_and_unexpected_action_fails(self):
        contract = {
            "required_path": "/details",
            "allowed_hosts": ["127.0.0.1"],
            "allowed_actions": ["done"],
            "code": "SYNTHETIC-CODE",
            "actor": "review-user-A",
        }
        trace = {
            "browser_started": True,
            "requests": [{"path": "/details", "url": "http://127.0.0.1/details"}],
            "actions": ["done"],
            "final_result": "SYNTHETIC-CODE",
            "actor": "review-user-A",
        }
        self.assertEqual(assess_trace(trace, contract), [])

        changed = deepcopy(trace)
        changed["actions"].append("unregistered_test_action")
        self.assertEqual(assess_trace(changed, contract), ["UNEXPECTED_ACTION"])


class RecordedEvidenceTests(unittest.TestCase):
    def test_navigation_observation_is_linked(self):
        row = read_json("matrices/NAVIGATION.json")["rows"][0]
        record = read_json("evidence/failures.json")[0]
        self.assertEqual(row["test_name"], record["original_test_name"])
        self.assertEqual(record["raw_outcome"], "failure")
        self.assertIn("/plain GET", record["observed"])
        self.assertIn("error", record["observed"])

    def test_format_records_preserve_allowed_action_and_code(self):
        rows = read_json("matrices/MODEL-OUTPUT.json")["rows"]
        records = {row["id"]: row for row in read_json("evidence/failures.json")}
        for row in rows:
            with self.subTest(case=row["id"]):
                record = records[row["id"]]
                self.assertEqual(record["recorded_actions"], record["allowed_actions"])
                self.assertTrue(record["code_preserved"])
                self.assertNotEqual(record["expected"], record["observed"])

    def test_reported_coverage_reconciles(self):
        report = read_json("evidence/coverage.json")
        self.assertEqual(
            report["latest_total"] - report["latest_passed"],
            len(read_json("evidence/failures.json")),
        )
