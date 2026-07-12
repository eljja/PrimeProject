from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket94_signed_remainder_and_goldbach_bridge import (  # noqa: E402
    analyze_goldbach_bridge,
    analyze_twin_signed_remainder,
)


class Ticket94SignedRemainderAndGoldbachBridgeTests(unittest.TestCase):
    def test_twin_exact_decomposition_and_norm_no_go(self) -> None:
        audit = analyze_twin_signed_remainder(20_000, (10, 30, 100))
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["positive_norm_lower_bound_count"], 0)
        self.assertTrue(all(row["norm_only_lower_bound"] < 0 for row in machine["rows"]))
        self.assertEqual(audit["next_theorem_target"], "JointShiftTwoSignedRemainderLowerBound")

    def test_goldbach_bridge_decomposes_prime_powers(self) -> None:
        audit = analyze_goldbach_bridge((100, 1_000, 10_000))
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["positive_certified_margin_count"], 0)
        self.assertTrue(all(row["goldbach_prime_weight"] > 0 for row in machine["rows"]))
        self.assertEqual(audit["next_theorem_target"], "UniformBinaryLambdaCorrelationExcess")

    def test_claim_boundaries_remain_open(self) -> None:
        twin = analyze_twin_signed_remainder(5_000, (10, 30))
        goldbach = analyze_goldbach_bridge((100, 1_000))
        self.assertIn("does not prove", twin["proof_boundary"])
        self.assertIn("does not prove", goldbach["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
