from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket97_periodic_projection_residual_audit import analyze_periodic_projection_residuals  # noqa: E402


class Ticket97PeriodicProjectionResidualAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = analyze_periodic_projection_residuals((10_000,))

    def test_projection_contracts_and_exact_reconstruction(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        for row in machine["checkpoint_rows"][0]["rows"]:
            self.assertLess(row["maximum_absolute_residue_residual_sum"], 1e-6)
            self.assertLess(row["orthogonality_error"], 1e-6)
            self.assertLess(row["energy_decomposition_error"], 1e-6)
            self.assertLess(row["goldbach_reconstruction_error"], 1e-6)
            self.assertLess(row["twin_reconstruction_error"], 1e-6)

    def test_optimal_periodic_norm_routes_do_not_certify(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["goldbach_certificate_count"], 0)
        self.assertEqual(machine["twin_certificate_count"], 0)
        for row in machine["checkpoint_rows"][0]["rows"]:
            self.assertLess(row["goldbach_norm_only_lower_bound"], 0)
            self.assertLess(row["twin_norm_only_lower_bound"], 0)

    def test_zero_residue_mean_countermodel_reverses_both_signs(self) -> None:
        countermodel = self.audit["countermodel_audit"]
        self.assertEqual(countermodel["failure_count"], 0)
        self.assertEqual(countermodel["residue_sums"], [0.0, 0.0])
        self.assertEqual(countermodel["goldbach_additive_coefficient"], -4.0)
        self.assertEqual(countermodel["twin_shift_two_coefficient"], -2.0)

    def test_claim_boundary_and_targets(self) -> None:
        self.assertIn("does not prove", self.audit["proof_boundary"])
        self.assertEqual(self.audit["goldbach_next_theorem_target"], "GrowingModulusBinaryResidualCancellation")
        self.assertEqual(self.audit["twin_next_theorem_target"], "GrowingModulusShiftTwoResidualCancellation")


if __name__ == "__main__":
    unittest.main()
