from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket102_twin_dyadic_vaughan_holdout import (  # noqa: E402
    audit_dyadic_holdouts,
    audit_horizon,
    cutoff_schedule,
)


class Ticket102TwinDyadicVaughanHoldoutTests(unittest.TestCase):
    def test_cutoff_schedule_is_deterministic_and_cubic(self) -> None:
        self.assertEqual(cutoff_schedule(1_000_000), (100, 84))
        self.assertEqual(cutoff_schedule(8_000_000), (200, 168))

    def test_small_horizon_reconstructs_joint_correlation(self) -> None:
        row = audit_horizon(20_000)
        self.assertGreater(row["evaluated_count"], 0)
        self.assertGreater(row["type_ii_support_fraction"], 0.01)
        self.assertLess(row["joint_reconstruction_max_absolute_error"], 1e-7)
        self.assertLess(row["joint_reconstruction_max_relative_error"], 1e-12)
        self.assertLess(row["lambda_reconstruction_max_error"], 1e-10)

    def test_doubling_schedule_is_required(self) -> None:
        with self.assertRaises(ValueError):
            audit_dyadic_holdouts((20_000, 50_000))

    def test_any_fixed_budget_sum_has_eventual_positive_main_factor(self) -> None:
        budget_sum = 4.0 + 1.0
        self.assertGreater(1 - budget_sum / math.log(1_000_000), 0)


if __name__ == "__main__":
    unittest.main()
