from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket89_fixed_log_golden_mean_reduction_lab import (  # noqa: E402
    analyze_fixed_log_reduction,
    fibonacci,
)


class Ticket89FixedLogGoldenMeanReductionTests(unittest.TestCase):
    def test_golden_mean_word_count(self) -> None:
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(66), 27_777_890_035_288)

    def test_exact_reduction_small_audit(self) -> None:
        audit = analyze_fixed_log_reduction(4_096)
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["maximum_zero_run"], 13)
        self.assertEqual(machine["maximum_valuation_excess"], 16)
        self.assertGreater(machine["valuation_excess_at_least_five_count"], 500)
        self.assertIn("floor(log2(k))+5", audit["exact_equivalence"]["pattern_equivalence"])

    def test_target_and_boundaries(self) -> None:
        audit = analyze_fixed_log_reduction(1_024)
        self.assertEqual(audit["theorem_status"], "fixed_log_golden_mean_reduced_exactly_no_collatz_resolution")
        self.assertEqual(audit["next_theorem_target"], "FixedLogValuationExcessFiveInfinitude")
        self.assertIn("no additive-two", audit["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
