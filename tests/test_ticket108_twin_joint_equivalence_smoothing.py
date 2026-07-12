from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket108_twin_joint_equivalence_smoothing import (  # noqa: E402
    analyze_ticket108,
    audit_joint_equivalence_and_smoothing,
    dyadic_bump,
)


class Ticket108TwinJointEquivalenceSmoothingTests(unittest.TestCase):
    def test_bump_is_nonnegative_and_bounded(self) -> None:
        numbers = np.arange(501, 1001, dtype=np.int64)
        weights = dyadic_bump(numbers, 1_000)
        self.assertGreaterEqual(float(weights.min()), 0.0)
        self.assertLessEqual(float(weights.max()), 1.0)

    def test_hard_joint_target_is_exact_recombination(self) -> None:
        row = audit_joint_equivalence_and_smoothing(2_000)
        self.assertLess(row["hard_joint_equivalence_absolute_error"], 1e-9)
        self.assertLess(row["type_ii_q_to_vaughan_max_error"], 1e-9)

    def test_smoothed_bridge_recombines_and_bounds_contamination(self) -> None:
        row = audit_joint_equivalence_and_smoothing(2_000)
        self.assertLess(row["smooth_joint_equivalence_absolute_error"], 1e-9)
        self.assertLess(row["smooth_contamination_decomposition_absolute_error"], 1e-9)
        self.assertTrue(row["smooth_contamination_bound_holds"])

    def test_full_audit_contract(self) -> None:
        audit = analyze_ticket108()
        self.assertEqual(audit["machine_audit"]["maximum_horizon"], 8_000_000)
        self.assertEqual(audit["machine_audit"]["row_count"], 6)
        self.assertEqual(audit["machine_audit"]["smoothing_improvement_count"], 2)
        self.assertEqual(audit["machine_audit"]["smoothing_worsening_count"], 4)
        self.assertEqual(audit["machine_audit"]["contract_failure_count"], 0)
        self.assertEqual(audit["next_theorem_target"], "SmoothedShiftTwoTypeIICorrelationExcess")


if __name__ == "__main__":
    unittest.main()
