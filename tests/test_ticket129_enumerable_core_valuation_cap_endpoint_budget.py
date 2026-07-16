from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket129_enumerable_core_valuation_cap_endpoint_budget import (  # noqa: E402
    atanh_log_interval,
    bounded_rational_grid,
    build_audit,
    collatz_least_counterexample_valuation_cap_audit,
    goldbach_k56_endpoint_audit,
    riemann_enumerable_autocorrelation_core_audit,
    twin_increment_synchronization_audit,
    valuation_cap,
)


class Ticket129EnumerableCoreValuationCapEndpointBudgetTests(unittest.TestCase):
    def test_rational_bump_parameter_grids_are_nested_and_finite(self) -> None:
        previous: set[Fraction] = set()
        for height in range(1, 7):
            current = set(bounded_rational_grid(height))
            self.assertTrue(previous.issubset(current))
            self.assertIn(Fraction(1, height), current)
            previous = current
        audit = riemann_enumerable_autocorrelation_core_audit(6)
        self.assertTrue(
            audit["finite_enumeration_audit"]["nested_parameter_grids"]
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_least_counterexample_cap_uses_t128_lower_bound(self) -> None:
        self.assertEqual(valuation_cap(1), 2)
        self.assertEqual(valuation_cap(2), 4)
        audit = collatz_least_counterexample_valuation_cap_audit(64)
        constants = audit["exact_constants"]
        self.assertEqual(
            constants["verified_lower_bound_for_least_counterexample"], 2**28
        )
        self.assertEqual(constants["proved_accelerated_horizon"], 2**29)
        self.assertTrue(constants["squared_upper_below_8"])
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_log_intervals_are_exact_rational_enclosures(self) -> None:
        lower, upper = atanh_log_interval(Fraction(1, 3), 3)
        self.assertLess(lower, upper)
        self.assertGreater(lower, Fraction(693, 1000))
        self.assertLess(upper, Fraction(694, 1000))

    def test_goldbach_k56_is_certified_but_k57_is_not(self) -> None:
        audit = goldbach_k56_endpoint_audit()
        budget = audit["endpoint_budget"]
        self.assertEqual(budget["candidate_pointwise_residual_K"], 56)
        self.assertGreater(budget["positive_margin_decimal"], 0)
        self.assertLess(budget["K57_margin_under_same_certificate"], 0)
        self.assertTrue(
            budget["K56_is_largest_integer_certified_by_this_coarse_interval"]
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_twin_increment_identity_survives_monotone_countermodel(self) -> None:
        audit = twin_increment_synchronization_audit()
        rows = audit["strengthened_monotone_countermodel"]["rows"]
        self.assertTrue(
            all(
                row["A_and_K_are_nondecreasing"]
                and row["denominator_doubles_at_right_endpoint"]
                and row["midpoint_ratio"] > 1
                for row in rows
            )
        )
        self.assertTrue(audit["machine_audit"]["identity_passes_every_state"])
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_all_four_conjectures_remain_open(self) -> None:
        audit = build_audit(language_horizon=64)
        self.assertEqual(audit["machine_audit"]["problem_count"], 4)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
