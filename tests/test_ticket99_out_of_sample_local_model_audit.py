from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket99_out_of_sample_local_model_audit import (  # noqa: E402
    analyze_out_of_sample_local_models,
    local_pair_density_floor,
)


class Ticket99OutOfSampleLocalModelAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = analyze_out_of_sample_local_models((10_000,), 200_000)

    def test_local_density_formula_matches_primorial_values(self) -> None:
        self.assertAlmostEqual(local_pair_density_floor(30)["minimum_pair_density"], 1.40625)
        self.assertAlmostEqual(local_pair_density_floor(210)["minimum_pair_density"], 1.3671875)

    def test_cross_fit_is_disjoint_and_does_not_certify(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["cross_fit_goldbach_certificate_count"], 0)
        self.assertEqual(machine["cross_fit_twin_certificate_count"], 0)
        row = machine["cross_fit_checkpoint_rows"][0]
        self.assertGreater(row["nonempty_configuration_count"], 0)
        self.assertEqual(row["best_nonempty_goldbach_row"]["train_evaluation_overlap_count"], 0)
        self.assertEqual(row["best_nonempty_twin_row"]["train_evaluation_overlap_count"], 0)

    def test_external_main_lower_bound_and_norm_no_go(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["external_main_failure_count"], 0)
        self.assertEqual(machine["external_goldbach_norm_certificate_count"], 0)
        self.assertEqual(machine["external_twin_norm_certificate_count"], 0)

    def test_finite_envelope_holdout_and_boundary(self) -> None:
        envelope = self.audit["machine_audit"]["finite_residual_envelope_screen"]
        self.assertGreaterEqual(envelope["candidate_log_envelope_constant"], 1.5)
        self.assertLessEqual(envelope["candidate_log_envelope_constant"], 1.7)
        self.assertEqual(envelope["goldbach_validation_failure_count"], 0)
        self.assertEqual(envelope["twin_validation_failure_count"], 0)
        self.assertIn("not_an_asymptotic_theorem", envelope["status"])

    def test_claim_boundary_and_next_targets(self) -> None:
        self.assertEqual(self.audit["machine_audit"]["total_failure_count"], 0)
        self.assertIn("does not prove", self.audit["proof_boundary"])
        self.assertEqual(self.audit["goldbach_next_theorem_target"], "UniformExternalLocalModelGoldbachResidualDecay")
        self.assertEqual(self.audit["twin_next_theorem_target"], "UniformExternalLocalModelShiftTwoResidualDecay")


if __name__ == "__main__":
    unittest.main()
