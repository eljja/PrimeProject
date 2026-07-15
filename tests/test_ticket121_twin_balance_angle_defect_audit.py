from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket121_twin_balance_angle_defect_audit import (  # noqa: E402
    CERTIFIED_FRACTION,
    SCHEMA,
    abstract_countermodels,
    balance_angle_row,
)


class Ticket121TwinBalanceAngleDefectAuditTests(unittest.TestCase):
    def test_exact_rationalization_and_quadratic_sandwich(self) -> None:
        left_norm = 3.0
        right_norm = 2.0
        cosine = -0.25
        row = balance_angle_row(
            left_norm**2,
            left_norm * right_norm * cosine,
            right_norm**2,
            7.0,
        )
        self.assertAlmostEqual(row["norm_balance"], 6.0 / 25.0)
        self.assertAlmostEqual(row["angle_gap"], 1.25)
        self.assertAlmostEqual(
            row["actual_centered_saving"],
            row["rationalized_saving"],
            places=12,
        )
        self.assertLessEqual(
            row["quadratic_lower_certificate"],
            row["actual_centered_saving"],
        )
        self.assertLessEqual(
            row["actual_centered_saving"],
            row["quadratic_upper_certificate"],
        )

    def test_natural_mass_threshold_certifies_one_over_32(self) -> None:
        self.assertEqual(CERTIFIED_FRACTION, 1.0 / 32.0)

    def test_angle_and_balance_alone_have_exact_no_go_sequences(self) -> None:
        models = abstract_countermodels()
        angle_only = models["anti_aligned_norm_imbalance"]["sequence"]
        self.assertTrue(all(item["angle_gap"] == 2.0 for item in angle_only))
        self.assertLess(
            angle_only[-1]["actual_centered_saving_fraction"],
            3e-6,
        )
        balance_only = models["balanced_near_alignment"]["sequence"]
        self.assertTrue(
            all(item["norm_balance"] == 0.25 for item in balance_only)
        )
        self.assertLess(
            balance_only[-1]["actual_centered_saving_fraction"],
            2e-13,
        )

    def test_aligned_equal_norm_case_has_zero_defect(self) -> None:
        row = balance_angle_row(1.0, 1.0, 1.0, 1.0)
        self.assertEqual(row["norm_balance"], 0.25)
        self.assertEqual(row["angle_gap"], 0.0)
        self.assertEqual(row["actual_centered_saving"], 0.0)
        self.assertEqual(row["quadratic_lower_certificate"], 0.0)

    def test_generated_artifact_contract(self) -> None:
        payload = json.loads(
            (
                ROOT
                / "data/open-problem/ticket121-twin-balance-angle-defect-audit.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_low_divisor_balance_angle_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["scale_count"], 8)
        self.assertEqual(machine["denominator_row_count"], 248)
        self.assertEqual(machine["active_denominator_row_count"], 216)
        self.assertGreater(
            machine["minimum_qualifying_mass_fraction"], 0.63
        )
        self.assertGreater(
            machine["minimum_certified_lower_fraction"], 0.17
        )
        self.assertLess(machine["maximum_rationalization_error"], 1e-9)
        self.assertEqual(machine["maximum_lower_bound_violation"], 0.0)
        self.assertEqual(machine["maximum_upper_bound_violation"], 0.0)
        self.assertEqual(machine["minimum_gram_defect"], 0.0)
        self.assertEqual(machine["candidate_bridge_finite_closure_count"], 1)
        self.assertEqual(machine["total_failure_count"], 0)
        bridge = audit["full_budget_bridge"]
        self.assertFalse(bridge[0]["candidate_closes_finite"])
        self.assertTrue(bridge[1]["candidate_closes_finite"])
        self.assertAlmostEqual(
            bridge[0]["eta_required_with_other_finite_budgets_frozen"],
            0.23006677076937113,
            places=12,
        )
        self.assertAlmostEqual(
            bridge[1]["candidate_finite_lower_bound"],
            756220.785577069,
            places=6,
        )
        self.assertEqual(
            audit["retained_theorem"]["name"],
            "VaughanLowDivisorWeightedBalanceAngleDefectGap",
        )


if __name__ == "__main__":
    unittest.main()
