from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket114_twin_ramanujan_numerator_dispersion_audit import (  # noqa: E402
    SCHEMA,
    audit_ramanujan_numerator_dispersion,
    centered_support_envelope,
    integer_mobius,
    ramanujan_sum,
)


class Ticket114TwinRamanujanNumeratorDispersionAuditTests(unittest.TestCase):
    def test_integer_mobius_formula_handles_square_factors(self) -> None:
        self.assertEqual(integer_mobius(1), 1)
        self.assertEqual(integer_mobius(2), -1)
        self.assertEqual(integer_mobius(6), 1)
        self.assertEqual(integer_mobius(12), 0)

    def test_shift_two_ramanujan_sums_are_exact(self) -> None:
        self.assertEqual(ramanujan_sum(1, 2), 1)
        self.assertEqual(ramanujan_sum(2, 2), 1)
        self.assertEqual(ramanujan_sum(3, 2), -1)
        self.assertEqual(ramanujan_sum(4, 2), -2)
        self.assertEqual(ramanujan_sum(5, 2), -1)
        self.assertEqual(ramanujan_sum(6, 2), -1)

    def test_centered_support_bound_is_attainable(self) -> None:
        phases = np.exp(2j * math.pi * np.array([0.1, 0.3, 0.7]))
        cosine = np.real(phases)
        sine = np.imag(phases)
        projected = np.concatenate(
            [cosine - np.mean(cosine), -sine]
        )
        norm = float(np.linalg.norm(projected))
        target_norm = 7.0
        extremizer = -target_norm * projected / norm
        coefficients = extremizer[:3] + 1j * extremizer[3:]
        support = centered_support_envelope(coefficients, phases)
        self.assertAlmostEqual(
            support["coefficient_l2_norm"],
            target_norm,
            places=12,
        )
        self.assertAlmostEqual(
            support["centered_signed_contribution"],
            -support["centered_support_envelope"],
            places=12,
        )

    def test_small_audit_reconstructs_exact_decomposition(self) -> None:
        row = audit_ramanujan_numerator_dispersion(4_096)
        self.assertEqual(row["minor_cell_count"], 162)
        self.assertEqual(row["right_denominator_group_count"], 31)
        self.assertLess(row["maximum_ramanujan_contract_error"], 1e-10)
        self.assertLess(
            row["maximum_rational_boundary_decomposition_error"],
            1e-10,
        )
        self.assertLess(row["type_ii_abel_identity_absolute_error"], 1e-9)
        self.assertLess(row["endpoint_ramanujan_identity_absolute_error"], 1e-9)
        self.assertEqual(row["chord_lipschitz_failure_count"], 0)
        self.assertEqual(row["support_bound_failure_count"], 0)
        self.assertEqual(
            [item["right_denominator"] for item in row["denominator_profile"]],
            list(range(2, 33)),
        )
        self.assertIsInstance(row["signed_mean_l2_closes_finite"], bool)

    def test_generated_artifact_contract(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket114-twin-ramanujan-numerator-dispersion-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_ramanujan_numerator_dispersion_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 4_194_304)
        self.assertEqual(machine["row_count"], 6)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["right_denominator_group_count"], 31)
        self.assertEqual(machine["signed_mean_finite_closure_count"], 4)
        self.assertEqual(machine["sign_free_finite_closure_count"], 3)
        self.assertEqual(
            machine["sign_free_terminal_run_start_horizon"],
            1_048_576,
        )
        self.assertEqual(machine["contract_failure_count"], 0)
        frontier = audit["rows"][-1]
        self.assertAlmostEqual(
            frontier["signed_mean_l2_lower_bound"],
            621_322.8285207893,
            places=6,
        )
        self.assertAlmostEqual(
            frontier["sign_free_l2_lower_bound"],
            327_951.01574892923,
            places=6,
        )
        self.assertEqual(
            audit["next_theorem_target"],
            "EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget",
        )


if __name__ == "__main__":
    unittest.main()
