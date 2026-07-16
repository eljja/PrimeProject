from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket128_finite_core_prefix_constant_interpolation import (  # noqa: E402
    accelerated_strict_descent,
    build_audit,
    collatz_finite_prefix_closure_audit,
    goldbach_sharpened_singular_series_audit,
    prime_power_inventory,
    riemann_compact_support_prime_sum_audit,
    twin_dyadic_interpolation_audit,
)


class Ticket128FiniteCorePrefixConstantInterpolationTests(unittest.TestCase):
    def test_prime_power_inventory_is_exact_at_ten(self) -> None:
        inventory = prime_power_inventory(10)
        self.assertEqual(inventory["prime_count"], 4)
        self.assertEqual(inventory["prime_power_term_count"], 7)
        self.assertEqual(
            inventory["exponent_histogram"], {"1": 4, "2": 2, "3": 1}
        )

    def test_compact_support_reduction_has_no_infinite_prime_tail(self) -> None:
        audit = riemann_compact_support_prime_sum_audit(1_000)
        self.assertEqual(
            audit["theorem_name"], "CompactSupportFinitePrimeSideReduction"
        )
        self.assertGreater(
            audit["finite_inventory"]["prime_power_term_count"],
            audit["finite_inventory"]["prime_count"],
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_direct_descent_and_small_prefix_closure(self) -> None:
        self.assertTrue(accelerated_strict_descent(27, 1_000)["descends"])
        self.assertFalse(accelerated_strict_descent(1, 32)["descends"])
        audit = collatz_finite_prefix_closure_audit(12, 1_000)
        prefix = audit["exact_prefix_audit"]
        self.assertEqual(prefix["unresolved_after_direct_check"], 0)
        self.assertEqual(
            prefix["directly_closed_nontrivial_count"],
            prefix["nontrivial_frontier_representative_count"],
        )

    def test_goldbach_tail_bound_relaxes_endpoint_budget(self) -> None:
        audit = goldbach_sharpened_singular_series_audit(1_000)
        certificate = audit["exact_cutoff_certificate"]
        major = Fraction(
            int(certificate["major_lower_numerator"]),
            int(certificate["major_lower_denominator"]),
        )
        self.assertGreater(major, Fraction(131_917, 100_000))
        self.assertTrue(
            audit["conservative_endpoint_budget"][
                "exact_positive_margin_lower_decimal"
            ]
            > 0
        )
        self.assertEqual(
            audit["conservative_endpoint_budget"][
                "candidate_pointwise_residual_K"
            ],
            55,
        )

    def test_twin_endpoint_countermodel_requires_interpolation(self) -> None:
        audit = twin_dyadic_interpolation_audit()
        theorem = audit["proved_interpolation_theorem"]
        self.assertEqual(theorem["frozen_endpoint_ceiling"], 0.92)
        self.assertEqual(theorem["maximum_delta_when_c_is_1"], 0.08)
        self.assertTrue(theorem["candidate_condition_passes"])
        self.assertTrue(
            all(
                row["endpoint_recurrence_equality"]
                and row["all_scale_bound_fails"]
                for row in audit["endpoint_no_go"]["rows"]
            )
        )

    def test_small_build_keeps_all_conjectures_open(self) -> None:
        audit = build_audit(collatz_bits=12, collatz_step_cap=1_000)
        self.assertEqual(audit["machine_audit"]["problem_count"], 4)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
