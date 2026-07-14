from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket113_twin_farey_denominator_endpoint_audit import (  # noqa: E402
    SCHEMA,
    audit_farey_denominator_endpoints,
    reduced_farey_centers,
    right_boundary_labels,
)


class Ticket113TwinFareyDenominatorEndpointAuditTests(unittest.TestCase):
    def test_reduced_farey_centers_are_complete_and_ordered(self) -> None:
        fractions = reduced_farey_centers(32)
        self.assertEqual(len(fractions), 163)
        self.assertEqual(fractions[0], (0.0, 0, 1))
        self.assertEqual(fractions[-1], (0.5, 1, 2))
        self.assertEqual(fractions, sorted(fractions))

    def test_right_boundary_label_uses_adjacent_farey_fraction(self) -> None:
        frequencies = np.linspace(0.0, 0.5, 1_025)
        cells = [np.array([1], dtype=np.int64), np.array([1_023], dtype=np.int64)]
        labels, failures = right_boundary_labels(cells, frequencies, 32)
        self.assertEqual(failures, 0)
        self.assertEqual(labels[0]["left_numerator"], 0)
        self.assertEqual(labels[0]["right_numerator"], 1)
        self.assertEqual(labels[-1]["right_numerator"], 1)
        self.assertEqual(labels[-1]["right_denominator"], 2)

    def test_small_audit_reconstructs_both_exact_identities(self) -> None:
        row = audit_farey_denominator_endpoints(4_096)
        self.assertEqual(row["minor_cell_count"], 162)
        self.assertEqual(row["right_denominator_group_count"], 31)
        self.assertEqual(row["farey_adjacency_failure_count"], 0)
        self.assertLess(row["abel_identity_absolute_error"], 1e-9)
        self.assertLess(row["denominator_group_identity_absolute_error"], 1e-9)
        self.assertLess(
            row["right_denominator_group_envelope"],
            row["endpoint_absolute_envelope"],
        )

    def test_generated_holdout_contract(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket113-twin-farey-denominator-endpoint-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_farey_denominator_endpoint_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 4_194_304)
        self.assertEqual(machine["row_count"], 6)
        self.assertEqual(machine["calibration_row_count"], 5)
        self.assertEqual(machine["holdout_row_count"], 1)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["right_denominator_group_count"], 31)
        self.assertEqual(machine["contract_failure_count"], 0)
        holdout = audit["rows"][-1]
        self.assertEqual(holdout["split"], "post_selection_holdout")
        self.assertTrue(holdout["grouped_triangle_closes_finite"])
        self.assertGreater(holdout["grouped_lower_bound"], 0)


if __name__ == "__main__":
    unittest.main()
