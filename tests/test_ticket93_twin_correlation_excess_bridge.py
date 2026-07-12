from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket93_twin_correlation_excess_bridge import (  # noqa: E402
    analyze_twin_correlation_bridge,
    contamination_weight_bound,
    prime_power_count_bound,
)


class Ticket93TwinCorrelationExcessBridgeTests(unittest.TestCase):
    def test_elementary_bounds_are_sublinear(self) -> None:
        self.assertGreater(prime_power_count_bound(1_000), 0)
        self.assertGreater(contamination_weight_bound(1_000), 0)
        self.assertLess(contamination_weight_bound(10**18) / 10**18, 0.01)

    def test_exact_bridge_and_surrogate_counterexamples(self) -> None:
        audit = analyze_twin_correlation_bridge(100_000, 20_000)
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["final_twin_pair_count"], 1_224)
        self.assertGreater(machine["final_contamination"], 0)
        self.assertTrue(all(row["positive_surrogate_is_not_lower_bound"] for row in audit["surrogate_no_go"]["rows"]))

    def test_target_and_claim_boundary(self) -> None:
        audit = analyze_twin_correlation_bridge(20_000, 10_000)
        self.assertEqual(audit["next_theorem_target"], "ShiftTwoTypeIICorrelationExcess")
        self.assertIn("does not prove", audit["proof_boundary"])
        self.assertIn("limsup", audit["exact_correlation_bridge"]["sufficiency"])


if __name__ == "__main__":
    unittest.main()
