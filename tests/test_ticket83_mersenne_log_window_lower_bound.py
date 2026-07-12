from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket83_mersenne_log_window_lower_bound_lab import (  # noqa: E402
    analyze_log_window_lower_bound,
    audit_quantitative_horizon,
    explicit_exponent,
)


class Ticket83MersenneLogWindowLowerBoundTests(unittest.TestCase):
    def test_explicit_sequence_and_exact_log_guard(self) -> None:
        for horizon in (2, 3, 8, 32, 128):
            exponent = explicit_exponent(horizon)
            self.assertEqual(exponent, 3 + (1 << (2 * horizon + 3)))
            self.assertEqual(exponent % (1 << (2 * horizon + 3)), 3)
            self.assertLess(exponent, 1 << (2 * horizon + 4))

    def test_symbolic_constant_and_growth_guards(self) -> None:
        for horizon in (2, 4, 16, 64):
            audit = audit_quantitative_horizon(horizon)
            self.assertEqual(audit["maximum_denominator_power"], 2 * horizon + 4)
            self.assertEqual(audit["constant_bound_failure_count"], 0)
            self.assertEqual(audit["growth_proof_failure_count"], 0)
            self.assertEqual(audit["total_failure_count"], 0)

    def test_full_audit_and_claim_boundary(self) -> None:
        result = analyze_log_window_lower_bound()
        audit = result["machine_audit"]
        self.assertEqual(audit["horizon_case_count"], 255)
        self.assertEqual(audit["symbolic_state_count"], 33150)
        self.assertEqual(audit["total_failure_count"], 0)
        self.assertEqual(result["next_theorem_target"], "MersenneLogWindowDichotomy")
        self.assertIn("neither a divergent Collatz orbit", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
