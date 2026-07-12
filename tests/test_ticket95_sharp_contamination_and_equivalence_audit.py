from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket95_sharp_contamination_and_equivalence_audit import (  # noqa: E402
    analyze_goldbach_sharp_budget,
    analyze_twin_equivalence_and_budget,
)


class Ticket95SharpContaminationAndEquivalenceAuditTests(unittest.TestCase):
    def test_twin_sharp_budget_and_equivalence(self) -> None:
        audit = analyze_twin_equivalence_and_budget((100, 1_000, 10_000), (10, 30, 100))
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertTrue(all(row["sharp_bound_holds"] for row in machine["checkpoint_rows"]))
        self.assertTrue(all(row["bound_improvement_factor"] > 1 for row in machine["checkpoint_rows"]))
        self.assertTrue(all(row["target_equivalence_error"] < 1e-6 for row in machine["equivalence_rows"]))
        self.assertEqual(audit["next_theorem_target"], "IndependentShiftTwoCorrelationExcess")

    def test_goldbach_sharp_budget_and_screen(self) -> None:
        audit = analyze_goldbach_sharp_budget((100, 1_000, 10_000), 10_000)
        machine = audit["machine_audit"]
        screen = machine["all_even_screen"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["positive_sharp_margin_count"], 3)
        self.assertEqual(screen["last_nonpositive_margin_target"], 38)
        self.assertEqual(screen["observed_positive_suffix_start"], 40)
        self.assertTrue(screen["all_nonpositive_cases_have_goldbach_witness"])
        self.assertLess(screen["maximum_fft_direct_error"], 1e-6)
        self.assertEqual(audit["next_theorem_target"], "UniformBinaryMinorArcDominance")

    def test_claim_boundaries_remain_open(self) -> None:
        twin = analyze_twin_equivalence_and_budget((100, 1_000), (10, 30))
        goldbach = analyze_goldbach_sharp_budget((100, 1_000), 1_000)
        self.assertIn("does not prove", twin["proof_boundary"])
        self.assertIn("does not prove", goldbach["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
