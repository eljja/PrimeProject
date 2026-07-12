from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket96_fourier_phase_information_audit import analyze_fourier_phase_information  # noqa: E402


class Ticket96FourierPhaseInformationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = analyze_fourier_phase_information((10_000,))

    def test_exact_dft_reconstruction(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        row = machine["checkpoint_rows"][0]
        self.assertLess(row["goldbach_dft_error"], 1e-6)
        self.assertLess(row["twin_dft_error"], 1e-6)

    def test_sparse_energy_only_routes_do_not_certify(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["sparse_goldbach_certificate_count"], 0)
        self.assertEqual(machine["sparse_twin_certificate_count"], 0)
        row = machine["checkpoint_rows"][0]
        self.assertLessEqual(row["best_sparse_goldbach_row"]["major_density"], 0.10)
        self.assertLessEqual(row["best_sparse_twin_row"]["major_density"], 0.10)

    def test_adversarial_spectra_reach_negative_energy_envelope(self) -> None:
        countermodels = self.audit["countermodel_audit"]
        self.assertEqual(countermodels["failure_count"], 0)
        for problem in ("goldbach", "twin"):
            row = countermodels[problem]
            self.assertTrue(row["conjugate_symmetric"])
            self.assertAlmostEqual(row["target_coefficient"], -row["pair_energy"], places=12)

    def test_claim_boundary_and_targets(self) -> None:
        self.assertIn("does not prove", self.audit["proof_boundary"])
        self.assertEqual(self.audit["goldbach_next_theorem_target"], "ArithmeticMinorArcPhaseCancellation")
        self.assertEqual(self.audit["twin_next_theorem_target"], "ShiftTwoSpectralLocalizationOrTypeIICancellation")


if __name__ == "__main__":
    unittest.main()
