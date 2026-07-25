from __future__ import annotations

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket141_one_sided_moving_floor_robust_dual_large_sieve import (  # noqa: E402
    SCHEMA,
    build_audit,
    minimum_floor_for_window_below_two,
    window_is_below_two,
)


class Ticket141OneSidedMovingFloorRobustDualLargeSieveTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            (
                "primeproject.ticket141-one-sided-moving-floor-robust-dual-"
                "large-sieve.v1"
            ),
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_shifted_trace_separates_opposite_spikes(self) -> None:
        rows = self.audit["riemann"]["shifted_trace_audit"]["rows"]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                Fraction(row["positive_shifted_trace_moment"]["exact"]),
                0,
            )
            self.assertGreaterEqual(
                Fraction(row["negative_shifted_trace_moment"]["exact"]),
                Fraction(row["shifted_threshold_moment"]["exact"]),
            )

    def test_moving_floor_thresholds_are_exact(self) -> None:
        expected = {
            16: 8,
            64: 31,
            256: 123,
            1024: 493,
            4096: 1970,
            16384: 7879,
        }
        for period, minimum in expected.items():
            self.assertEqual(
                minimum_floor_for_window_below_two(period),
                minimum,
            )
            self.assertTrue(window_is_below_two(period, minimum))
            self.assertFalse(window_is_below_two(period, minimum - 1))

    def test_moving_floor_ratio_converges_to_linear_barrier(self) -> None:
        rows = self.audit["collatz"]["moving_floor_audit"]["rows"]
        target = 1 / (3 * math.log(2))
        self.assertEqual(len(rows), 6)
        self.assertLess(
            abs(rows[-1]["floor_to_period_ratio"] - target),
            abs(rows[0]["floor_to_period_ratio"] - target),
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_raw_moment_dual_has_quadratic_exponential_lower_bound(
        self,
    ) -> None:
        rows = self.audit["goldbach"][
            "raw_moment_conditioning_audit"
        ]["rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            order = row["moment_order_q"]
            leading = Fraction(
                row["endpoint_leading_dual_coefficient"]["exact"]
            )
            self.assertGreater(
                leading,
                2 ** (order * (order - 1) // 2),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_q56_conditioning_exponent_is_not_k56_identity(self) -> None:
        audit = self.audit["goldbach"]["raw_moment_conditioning_audit"]
        self.assertEqual(audit["largest_order"], 56)
        self.assertEqual(audit["largest_lower_bound_exponent"], 1540)
        self.assertIn(
            "K=56 residual margin",
            self.audit["goldbach"]["proof_boundary"],
        )

    def test_bilinear_large_sieve_diagnostics_stay_below_theorem(self) -> None:
        rows = self.audit["twin_prime"][
            "bilinear_large_sieve_audit"
        ]["rows"]
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertLess(
                row["observed_operator_norm_squared"],
                row["large_sieve_operator_norm_squared_bound"],
            )
        self.assertLess(rows[-1]["bounded_coefficient_relative_bound"], 0.2)

    def test_each_track_has_one_revised_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilShiftedLogMomentBelowTailGap",
            "collatz": (
                "CycleMinimumAboveExactPowerOfTwoWindowThreshold"
            ),
            "goldbach": (
                "LocalizedOrthogonalArithmeticK56DualCertificate"
            ),
            "twin_prime": (
                "UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass"
            ),
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(
                    section["route_decision"]["next_theorem"], theorem
                )
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"], 0
                )


if __name__ == "__main__":
    unittest.main()
