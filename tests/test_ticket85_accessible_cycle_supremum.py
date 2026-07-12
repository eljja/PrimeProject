from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket85_accessible_cycle_supremum_lab import (  # noqa: E402
    analyze_cycle_supremum,
    audit_horizon,
    cycle_formula,
)


class Ticket85AccessibleCycleSupremumTests(unittest.TestCase):
    def test_cycle_family_formula_and_accessibility(self) -> None:
        for length in range(2, 20):
            cycle = cycle_formula(length)
            x = cycle["cycle_value"]
            current = x
            for valuation in [2] + [1] * (length - 1):
                current = (3 * current + 1) / (1 << valuation)
            self.assertEqual(current, x)
            self.assertEqual((x.numerator * pow(x.denominator, -1, 8)) % 8, 1)
            self.assertEqual(cycle["reciprocal_mean"].numerator, length)
            self.assertEqual(cycle["reciprocal_mean"].denominator, length + 1)

    def test_positive_lifts_have_unit_log_guard(self) -> None:
        for horizon in (2, 3, 8, 32, 128):
            audit = audit_horizon(horizon)
            self.assertLess(audit["exponent"], 1 << (horizon + 2))
            self.assertEqual(audit["total_failure_count"], 0)

    def test_full_audit_and_boundary(self) -> None:
        result = analyze_cycle_supremum()
        audit = result["machine_audit"]
        self.assertEqual(audit["horizon_case_count"], 255)
        self.assertEqual(audit["maximum_precision"], 259)
        self.assertEqual(audit["symbolic_state_count"], 33150)
        self.assertEqual(audit["total_failure_count"], 0)
        self.assertEqual(result["next_theorem_target"], "CoefficientOneBoundary")
        self.assertIn("constructs no divergent orbit", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
