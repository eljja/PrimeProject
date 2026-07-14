from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket115_twin_complex_cyclotomic_dispersion_audit import (  # noqa: E402
    SCHEMA,
    audit_complex_cyclotomic_dispersion,
    complex_centered_support_envelope,
)


class Ticket115TwinComplexCyclotomicDispersionAuditTests(unittest.TestCase):
    def test_complex_centered_support_bound_is_attainable(self) -> None:
        phases = np.exp(2j * math.pi * np.array([0.1, 0.3, 0.7, 0.9]))
        projected = phases - np.mean(phases)
        target_norm = 9.0
        centered = -target_norm * np.conj(projected) / np.linalg.norm(projected)
        coefficients = (3.0 - 2.0j) + centered
        support = complex_centered_support_envelope(coefficients, phases)
        self.assertAlmostEqual(
            support["complex_centered_coefficient_l2_norm"],
            target_norm,
            places=12,
        )
        self.assertAlmostEqual(
            support["complex_centered_signed_contribution"],
            -support["complex_centered_support_envelope"],
            places=12,
        )
        self.assertLess(support["geometry_identity_error"], 1e-12)

    def test_small_audit_reconstructs_complex_decomposition(self) -> None:
        row = audit_complex_cyclotomic_dispersion(4_096)
        self.assertEqual(row["minor_cell_count"], 162)
        self.assertEqual(row["right_denominator_group_count"], 31)
        self.assertLess(row["maximum_half_ramanujan_real_error"], 1e-10)
        self.assertLess(row["maximum_complex_decomposition_error"], 1e-9)
        self.assertLess(row["aggregate_complex_decomposition_error"], 1e-9)
        self.assertLess(
            row["maximum_complex_geometry_identity_error"],
            1e-10,
        )
        self.assertEqual(row["complex_support_bound_failure_count"], 0)
        self.assertEqual(
            [
                item["right_denominator"]
                for item in row["complex_denominator_profile"]
            ],
            list(range(2, 33)),
        )

    def test_generated_artifact_contract(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket115-twin-complex-cyclotomic-dispersion-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_complex_cyclotomic_dispersion_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 4_194_304)
        self.assertEqual(machine["row_count"], 6)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["right_denominator_group_count"], 31)
        self.assertEqual(
            machine["complex_scalar_centering_reduces_budget_count"],
            6,
        )
        self.assertEqual(machine["orientation_free_worsens_budget_count"], 6)
        self.assertEqual(
            machine["complex_sign_free_finite_closure_count"],
            3,
        )
        self.assertEqual(machine["orientation_free_finite_closure_count"], 2)
        self.assertEqual(machine["contract_failure_count"], 0)
        frontier = audit["rows"][-1]
        self.assertAlmostEqual(
            frontier["complex_sign_free_lower_bound"],
            335_523.7440742075,
            places=6,
        )
        self.assertAlmostEqual(
            frontier["complex_sign_free_budget_to_known_ratio"],
            0.8209817766171058,
            places=12,
        )
        self.assertAlmostEqual(
            frontier["orientation_free_lower_bound"],
            248_127.10487070633,
            places=6,
        )
        self.assertEqual(
            audit["next_theorem_target"],
            "EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget",
        )


if __name__ == "__main__":
    unittest.main()
