from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket80_least_counterexample_compactness_no_go_lab import (  # noqa: E402
    accelerated_step,
    all_ones_affine_constant,
    all_ones_iterate,
    all_ones_witness,
    analyze_compactness_no_go,
)


class Ticket80CompactnessNoGoTests(unittest.TestCase):
    def test_arbitrarily_large_finite_witness(self) -> None:
        for horizon in (1, 2, 8, 32):
            for lower_bound in (1, 1 << 68, 10**100):
                witness = all_ones_witness(horizon, lower_bound)
                start = witness["start"]
                q = witness["q"]
                self.assertGreaterEqual(start, lower_bound)
                self.assertEqual(start % witness["modulus"], witness["modulus"] - 1)
                current = start
                for step in range(1, horizon + 1):
                    current, valuation = accelerated_step(current)
                    self.assertEqual(valuation, 1)
                    self.assertEqual(current, all_ones_iterate(horizon, q, step))
                    self.assertGreater(current, start)
                    self.assertLessEqual(
                        (1 << step) * start,
                        (3**step) * start + all_ones_affine_constant(step),
                    )

    def test_dual_topology_limit_is_minus_one(self) -> None:
        for horizon in (1, 2, 8, 32, 128):
            start = (1 << (horizon + 1)) - 1
            self.assertEqual(start + 1, 1 << (horizon + 1))
            self.assertGreaterEqual(start, 1 << horizon)
        terminal, valuation = accelerated_step(-1)
        self.assertEqual(terminal, -1)
        self.assertEqual(valuation, 1)

    def test_full_audit_has_no_failure(self) -> None:
        audit = analyze_compactness_no_go()
        self.assertEqual(audit["computational_failure_count"], 0)
        self.assertEqual(
            audit["theorem_status"],
            "least_counterexample_finite_prefix_compactness_refuted_exactly_no_collatz_resolution",
        )
        self.assertEqual(audit["next_theorem_target"], "LeastCounterexampleUniformHeightBound")


if __name__ == "__main__":
    unittest.main()
