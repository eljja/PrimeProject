from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket112_twin_farey_endpoint_abel_audit import (  # noqa: E402
    analyze_ticket112,
    audit_farey_endpoint_abel,
    connected_components,
)


class Ticket112TwinFareyEndpointAbelAuditTests(unittest.TestCase):
    def test_connected_components_are_exact(self) -> None:
        mask = np.array([False, True, True, False, True, False, True, True])
        self.assertEqual(
            [component.tolist() for component in connected_components(mask)],
            [[1, 2], [4], [6, 7]],
        )

    def test_abel_identity_reconstructs_type_ii_minor(self) -> None:
        row = audit_farey_endpoint_abel(4_096)
        self.assertEqual(row["minor_cell_count"], 162)
        self.assertLess(row["abel_identity_absolute_error"], 1e-9)
        self.assertEqual(row["lambda_reconstruction_max_error"], 0.0)

    def test_endpoint_triangle_is_insufficient(self) -> None:
        row = audit_farey_endpoint_abel(4_096)
        self.assertTrue(row["farey_abel_route_refuted"])
        self.assertLess(row["farey_abel_lower_bound"], 0)
        self.assertLess(row["farey_abel_envelope"], row["phase_blind_bin_envelope"])

    def test_full_audit_and_holdout_contract(self) -> None:
        audit = analyze_ticket112()
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 2_097_152)
        self.assertEqual(machine["row_count"], 5)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["endpoint_triangle_refutation_count"], 5)
        self.assertEqual(machine["holdout_candidate_failure_count"], 0)
        self.assertEqual(machine["contract_failure_count"], 0)
        holdout = audit["rows"][-1]
        self.assertTrue(holdout["inherited_endpoint_inequality_passes"])
        self.assertTrue(holdout["inherited_positivity_closes"])
        self.assertGreater(holdout["inherited_lower_bound"], 0)


if __name__ == "__main__":
    unittest.main()
