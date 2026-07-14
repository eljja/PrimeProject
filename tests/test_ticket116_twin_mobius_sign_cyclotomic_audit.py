from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket116_twin_mobius_sign_cyclotomic_audit import (  # noqa: E402
    SCHEMA,
    audit_mobius_sign_cyclotomic,
    vaughan_mobius_sign_layers,
)


class Ticket116TwinMobiusSignCyclotomicAuditTests(unittest.TestCase):
    def test_time_domain_sign_layers_reconstruct_vaughan_type_ii(self) -> None:
        _, positive, negative, metadata = vaughan_mobius_sign_layers(4_096)
        self.assertTrue(np.all(positive >= 0.0))
        self.assertTrue(np.all(negative >= 0.0))
        self.assertLess(
            metadata["time_domain_sign_layer_reconstruction_max_error"],
            1e-12,
        )
        self.assertGreater(metadata["positive_outer_divisor_count"], 0)
        self.assertGreater(metadata["negative_outer_divisor_count"], 0)

    def test_small_audit_reconstructs_endpoint_and_polarization(self) -> None:
        row = audit_mobius_sign_cyclotomic(4_096)
        self.assertLess(row["maximum_profile_reconstruction_error"], 1e-9)
        self.assertLess(
            row["inherited_signed_budget_reconstruction_error"],
            1e-9,
        )
        self.assertLess(row["maximum_polarization_identity_error"], 1e-8)
        self.assertEqual(row["mobius_sign_minor_cell_count"], 162)
        self.assertEqual(
            len(row["mobius_sign_denominator_profile"]),
            31,
        )
        self.assertGreater(row["independent_sign_budget_inflation"], 0.0)
        self.assertFalse(row["independent_sign_closes_finite"])

    def test_generated_artifact_contract(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket116-twin-mobius-sign-cyclotomic-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_mobius_sign_cyclotomic_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 4_194_304)
        self.assertEqual(machine["row_count"], 6)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["right_denominator_group_count"], 31)
        self.assertEqual(machine["outer_pair_count"], 1_650_675)
        self.assertEqual(
            machine["independent_sign_budget_worsens_count"],
            6,
        )
        self.assertEqual(
            machine["independent_sign_finite_closure_count"],
            0,
        )
        self.assertEqual(machine["positive_aggregate_covariance_count"], 4)
        self.assertEqual(machine["contract_failure_count"], 0)
        frontier = audit["rows"][-1]
        self.assertAlmostEqual(
            frontier["independent_sign_budget_ratio"],
            2.888576909532816,
            places=12,
        )
        self.assertAlmostEqual(
            frontier["independent_sign_lower_bound"],
            -2_401_998.6601239927,
            places=6,
        )
        self.assertAlmostEqual(
            frontier["signed_lower_bound"],
            335_523.7440742075,
            places=6,
        )
        self.assertEqual(
            audit["next_theorem_target"],
            "EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget",
        )


if __name__ == "__main__":
    unittest.main()
