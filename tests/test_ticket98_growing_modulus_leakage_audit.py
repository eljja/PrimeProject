from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket98_growing_modulus_leakage_audit import (  # noqa: E402
    analyze_growing_modulus_leakage,
    occupancy_summary,
)


class Ticket98GrowingModulusLeakageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = analyze_growing_modulus_leakage((10_000, 100_000))

    def test_row_unique_occupancy_boundary(self) -> None:
        self.assertFalse(occupancy_summary(10_003, 2_310)["row_unique_leakage"])
        summary = occupancy_summary(10_003, 30_030)
        self.assertTrue(summary["row_unique_leakage"])
        self.assertEqual(summary["maximum_samples_per_occupied_residue"], 1)
        self.assertEqual(summary["singleton_residue_count"], 10_003)

    def test_first_certificates_equal_first_row_unique_modulus(self) -> None:
        rows = self.audit["machine_audit"]["checkpoint_rows"]
        self.assertEqual(rows[0]["first_row_unique_modulus"], 30_030)
        self.assertEqual(rows[1]["first_row_unique_modulus"], 510_510)
        for checkpoint in rows:
            self.assertEqual(checkpoint["first_goldbach_certificate_modulus"], checkpoint["first_row_unique_modulus"])
            self.assertEqual(checkpoint["first_twin_certificate_modulus"], checkpoint["first_row_unique_modulus"])
            self.assertTrue(checkpoint["goldbach_first_certificate_is_row_unique"])
            self.assertTrue(checkpoint["twin_first_certificate_is_row_unique"])

    def test_no_non_row_unique_certificate(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["non_row_unique_goldbach_certificate_count"], 0)
        self.assertEqual(machine["non_row_unique_twin_certificate_count"], 0)
        self.assertEqual(machine["first_certificate_mismatch_count"], 0)

    def test_projection_contracts_and_claim_boundary(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        for checkpoint in machine["checkpoint_rows"]:
            for row in checkpoint["rows"]:
                self.assertLess(row["relative_orthogonality_error"], 1e-12)
                self.assertLess(row["relative_energy_decomposition_error"], 1e-12)
                self.assertLess(row["goldbach_reconstruction_relative_error"], 1e-12)
                self.assertLess(row["twin_reconstruction_relative_error"], 1e-12)
        self.assertIn("does not prove", self.audit["proof_boundary"])

    def test_next_targets_require_out_of_sample_control(self) -> None:
        self.assertEqual(
            self.audit["goldbach_next_theorem_target"],
            "OutOfSampleGrowingModulusBinaryResidualCancellation",
        )
        self.assertEqual(
            self.audit["twin_next_theorem_target"],
            "OutOfSampleGrowingModulusShiftTwoResidualCancellation",
        )


if __name__ == "__main__":
    unittest.main()
